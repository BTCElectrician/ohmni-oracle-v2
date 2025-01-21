I'll create a comprehensive workflow breakdown of the system based on the provided codebase.

# System Workflow Analysis

## 1. Data Flow Diagram
```
Input Files (PDF Drawings)
       ↓
Document Intelligence Processing
       ↓
Text & Layout Extraction
       ↓
Drawing Type Classification
       ↓
GPT-4 Processing & Structuring
       ↓
JSON Output Generation
       ↓
Structured Data Storage
```

## 2. Component Interaction Flow

### Primary Processing Pipeline
```
drawing_processor.py (Main Handler)
         ↓
    Initialization
         ↓
document_processor.py (Azure Setup)
         ↓
PDF Processing Branch
    ↙     ↓     ↘
Electrical  Mechanical  Plumbing
    ↓         ↓          ↓
Type-Specific Processing
         ↓
JSON Structure Generation
```

### Drawing Type-Specific Processing

**Electrical Drawings:**
```
Input PDF
    ↓
Panel Schedule Detection
    ↓
Circuit Information Extraction
    ↓
Equipment Specifications
    ↓
Structured JSON Output
```

**Mechanical Drawings:**
```
Input PDF
    ↓
Equipment Schedule Processing
    ↓
HVAC Details Extraction
    ↓
System Specifications
    ↓
Structured JSON Output
```

**Plumbing Drawings:**
```
Input PDF
    ↓
Fixture Schedule Analysis
    ↓
Pipe Sizing Information
    ↓
System Requirements
    ↓
Structured JSON Output
```

## 3. File Purpose Map

### Core Processing Files:

**drawing_processor.py**
- Role: Main processing orchestrator
- Triggers: File input
- Reference: 

```32:132:utils/drawing_processor.py
class DrawingProcessor(DocumentProcessor):
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        super().__init__(endpoint, key)
        self.openai_client = AsyncOpenAI()

    async def process_drawing(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Drawing file not found: {file_path}")
            
        file_size = os.path.getsize(file_path)
        if file_size > 50_000_000:  # 50MB limit
            return await self.process_large_drawing(file_path)

        try:
            async with aiofiles.open(file_path, 'rb') as file:
                content = await file.read()
                
            return await self._process_with_azure(content)
        except Exception as e:
            logger.error(f"Azure processing failed for {file_path}: {e}")
            return await self._fallback_to_pymupdf(file_path)

    async def _process_with_azure(self, content: bytes) -> Dict[str, Any]:
        poller = await self.client.begin_analyze_document(
            "prebuilt-layout",
            document=content,
            pages="1-",
            features=["tables", "selectionMarks", "languages"]
        )
        return self._parse_drawing_content(await poller.result())
    def _parse_drawing_content(self, result: Any) -> Dict[str, Any]:
        parsed_data = {
            "tables": [],
            "annotations": [],
            "text_blocks": [],
            "metadata": {
                "page_count": result.page_count,
                "languages": result.languages
            }
        }
        
        for table in result.tables:
            processed_table = self._process_table(table)
            if self._is_panel_schedule(processed_table):
                processed_table["type"] = "panel_schedule"
            parsed_data["tables"].append(processed_table)
            
        for paragraph in result.paragraphs:
            parsed_data["text_blocks"].append({
                "content": paragraph.content,
                "coordinates": paragraph.bounding_regions[0].polygon if paragraph.bounding_regions else None,
                "role": paragraph.role
            })
            
        return parsed_data

    async def process_batch(self, file_paths: List[str]) -> Dict[str, Dict[str, Any]]:
        tasks = [self.process_drawing(path) for path in file_paths]
        results = {}
        
        async for task, path in tqdm_asyncio.as_completed(
            tasks, 
            total=len(tasks),
            desc="Processing drawings"
        ):
            try:
                results[path] = await task
            except Exception as e:
                logger.error(f"Failed to process {path}: {e}")
                results[path] = {"error": str(e)}
                
        return results
    async def process_drawing(self, raw_content: str, drawing_type: str, client: AsyncOpenAI):
        system_message = f"""
        Parse this {drawing_type} drawing/schedule into a structured JSON format. Guidelines:
        1. For text: Extract key information, categorize elements.
        2. For tables: Preserve structure, use nested arrays/objects.
        3. Create a hierarchical structure, use consistent key names.
        4. Include metadata (drawing number, scale, date) if available.
        5. {DRAWING_INSTRUCTIONS.get(drawing_type, DRAWING_INSTRUCTIONS["General"])}
        6. For all drawing types, if room information is present, always include a 'rooms' array in the JSON output, with each room having at least 'number' and 'name' fields.
        Ensure the entire response is a valid JSON object.
        """
        
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": raw_content}
                ],
                temperature=0.2,
                max_tokens=16000,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error processing {drawing_type} drawing: {str(e)}")
            raise
```


**document_processor.py**
- Role: Azure service initialization
- Triggers: Called by drawing_processor.py
- Reference:

```11:31:utils/document_processor.py
class DocumentProcessor:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        if not self.endpoint:
            raise ValueError("Azure Form Recognizer endpoint not provided")
            
        try:
            self.credential = DefaultAzureCredential()
            self.client = DocumentAnalysisClient(
                endpoint=self.endpoint, 
                credential=self.credential
            )
        except Exception as e:
            key = key or os.getenv("AZURE_FORM_RECOGNIZER_KEY")
            if not key:
                raise ValueError("Neither DefaultAzureCredential nor API key available")
            self.credential = AzureKeyCredential(key)
            self.client = DocumentAnalysisClient(
                endpoint=self.endpoint, 
                credential=self.credential
            )
```


### Utility Files:

**pdf_processor.py**
- Role: PDF text extraction
- Triggers: Called during initial processing
- Reference:

```6:56:utils/pdf_processor.py
async def extract_text_and_tables_from_pdf(pdf_path: str) -> str:
    doc = pymupdf.open(pdf_path)
    all_content = ""
    for page in doc:
        text = page.get_text()
        all_content += "TEXT:\n" + text + "\n"
        
        tables = page.find_tables()
        for table in tables:
            all_content += "TABLE:\n"
            markdown = table.to_markdown()
            all_content += markdown + "\n"
    
    return all_content

async def structure_panel_data(client: AsyncOpenAI, raw_content: str) -> dict:
    prompt = f"""
    You are an expert in electrical engineering and panel schedules. 
    Please structure the following content from an electrical panel schedule into a valid JSON format. 
    The content includes both text and tables. Extract key information such as panel name, voltage, amperage, circuits, and any other relevant details.
    Pay special attention to the tabular data, which represents circuit information.
    Ensure your entire response is a valid JSON object.
    Raw content:
    {raw_content}
    """
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that structures electrical panel data into JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=2000,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
async def process_pdf(pdf_path: str, output_folder: str, client: AsyncOpenAI):
    print(f"Processing PDF: {pdf_path}")
    raw_content = await extract_text_and_tables_from_pdf(pdf_path)
    
    structured_data = await structure_panel_data(client, raw_content)
    
    panel_name = structured_data.get('panel_name', 'unknown_panel').replace(" ", "_").lower()
    filename = f"{panel_name}_electric_panel.json"
    filepath = os.path.join(output_folder, filename)
    
    with open(filepath, 'w') as f:
        json.dump(structured_data, f, indent=2)
    
    print(f"Saved structured panel data: {filepath}")
```


**pdf_utils.py**
- Role: PDF manipulation utilities
- Triggers: Support functions for processing
- Reference:

```9:97:utils/pdf_utils.py
def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
    file_path (str): The path to the PDF file.
    
    Returns:
    str: The extracted text from the PDF.
    
    Raises:
    Exception: If there's an error in opening or processing the PDF.
    """
    logger.info(f"Starting text extraction for {file_path}")
    try:
        with pdfplumber.open(file_path) as pdf:
            logger.info(f"Successfully opened {file_path}")
            text = ""
            for i, page in enumerate(pdf.pages):
                logger.info(f"Processing page {i+1} of {len(pdf.pages)}")
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    logger.warning(f"No text extracted from page {i+1}")
        
        if not text:
            logger.warning(f"No text extracted from {file_path}")
        else:
            logger.info(f"Successfully extracted text from {file_path}")
        
        return text
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        raise
def extract_images(file_path: str) -> List[Dict[str, Any]]:
    """
    Extract images from a PDF file.
    
    Args:
    file_path (str): The path to the PDF file.
    
    Returns:
    List[Dict[str, Any]]: A list of dictionaries containing image information.
    
    Raises:
    Exception: If there's an error in opening or processing the PDF.
    """
    try:
        images = []
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                for image in page.images:
                    images.append({
                        'page': i + 1,
                        'bbox': image['bbox'],
                        'width': image['width'],
                        'height': image['height'],
                        'type': image['type']
                    })
        
        logger.info(f"Extracted {len(images)} images from {file_path}")
        return images
    except Exception as e:
        logger.error(f"Error extracting images from {file_path}: {str(e)}")
        raise

def get_pdf_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get metadata from a PDF file.
    
    Args:
    file_path (str): The path to the PDF file.
    
    Returns:
    Dict[str, Any]: A dictionary containing the PDF metadata.
    
    Raises:
    Exception: If there's an error in opening or processing the PDF.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            metadata = pdf.metadata
        logger.info(f"Successfully extracted metadata from {file_path}")
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata from {file_path}: {str(e)}")
        raise
```


### Configuration Files:

**settings.py**
- Role: Environment configuration
- Triggers: System initialization
- Reference:

```1:6:config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```


### Template Files:

**room_templates.py**
- Role: Room data structure definitions
- Triggers: During room data processing
- Reference:

```1:90:templates/room_templates.py
import json
import os

def load_template(template_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, f"{template_name}_template.json")
    try:
        with open(template_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Template file not found: {template_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {template_path}")
        return {}

def generate_rooms_data(parsed_data, room_type):
    template = load_template(room_type)
    
    metadata = parsed_data.get('metadata', {})
    
    rooms_data = {
        "metadata": metadata,
        "project_name": metadata.get('project', ''),
        "floor_number": '',
        "rooms": []
    }
    
    parsed_rooms = parsed_data.get('rooms', [])
    
    if not parsed_rooms:
        print(f"No rooms found in parsed data for {room_type}.")
        return rooms_data

    for parsed_room in parsed_rooms:
        room_number = str(parsed_room.get('number', ''))
        room_name = parsed_room.get('name', '')
        
        if not room_number or not room_name:
            print(f"Skipping room with incomplete data: {parsed_room}")
            continue
        
        room_data = template.copy()
        room_data['room_id'] = f"Room_{room_number}"
        room_data['room_name'] = f"{room_name}_{room_number}"
        
        # Copy all fields from parsed_room to room_data
        for key, value in parsed_room.items():
            if key not in ['number', 'name']:  # Avoid duplicating number and name
                room_data[key] = value
        
        rooms_data['rooms'].append(room_data)
    
    return rooms_data
def process_architectural_drawing(parsed_data, file_path, output_folder):
    is_reflected_ceiling = "REFLECTED CEILING PLAN" in file_path.upper()
    
    project_name = parsed_data.get('metadata', {}).get('project', '')
    job_number = parsed_data.get('metadata', {}).get('job_number', '')
    floor_number = ''  # If floor number is available in the future, extract it here
    
    e_rooms_data = generate_rooms_data(parsed_data, 'e_rooms')
    a_rooms_data = generate_rooms_data(parsed_data, 'a_rooms')
    
    e_rooms_file = os.path.join(output_folder, f'e_rooms_details_floor_{floor_number}.json')
    a_rooms_file = os.path.join(output_folder, f'a_rooms_details_floor_{floor_number}.json')
    
    with open(e_rooms_file, 'w') as f:
        json.dump(e_rooms_data, f, indent=2)
    
    with open(a_rooms_file, 'w') as f:
        json.dump(a_rooms_data, f, indent=2)
    
    return {
        "e_rooms_file": e_rooms_file,
        "a_rooms_file": a_rooms_file,
        "is_reflected_ceiling": is_reflected_ceiling
    }

if __name__ == "__main__":
    # This block is for testing purposes. You can remove it if not needed.
    test_file_path = "path/to/your/test/file.json"
    test_output_folder = "path/to/your/test/output/folder"
    
    with open(test_file_path, 'r') as f:
        test_parsed_data = json.load(f)
    
    result = process_architectural_drawing(test_parsed_data, test_file_path, test_output_folder)
    print(result)
```


## Data Transformation Flow

```
Raw PDF
   ↓
Text Extraction (pdf_processor.py)
   ↓
Layout Analysis (document_processor.py)
   ↓
Drawing Classification
   ↓
GPT Processing (drawing_processor.py)
   ↓
Template Application (room_templates.py)
   ↓
Final JSON Structure
```

### Error Handling Flow
```
Process Start
   ↓
Azure Processing Attempt
   ↓
If Failure → PyMuPDF Fallback
   ↓
If Success → Continue Processing
   ↓
Error Logging & Reporting
   ↓
Process Completion/Failure Notice
```

