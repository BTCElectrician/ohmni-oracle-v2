Directory structure:
└── btcelectrician-ohmni-oracle-v2/
    ├── README.md
    ├── git-best-practices-guide.md
    ├── main.py
    ├── pyrightconfig.json
    ├── requirements.txt
    ├── upgrade.md
    ├── v1-workflow.md
    ├── .cursorrules
    ├── config/
    │   └── settings.py
    ├── data/
    ├── documents/
    │   ├── lessonslearned.md
    │   ├── proj-work-flow.md
    │   └── testscode.md
    ├── templates/
    │   ├── a_rooms_template.json
    │   ├── e_rooms_template.json
    │   └── room_templates.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test-command.md
    │   ├── test_drawing_processor_fix.py
    │   └── test_processor.py
    └── utils/
        ├── __init__.py
        ├── common_utils.py
        ├── document_processor.py
        ├── drawing_processor.py
        ├── file_utils.py
        ├── pdf_processor.py
        └── pdf_utils.py


Files Content:

================================================
File: README.md
================================================
# Ohmni Oracle

This project processes various types of architectural and engineering drawings, including electrical, mechanical, plumbing, and architectural documents. It uses PyMuPDF for general text extraction, with specialized Azure Document Intelligence processing for electrical panel schedules, and GPT-4o-mini for data structuring.

## Features

- Intelligent document processing:
  - PyMuPDF for general drawing text extraction
  - Azure Document Intelligence for electrical panel schedules
  - GPT-4o-mini for structured data generation
- Smart detection of electrical panel schedules
- Asynchronous batch processing of multiple drawings
- Specialized templates for different drawing types
- Comprehensive error handling and logging
- Test suite for validation
- Support for multiple document types:
  - Architectural drawings
  - Electrical drawings (with specialized panel schedule processing)
  - Mechanical drawings
  - Plumbing drawings

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with required credentials:
```env
DI_KEY=your_azure_key
DI_ENDPOINT=your_azure_endpoint
OPENAI_API_KEY=your_api_key_here
```
4. Ensure you have the necessary JSON templates in the `templates` folder:
- `a_rooms_template.json`
- `e_rooms_template.json`

## File Structure

- `main.py`: Asynchronous PDF processing coordinator with batch processing capabilities
- `.env`: Environment variables (Azure and OpenAI credentials)
- `.gitignore`: Comprehensive Git ignore rules for Python projects
- `.cursorrules`: Cursor editor configuration with AI/ML processing rules
- `git-best-practices-guide.md`: Detailed Git workflow and best practices
- `requirements.txt`: Project dependencies including Azure AI and document processing packages

### Config
- `config/.gitignore`: Environment-specific ignore rules
- `config/settings.py`: Centralized configuration for Azure and processing settings

### Templates
- `templates/room_templates.py`: Room data processing and template management
- `templates/a_rooms_template.json`: Architectural room data schema
- `templates/e_rooms_template.json`: Electrical room data schema

### Utils
- `utils/__init__.py`: Package initialization
- `utils/document_processor.py`: Base Azure Document Intelligence processor
- `utils/drawing_processor.py`: Specialized drawing processing with Azure integration
- `utils/file_utils.py`: File system operations and folder management
- `utils/pdf_processor.py`: PDF processing with Azure and PyMuPDF fallback
- `utils/pdf_utils.py`: Advanced PDF utilities for text and image extraction

### Tests
- `tests/__init__.py`: Test package initialization
- `tests/test_processor.py`: Drawing processor test suite

### Documents
- `documents/proj-work-flow.md`: System workflow documentation

## Folder Structure
ohmni_oracle/
├── config/
│   ├── .gitignore
│   └── settings.py
├── documents/
│   └── proj-work-flow.md
├── templates/
│   ├── __pycache__/
│   ├── a_rooms_template.json
│   ├── e_rooms_template.json
│   └── room_templates.py
├── tests/
│   ├── __init__.py
│   └── test_processor.py
├── utils/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── drawing_processor.py
│   ├── file_utils.py
│   ├── pdf_processor.py
│   └── pdf_utils.py
├── venv/
├── .cursorrules
├── .env
├── .gitignore
├── git-best-practices-guide.md
├── main.py
├── README.md
└── requirements.txt

================================================
File: git-best-practices-guide.md
================================================
# Comprehensive Git Best Practices Guide

## Table of Contents
1. [Understanding Git and Version Control](#1-understanding-git-and-version-control)
2. [Setting Up Your Project](#2-setting-up-your-project)
3. [Best Practices for Commits](#3-best-practices-for-commits)
4. [Branching Strategy](#4-branching-strategy)
5. [Collaboration and Remote Repositories](#5-collaboration-and-remote-repositories)
6. [Handling Mistakes](#6-handling-mistakes)
7. [Advanced Git Features](#7-advanced-git-features)
8. [Maintaining Your Repository](#8-maintaining-your-repository)
9. [Best Practices for Python Projects](#9-best-practices-for-python-projects)
10. [Continuous Learning](#10-continuous-learning)

## 1. Understanding Git and Version Control

Git is a distributed version control system that allows you to track changes in your code, collaborate with others, and maintain different versions of your project. Key concepts include:

- **Repository**: A container for your project, including all files and their revision history.
- **Commit**: A snapshot of your project at a specific point in time.
- **Branch**: An independent line of development.
- **Remote**: A version of your project hosted on a server (like GitHub).

## 2. Setting Up Your Project

Before you start coding:

a. Initialize a Git repository:
   ```
   git init
   ```

b. Create a .gitignore file immediately:
   ```
   touch .gitignore
   ```

c. Edit .gitignore to exclude common unnecessary files:
   ```
   # Python
   __pycache__/
   *.py[cod]
   *.so

   # Virtual Environment
   venv/
   env/
   *.venv
   
   # IDEs and Editors
   .vscode/
   .idea/
   *.swp
   *.swo

   # OS generated files
   .DS_Store
   Thumbs.db

   # Project-specific
   *.log
   *.sqlite3
   ```

d. Commit your .gitignore file:
   ```
   git add .gitignore
   git commit -m "Initial commit: Add .gitignore"
   ```

## 3. Best Practices for Commits

a. Commit early and often:
   - Make small, focused commits that do one thing.
   - This makes it easier to understand changes and revert if necessary.

b. Write meaningful commit messages:
   - Use the imperative mood: "Add feature" not "Added feature"
   - First line: Short (50 chars or less) summary
   - Followed by a blank line
   - Then a more detailed explanation if necessary

c. Before committing:
   - Always run `git status` to see what changes you're about to commit
   - Use `git diff` to review your changes

d. Use `git add -p` to stage changes in hunks, allowing you to make more granular commits

## 4. Branching Strategy

a. Use branches for new features or bug fixes:
   ```
   git checkout -b feature/new-login-system
   ```

b. Keep your main (or master) branch stable

c. Merge or rebase frequently to stay up-to-date with the main branch

d. Delete branches after merging:
   ```
   git branch -d feature/new-login-system
   ```

## 5. Collaboration and Remote Repositories

a. Clone repositories:
   ```
   git clone https://github.com/username/repository.git
   ```

b. Add remotes:
   ```
   git remote add origin https://github.com/username/repository.git
   ```

c. Push your changes:
   ```
   git push origin main
   ```

d. Pull changes from others:
   ```
   git pull origin main
   ```

## 6. Handling Mistakes

a. Undo last commit (keeping changes):
   ```
   git reset HEAD~1
   ```

b. Amend last commit:
   ```
   git commit --amend
   ```

c. Undo staged changes:
   ```
   git reset HEAD <file>
   ```

d. Discard local changes:
   ```
   git checkout -- <file>
   ```

## 7. Advanced Git Features

a. Stashing changes:
   ```
   git stash
   git stash pop
   ```

b. Interactive rebase to clean up commit history:
   ```
   git rebase -i HEAD~3
   ```

c. Use tags for releases:
   ```
   git tag -a v1.0 -m "Version 1.0"
   ```

## 8. Maintaining Your Repository

a. Regularly update your .gitignore if you start using new tools or generating new types of files

b. Use `git clean -n` to see what untracked files would be removed (use -f to actually remove them)

c. Periodically run `git gc` to clean up and optimize your local repository

## 9. Best Practices for Python Projects

a. Use virtual environments for every project

b. Generate a requirements.txt file:
   ```
   pip freeze > requirements.txt
   ```

c. Include the requirements.txt in your repository, but not the virtual environment itself

## 10. Continuous Learning

a. Read Git documentation regularly

b. Practice with online Git tutorials and sandboxes

c. Contribute to open-source projects to see how larger teams use Git

Remember, becoming proficient with Git is a journey. Don't be afraid to make mistakes – that's how you learn. Always keep a backup of your important work, especially when trying new Git commands.

By following these practices, you'll maintain a clean, efficient, and professional Git repository. This will make your development process smoother, facilitate collaboration, and showcase your growing skills as a software developer.



================================================
File: main.py
================================================
# Standard library imports
from pathlib import Path
import json
import sys
import asyncio
import random
import time
import logging
import os
from datetime import datetime
from typing import Dict, List, Any

# Third-party imports
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm
import aiofiles

# Local application imports
from templates.room_templates import process_architectural_drawing
from utils.pdf_processor import extract_text_and_tables_from_pdf
from utils.drawing_processor import DrawingProcessor
from utils.document_processor import DocumentProcessor
from utils.common_utils import is_panel_schedule_file

# Suppress pdfminer debug output
logging.getLogger('pdfminer').setLevel(logging.ERROR)

# Constants
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
API_RATE_LIMIT = 60  # Adjust if needed
TIME_WINDOW = 60  # Time window to respect the rate limit
BATCH_SIZE = 10  # Batch size for processing

drawing_types = {
    'Architectural': ['A', 'AD'],
    'Electrical': ['E', 'ED'],
    'Mechanical': ['M', 'MD'],
    'Plumbing': ['P', 'PD'],
    'Site': ['S', 'SD'],
    'Civil': ['C', 'CD'],
    'Low Voltage': ['LV', 'LD'],
    'Fire Alarm': ['FA', 'FD'],
    'Kitchen': ['K', 'KD']
}

def setup_logging(output_folder: Path) -> None:
    log_folder = output_folder / 'logs'
    log_folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_folder / f"process_log_{timestamp}.txt"
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    print(f"Logging to: {log_file}")

def get_drawing_type(filename: Path) -> str:
    prefix = filename.stem[:2].upper()
    for dtype, prefixes in drawing_types.items():
        if any(prefix.startswith(p.upper()) for p in prefixes):
            return dtype
    return 'General'

async def async_safe_api_call(client: AsyncOpenAI, *args: Any, **kwargs: Any) -> Any:
    """
    Make an API call with retry logic and exponential backoff.
    
    Args:
        client: AsyncOpenAI client instance
        *args: Positional arguments for the API call
        **kwargs: Keyword arguments for the API call
        
    Returns:
        API response
        
    Raises:
        Exception: If max retries are reached
    """
    retries = 0
    delay = 1  # Initial delay for backoff
    while retries < MAX_RETRIES:
        try:
            return await client.chat.completions.create(*args, **kwargs)
        except Exception as e:
            if "rate limit" in str(e).lower():
                logging.warning(f"Rate limit hit, retrying in {delay} seconds...")
                retries += 1
                delay = min(delay * 2, 60)  # Exponential backoff, with a max delay cap
                await asyncio.sleep(delay + random.uniform(0, 1))  # Adding jitter
            else:
                logging.error(f"API call failed: {e}")
                await asyncio.sleep(RETRY_DELAY)
                retries += 1
    logging.error("Max retries reached for API call")
    raise Exception("Failed to make API call after maximum retries")

async def process_pdf_async(pdf_path: Path, client: AsyncOpenAI, output_folder: Path, 
                          drawing_type: str, templates_created: Dict[str, bool],
                          processor: DrawingProcessor) -> Dict[str, Any]:
    """
    Process a single PDF file asynchronously.
    
    Args:
        pdf_path: Path to the PDF file
        client: AsyncOpenAI client instance
        output_folder: Output directory path
        drawing_type: Type of drawing being processed
        templates_created: Dictionary tracking created templates
        processor: Shared DrawingProcessor instance for document processing
    """
    file_name = pdf_path.name
    try:
        async with aiofiles.open(pdf_path, 'rb') as pdf_file:
            with tqdm(total=100, desc=f"Processing {file_name}", leave=False) as pbar:
                try:
                    pbar.update(10)  # Start processing
                    
                    # Get file content
                    raw_content = None
                    
                    # Try Azure Document Intelligence first
                    if is_panel_schedule_file(str(pdf_path)):
                        logging.info(f"Panel schedule detected, using Document Intelligence: {pdf_path}")
                        try:
                            raw_content = await processor.process_drawing(pdf_path)
                        except Exception as e:
                            logging.error(f"Document Intelligence failed for panel schedule: {str(e)}")
                            raw_content = await extract_text_and_tables_from_pdf(pdf_path)
                    else:
                        logging.info(f"Using PyMuPDF for standard processing: {pdf_path}")
                        raw_content = await extract_text_and_tables_from_pdf(pdf_path)
                    
                    pbar.update(20)  # Text and tables extracted
                    structured_json = await processor.analyze_document(raw_content, drawing_type, client)
                    pbar.update(40)  # API call completed
                    
                    type_folder = output_folder / drawing_type
                    type_folder.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        parsed_json = json.loads(structured_json)
                        output_filename = f"{pdf_path.stem}_structured.json"
                        output_path = type_folder / output_filename
                        
                        async with aiofiles.open(output_path, 'w') as f:
                            await f.write(json.dumps(parsed_json, indent=2))
                        
                        pbar.update(20)  # JSON saved
                        logging.info(f"Successfully processed and saved: {output_path}")
                        
                        if drawing_type == 'Architectural':
                            result = process_architectural_drawing(parsed_json, str(pdf_path), str(type_folder))
                            templates_created['floor_plan'] = True
                            logging.info(f"Created room templates: {result}")
                        
                        pbar.update(10)  # Processing completed
                        return {"success": True, "file": str(output_path)}
                        
                    except json.JSONDecodeError as e:
                        pbar.update(100)  # Ensure bar completes on error
                        logging.error(f"JSON parsing error for {pdf_path}: {str(e)}")
                        logging.info(f"Raw API response: {structured_json}")
                        raw_output_filename = f"{pdf_path.stem}_raw_response.json"
                        raw_output_path = type_folder / raw_output_filename
                        
                        async with aiofiles.open(raw_output_path, 'w') as f:
                            await f.write(structured_json)
                            
                        logging.warning(f"Saved raw API response to {raw_output_path}")
                        return {"success": False, "error": "Failed to parse JSON", "file": str(pdf_path)}
                        
                except Exception as e:
                    pbar.update(100)  # Ensure bar completes on error
                    logging.error(f"Error processing {pdf_path}: {str(e)}")
                    return {"success": False, "error": str(e), "file": str(pdf_path)}
    except FileNotFoundError:
        logging.error(f"File not found: {pdf_path}")
        return {"success": False, "error": "File not found", "file": str(pdf_path)}
    except Exception as e:
        logging.error(f"Error opening file {pdf_path}: {str(e)}")
        return {"success": False, "error": f"File access error: {str(e)}", "file": str(pdf_path)}

async def process_batch_async(batch: List[Path], client: AsyncOpenAI, 
                            output_folder: Path, templates_created: Dict[str, bool]) -> List[Dict[str, Any]]:
    """
    Process a batch of PDF files asynchronously.
    """
    tasks = []
    start_time = time.time()
    semaphore = asyncio.Semaphore(5)  # Limit concurrent operations
    
    # Initialize processor once for the batch
    processor = DrawingProcessor()
    
    async def bounded_process(pdf_file: Path) -> Dict[str, Any]:
        async with semaphore:
            drawing_type = get_drawing_type(pdf_file)
            return await process_pdf_async(
                pdf_file, 
                client, 
                output_folder, 
                drawing_type, 
                templates_created,
                processor  # Pass the shared processor instance
            )

    # Create tasks with bounded concurrency
    tasks = [bounded_process(pdf_file) for pdf_file in batch]
    
    # Process with existing rate limiting
    results = []
    for task in asyncio.as_completed(tasks):
        result = await task
        results.append(result)
        
        # Your existing rate limiting logic
        if len(results) % API_RATE_LIMIT == 0:
            elapsed = time.time() - start_time
            if elapsed < TIME_WINDOW:
                await asyncio.sleep(TIME_WINDOW - elapsed)
            start_time = time.time()
    
    return results

async def process_job_site_async(job_folder: Path, output_folder: Path) -> None:
    output_folder.mkdir(parents=True, exist_ok=True)
        
    pdf_files = [
        path for path in job_folder.rglob('*.pdf')
    ]
    
    logging.info(f"Found {len(pdf_files)} PDF files in {job_folder}")
    
    if not pdf_files:
        logging.warning("No PDF files found. Please check the input folder.")
        return
        
    templates_created = {"floor_plan": False}
    total_batches = (len(pdf_files) + BATCH_SIZE - 1) // BATCH_SIZE
    client = AsyncOpenAI()
    all_results = []
    
    with tqdm(total=len(pdf_files), desc="Overall Progress") as overall_pbar:
        for i in range(0, len(pdf_files), BATCH_SIZE):
            batch = pdf_files[i:i+BATCH_SIZE]
            logging.info(f"Processing batch {i//BATCH_SIZE + 1} of {total_batches}")
            batch_results = await process_batch_async(batch, client, output_folder, templates_created)
            all_results.extend(batch_results)
            
            successes = [r for r in batch_results if r['success']]
            failures = [r for r in batch_results if not r['success']]
            overall_pbar.update(len(batch))
            
            logging.info(f"Batch completed. Successes: {len(successes)}, Failures: {len(failures)}")
            for failure in failures:
                logging.error(f"Failed to process {failure['file']}: {failure['error']}")
    
    successes = [r for r in all_results if r['success']]
    failures = [r for r in all_results if not r['success']]
    logging.info(f"Processing complete. Total successes: {len(successes)}, Total failures: {len(failures)}")
    
    if failures:
        logging.warning("Failures:")
        for failure in failures:
            logging.warning(f" {failure['file']}: {failure['error']}")

def verify_azure_credentials() -> bool:
    """
    Verify that Azure credentials are properly configured.
    
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    required_vars = {
        "DOCUMENTINTELLIGENCE_ENDPOINT": os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT"),
        "DOCUMENTINTELLIGENCE_API_KEY": os.getenv("DOCUMENTINTELLIGENCE_API_KEY"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_KEY": os.getenv("AZURE_OPENAI_KEY")
    }
    
    missing_vars = [key for key, value in required_vars.items() if not value]
    
    if missing_vars:
        logging.error("Missing required Azure credentials:")
        for var in missing_vars:
            logging.error(f"  {var} not found in environment variables")
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_folder> [output_folder]")
        sys.exit(1)
        
    job_folder = Path(sys.argv[1])
    output_folder = Path(sys.argv[2]) if len(sys.argv) > 2 else job_folder / "output"
    
    if not job_folder.exists():
        print(f"Error: Input folder '{job_folder}' does not exist.")
        sys.exit(1)
        
    setup_logging(output_folder)
    
    if not verify_azure_credentials():
        sys.exit(1)
        
    logging.info(f"Processing files from: {job_folder}")
    logging.info(f"Output will be saved to: {output_folder}")
    
    asyncio.run(process_job_site_async(job_folder, output_folder))


================================================
File: pyrightconfig.json
================================================
{
    "include": ["."],
    "exclude": ["**/node_modules", "**/__pycache__"],
    "ignore": [],
    "defineConstant": {},
    "venvPath": ".",
    "venv": "venv",
    "reportMissingImports": false,
    "reportMissingModuleSource": false,
    "pythonVersion": "3.11",
    "pythonPlatform": "Darwin"
}

================================================
File: requirements.txt
================================================
aiofiles==24.1.0
aiohappyeyeballs==2.4.1
aiohttp==3.10.6
aiosignal==1.3.1
annotated-types==0.7.0
anyio==4.6.0
attrs==24.2.0
azure-ai-documentintelligence==1.0.0
azure-common==1.1.28
azure-core==1.32.0
azure-identity==1.19.0
certifi==2024.8.30
cffi==1.17.1
charset-normalizer==3.3.2
cryptography==43.0.1
distro==1.9.0
frozenlist==1.4.1
h11==0.14.0
httpcore==1.0.5
httpx==0.27.2
idna==3.10
jiter==0.5.0
multidict==6.1.0
openai==1.55.0
pdfminer.six==20231228
pdfplumber==0.11.4
pillow==10.4.0
pycparser==2.22
pydantic==2.9.2
pydantic_core==2.23.4
PyMuPDF==1.24.11
pypdfium2==4.30.0
python-dotenv==1.0.1
requests==2.32.3
sniffio==1.3.1
tqdm==4.66.5
typing_extensions==4.12.2
urllib3==2.2.3
Wand==0.6.13
yarl==1.12.1


================================================
File: upgrade.md
================================================
# Implementation Guide: Azure Document Intelligence Integration

## Step 1: Update Requirements
Add to `requirements.txt`:
```txt
azure-ai-documentintelligence==1.0.0b4
azure-identity
aiofiles
pymupdf
tqdm
python-dotenv
```

## Step 2: Create New Files

### 1. Create `utils/document_processor.py`:
This is your base processor class handling authentication and basic setup.
```python
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.identity import DefaultAzureCredential
from typing import Optional
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        if not self.endpoint:
            raise ValueError("Azure Document Intelligence endpoint not provided")
            
        try:
            self.credential = DefaultAzureCredential()
            logger.info("Using DefaultAzureCredential for authentication")
            self.client = DocumentIntelligenceClient(
                endpoint=self.endpoint, 
                credential=self.credential
            )
        except Exception as e:
            logger.warning(f"DefaultAzureCredential failed: {e}. Falling back to API key")
            key = key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
            if not key:
                raise ValueError("Neither DefaultAzureCredential nor API key available")
            self.credential = AzureKeyCredential(key)
            self.client = DocumentIntelligenceClient(
                endpoint=self.endpoint, 
                credential=self.credential
            )
```

### 2. Create `utils/drawing_processor.py`:
This handles the specific drawing processing functionality.
```python
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections.abc import AsyncIterator
import asyncio
import aiofiles
import logging
from tqdm.asyncio import tqdm_asyncio
from .document_processor import DocumentProcessor

logger = logging.getLogger(__name__)

class DrawingProcessor(DocumentProcessor):
    async def process_drawing(self, file_path: str | Path) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Drawing file not found: {path}")
            
        file_size = path.stat().st_size
        if file_size > 50_000_000:  # 50MB limit
            return await self.process_large_drawing(path)

        try:
            async with aiofiles.open(path, mode='rb') as file:
                content = await file.read()
                
            return await self._process_with_azure(content)
        except Exception as e:
            logger.exception(f"Azure processing failed for {path}")
            return await self._fallback_to_pymupdf(path)

    async def _process_with_azure(self, content: bytes) -> Dict[str, Any]:
        async with self.client:
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

    async def process_batch(
        self, 
        file_paths: List[str | Path]
    ) -> Dict[str, Dict[str, Any]]:
        tasks = [self.process_drawing(path) for path in file_paths]
        results: Dict[str, Dict[str, Any]] = {}
        
        async for result in tqdm_asyncio.gather(*tasks, desc="Processing drawings"):
            try:
                results[str(path)] = result
            except Exception as e:
                logger.exception(f"Failed to process {path}")
                results[str(path)] = {"error": str(e)}
                
        return results
```

## Step 3: Update Existing Files

### 1. Update `utils/pdf_processor.py`:
```python
from typing import Dict, Any
import pymupdf  # Updated from 'fitz'
import logging
from .drawing_processor import DrawingProcessor

logger = logging.getLogger(__name__)

async def process_pdf(file_path: str) -> Dict[str, Any]:
    """Process PDF using Azure Document Intelligence with PyMuPDF fallback"""
    try:
        processor = DrawingProcessor()
        return await processor.process_drawing(file_path)
    except Exception as e:
        logger.error(f"Failed to process PDF {file_path}: {str(e)}")
        raise
```

### 2. Update `config/settings.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Azure Document Intelligence Settings
DOCUMENTINTELLIGENCE_ENDPOINT = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
DOCUMENTINTELLIGENCE_KEY = os.getenv("DOCUMENTINTELLIGENCE_KEY")

# Processing Settings
MAX_FILE_SIZE = 50_000_000  # 50MB
SUPPORTED_FILE_TYPES = [".pdf"]
```

## Step 4: Azure Setup

### Environment Variables
Add to your `.env` file:
```plaintext
# Azure Document Intelligence
DOCUMENTINTELLIGENCE_ENDPOINT=https://<your-resource-name>.cognitiveservices.azure.com/
DOCUMENTINTELLIGENCE_KEY=<your-api-key>

# Existing settings...
OPENAI_API_KEY=your_openai_key_here
```

### Setup Steps
1. Create Azure Document Intelligence resource in Azure Portal
2. Copy endpoint and key to `.env` file
3. Ensure your Azure subscription has necessary permissions

## Step 5: Test Implementation 
Create `tests/test_processor.py`

```python
import asyncio
import os
from utils.drawing_processor import DrawingProcessor

async def test_processing():
    processor = DrawingProcessor()
    
    # Test single file
    result = await processor.process_drawing("path/to/test.pdf")
    print(f"Tables found: {len(result['tables'])}")
    print(f"Text blocks found: {len(result['text_blocks'])}")
    
    # Test batch processing
    files = ["file1.pdf", "file2.pdf"]
    results = await processor.process_batch(files)
    for file, result in results.items():
        if "error" in result:
            print(f"Error processing {file}: {result['error']}")
        else:
            print(f"Processed {file}:")
            print(f"- Tables found: {len(result.get('tables', []))}")
            print(f"- Text blocks found: {len(result.get('text_blocks', []))}")
            if result.get('metadata'):
                print(f"- Pages: {result['metadata'].get('page_count')}")
                print(f"- Languages detected: {result['metadata'].get('languages', ['unknown'])}")

async def run_tests():
    """Run a complete test suite"""
    # Test valid file
    await test_processing()
    
    # Test non-existent file
    try:
        processor = DrawingProcessor()
        await processor.process_drawing("nonexistent.pdf")
    except FileNotFoundError as e:
        print(f"Successfully caught file not found: {e}")
    
    # Test batch processing with mixed valid/invalid files
    mixed_files = ["valid.pdf", "nonexistent.pdf", "another_valid.pdf"]
    processor = DrawingProcessor()
    results = await processor.process_batch(mixed_files)
    print("\nBatch processing results:")
    for file, result in results.items():
        print(f"{file}: {'Success' if 'error' not in result else f'Error - {result['error']}'}")

if __name__ == "__main__":
    asyncio.run(run_tests())
```

## Step 6: Usage in Main Application

Update `main.py`:
```python
# Standard library imports
import os
import json
import sys
import asyncio
import random
import time
import logging
from datetime import datetime
from typing import Dict, List, Any

# Third-party imports
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm

# Local application imports
from templates.room_templates import process_architectural_drawing
from utils.pdf_processor import extract_text_and_tables_from_pdf
from utils.drawing_processor import process_drawing
from utils.document_processor import DocumentProcessor

# Suppress pdfminer debug output
logging.getLogger('pdfminer').setLevel(logging.ERROR)

# Constants
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
API_RATE_LIMIT = 60  # Adjust if needed
TIME_WINDOW = 60  # Time window to respect the rate limit
BATCH_SIZE = 10  # Batch size for processing

async def process_drawings(file_paths: List[str]) -> Dict[str, Any]:
    """Process multiple PDF drawings asynchronously."""
    processor = DrawingProcessor()
    results = await processor.process_batch(file_paths)
    
    for path, result in results.items():
        if "error" in result:
            logger.error(f"Error processing {path}: {result['error']}")
            continue
            
        logger.info(f"Processed {path}:")
        logger.info(f"Found {len(result['tables'])} tables")
        logger.info(f"Found {len(result['text_blocks'])} text blocks")
    
    return results

if __name__ == "__main__":
    files = ["drawing1.pdf", "drawing2.pdf"]
    asyncio.run(process_drawings(files))
```

## Final Steps and Verification

### 1. Install Updated Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Azure Setup
- Log into Azure Portal
- Confirm Document Intelligence resource is active
- Verify endpoint and key in `.env` are correct
- Check subscription has required permissions

### 3. Run Test Script
```bash
python -m tests.test_processor
```

### 4. Monitor Logs
- Check for authentication errors
- Verify processing successful
- Confirm data extraction working as expected

## Error Handling

Common issues and solutions:

### 1. Authentication Errors
```python
ValueError: Neither DefaultAzureCredential nor API key available
```
- Solution: Check `.env` file has correct credentials

### 2. Processing Errors
```python
DocumentProcessingError: Azure processing failed
```
- Solution: Verify file is valid PDF and under size limit

### 3. Import Errors
```python
ImportError: No module named 'azure.ai.documentintelligence'
```
- Solution: Verify all dependencies installed correctly

## Best Practices

### 1. Memory Management
- Use batch processing for multiple files
- Process large files in chunks
- Clean up resources after processing

### 2. Error Handling
- Implement graceful fallback to PyMuPDF
- Log all errors with context
- Use custom exceptions for clarity

### 3. Performance
- Use async/await for I/O operations
- Implement progress tracking for batch operations
- Configure appropriate timeouts

### 4. Security
- Never commit `.env` file
- Use Azure managed identities when possible
- Implement proper access controls

## Need Help?

If you encounter issues:
1. Check Azure Portal for service status
2. Verify all environment variables
3. Review logs for specific error messages
4. Ensure PDF files are valid and readable


================================================
File: v1-workflow.md
================================================
Below is the **Generic Workflow Template** populated with details from your **btcelectrician-ohmni_oracle_v2** code snapshot. Each section maps to the files, functions, and flow shown in the repository.

---

# **Customized Workflow for btcelectrician-ohmni_oracle_v2**

## 1. Data Flow Diagram
**General Workflow:**
1. **Input Data:** 
   - **Sources**: PDF files (e.g., architectural, electrical, mechanical drawings).
   - **Location**: Retrieved from a specified `job_folder` path.

2. **Data Validation:** 
   - **Checking**: Verifies file existence, size (under 50 MB), and occasionally checks for recognized drawing types (e.g., panel schedules).
   - **Modules**: 
     - `main.py` (initial checks)  
     - `file_utils.py` (`is_panel_schedule_file`, path checks)

3. **Data Transformation:** 
   - **Process**: Azure Document Intelligence or PyMuPDF text extraction.
   - **Modules**:
     - `drawing_processor.py` (Azure-based analysis & fallback)
     - `pdf_processor.py` (PyMuPDF text/table extraction)

4. **Processing Pipelines:** 
   - **OpenAI/GPT Processing**: Takes extracted text/tables and structures it into JSON.
   - **Modules**: 
     - `drawing_processor.py` (GPT prompting for structured JSON)
     - `pdf_processor.py` (Panel schedule GPT logic)

5. **Output Generation:** 
   - **Format**: Structured JSON files, specialized templates (for rooms, e_rooms, a_rooms).
   - **Modules**: 
     - `room_templates.py` (applies architectural/electrical JSON templates)
     - `drawing_processor.py` (writes out structured JSON)

6. **Storage:**
   - **Location**: Output folder (job_folder + “output” or user-specified).
   - **Files**: 
     - `*_structured.json`
     - `e_rooms_details_floor_*.json`
     - `a_rooms_details_floor_*.json`

---

## 2. Component Interaction Flow

### **Main Orchestration** (`main.py`)
- **Entry Point**: 
  - Invoked via `python main.py <input_folder> [output_folder]`.
  - Calls `process_job_site_async` to coordinate the entire pipeline.
- **Task Management**:
  - Splits PDF files into batches (`BATCH_SIZE`).
  - Dispatches tasks to `process_batch_async`.
- **Error Handling**:
  - Implements logging for each step.
  - Retries on certain Azure/GPT rate-limit or API errors.
  - Logs failures for unprocessed files.

### **Processing Pipeline**

1. **Input Handling** (in `main.py` / `file_utils.py`):
   - **Example**: `pdf_files = [path for path in job_folder.rglob('*.pdf')]`
   - Checks if PDFs exist, splits them into batches.

2. **Validation** (basic checks in `main.py` + `utils/file_utils.py`):
   - **Example**: `is_panel_schedule_file(...)` 
   - File-size check in `drawing_processor.py`.

3. **Processing**:
   - **Panel Schedules** (Electrical):
     - Route to `DrawingProcessor().process_drawing(...)` with Azure Document Intelligence.
     - If that fails, fallback to `pdf_processor.extract_text_and_tables_from_pdf`.
   - **Non-Panel Drawings** (Architectural, Mechanical, etc.):
     - Directly uses PyMuPDF or partial Azure parsing, followed by GPT structuring in `drawing_processor.py`.

4. **Output Preparation**:
   - **In-Code**: JSON creation with GPT-4o-mini or Azure + GPT combined results.
   - **Example**: `structured_json = await processor.analyze_document(raw_content, drawing_type, client)`

5. **Output Delivery**:
   - **Save**: 
     - Writes structured data to JSON in `output_folder/<DrawingType>`.
     - If architectural, calls `process_architectural_drawing` from `room_templates.py` to generate specialized “rooms” JSON files.
   - **Example**: 
     ```python
     async with aiofiles.open(output_path, 'w') as f:
         await f.write(json.dumps(parsed_json, indent=2))
     ```

---

## 3. Component Purpose Map

### **Core Components**

1. **Main Script (`main.py`):**
   - **Purpose**: Asynchronous batch PDF processing orchestrator.
   - **Key Functions**: 
     - `setup_logging(output_folder)`  
     - `process_job_site_async(job_folder, output_folder)`

2. **Drawing Processor (`utils/drawing_processor.py`):**
   - **Purpose**: Central logic for analyzing drawings via Azure Document Intelligence + GPT fallback or PyMuPDF fallback.
   - **Key Functions**: 
     - `process_drawing`: Reads file → Azure or fallback → GPT → returns structured JSON.
     - `process_batch`: Batch wrapper around `process_drawing`.

3. **Document Processor (`utils/document_processor.py`):**
   - **Purpose**: Base class sets up Azure Document Intelligence (`DocumentIntelligenceClient`).
   - **Key Methods**: 
     - `analyze_document` for single file analysis
     - `extract_text_from_result` for text extraction

### **Utility Components**

1. **PDF Processor (`utils/pdf_processor.py`):**
   - **Purpose**: Legacy or fallback text/table extraction using PyMuPDF, specialized GPT logic for panel schedules.
   - **Key Functions**: 
     - `extract_text_and_tables_from_pdf(pdf_path)`
     - `structure_panel_data(client, raw_content)`

2. **File Utilities (`utils/file_utils.py`):**
   - **Purpose**: File scanning, type detection, path utilities.
   - **Key Functions**:
     - `traverse_job_folder(job_folder)`
     - `is_panel_schedule_file(file_path)`

3. **Configuration Files (`config/settings.py`):**
   - **Purpose**: Environment variables, API keys, and global constants (e.g., `DI_ENDPOINT`, `DI_KEY`).

4. **PDF Utilities (`utils/pdf_utils.py`):**
   - **Purpose**: Additional PDF operations with pdfplumber (extracting metadata, images).

### **Templates**
- **Input Templates**: 
  - Not explicitly used for input, but we have typed detection logic for panel schedules, architectural vs. electrical, etc.
- **Output Templates**:
  - `templates/a_rooms_template.json`, `templates/e_rooms_template.json` define JSON structure for architectural/electrical rooms.
  - `room_templates.py` loads and merges the parsed data into final structured JSON.

---

## 4. Data Transformations

1. **Input Data → Validated Data:**
   - **Input**: Raw PDF files from a job folder.
   - **Process**: Check file existence, size limit (50 MB), panel schedule detection.

2. **Validated Data → Processed Data:**
   - **Input**: Verified PDF data.
   - **Process**: 
     1. Azure Document Intelligence (`document_processor.py` / `drawing_processor.py`).
     2. Or PyMuPDF fallback (`pdf_processor.py`).
   - **Output**: Extracted text, tables, or partial structured data.

3. **Processed Data → Output Data:**
   - **Input**: Raw text/tables + recognized drawing type.
   - **Process**: GPT-4o-mini prompts in `drawing_processor.py` or `pdf_processor.py` → Creates structured JSON.
   - **Output**: 
     - `_structured.json` files
     - Additional specialized JSON (e.g., for rooms).

4. **Output Data → Storage:**
   - **Input**: Final JSON.
   - **Process**: Saved in `output_folder/drawing_type/filename.json`, plus optional “rooms” JSON from `room_templates.py`.
   - **Destination**: Local filesystem under the specified output folder.

---

## 5. Processing Triggers

1. **Input Detection:** 
   - Triggered when user runs `python main.py <job_folder>`, scanning for `*.pdf`.

2. **Validation Trigger:** 
   - Once files are found, they’re size-checked, and optionally recognized as panel schedule vs. not.

3. **Processing Trigger:**
   - For each PDF, the system calls Azure Document Intelligence or fallback logic.  
   - GPT structuring is invoked after text extraction.

4. **Output Trigger:**
   - After GPT returns structured data, the code writes JSON to output directories.  
   - If architectural: merges data with `a_rooms_template.json` and `e_rooms_template.json`.

---

## 6. Notes and Best Practices

1. **Error Handling:**
   - Logs everything (using `logging`).
   - Retries on Azure rate-limits with exponential backoff (`async_safe_api_call` in `main.py`).
   - Fallback to PyMuPDF on Azure failures for certain doc types (panel schedules).

2. **Modularity:**
   - Distinct modules: 
     - `document_processor.py` (Azure logic)
     - `drawing_processor.py` (combines Azure + GPT)
     - `pdf_processor.py` (PyMuPDF fallback + GPT).
   - `room_templates.py` handles specialized final transformations.

3. **Scalability:**
   - Batch size control in `main.py` (`BATCH_SIZE`).
   - Async-based code for I/O concurrency (`asyncio`, `aiofiles`).

4. **Flexibility:**
   - Additional drawing types can be added by extending `drawing_types` or `file_utils.py`.
   - GPT prompts are adjustable in `drawing_processor.py` or `pdf_processor.py`.

5. **Documentation:**
   - `README.md` describes setup, environment variables, usage.
   - `code-workflow.md` (in the repo) outlines a generic process template.
   - `git-best-practices-guide.md` covers version control standards.

---


================================================
File: .cursorrules
================================================

    You are an expert in Azure Functions development, OpenAI integration, cloud-based AI applications, and Document Intelligence, with a focus on Python, Azure services, vector databases, MongoDB API operations, and document processing.
  
    Key Principles:
    - Write concise, efficient serverless functions optimized for Azure Functions runtime
    - Prioritize scalability and performance in AI-powered applications
    - Use async/await patterns for I/O operations
    - Implement proper error handling and logging
    - Use descriptive variable names and clear documentation
    - Follow PEP 8 style guidelines for Python code

    Azure and OpenAI Integration:
    - Use Azure OpenAI services for model interactions and embeddings
    - Implement efficient token management and rate limiting
    - Handle API timeouts and retries appropriately
    - Optimize prompt engineering and completion requests
    - Cache frequently used embeddings for performance

    Document Intelligence and Processing:
    - Implement OCR capabilities for multiple document types
    - Handle PDF, images, Word, Excel, PowerPoint, and HTML files
    - Process both printed and handwritten text
    - Utilize prebuilt models for specialized document types
    - Implement layout extraction and form processing
    - Handle document batch processing efficiently
    - Create searchable PDF outputs
    - Integrate with Azure OpenAI for advanced extraction

    MongoDB API and Cosmos DB Operations:
    - Use MongoDB API for flexible document operations
    - Implement efficient CRUD operations through Cosmos DB
    - Optimize query patterns and indexing strategies
    - Use aggregation pipelines effectively
    - Handle document relationships and nested structures
    - Implement proper pagination and cursor management
    - Use bulk operations for batch processing

    Vector Search and Database Integration:
    - Use Cosmos DB with MongoDB API for primary storage
    - Implement vector search using Azure Cognitive Search
    - Create efficient indexes for vector similarity search
    - Optimize query patterns for hybrid searches
    - Use proper partitioning strategies
    - Implement efficient data modeling for vector storage

    Document Processing Features:
    - Implement high-resolution scanning capabilities
    - Handle small and dense text processing
    - Detect paragraphs, text lines, and words
    - Process multiple languages
    - Handle specialized document types (invoices, receipts, ID documents)
    - Implement fillable form management
    - Create searchable document outputs

    Azure Functions Best Practices:
    - Structure functions with clear input/output bindings
    - Use async operations for I/O-bound tasks
    - Implement proper dependency injection
    - Optimize cold starts and performance
    - Use managed identities for secure access
    - Handle database connection lifecycle properly

    Error Handling and Validation:
    - Implement comprehensive error handling strategies
    - Validate input data and document formats
    - Handle API rate limits and quotas
    - Use proper HTTP status codes
    - Implement retry patterns for transient failures
    - Handle MongoDB-specific error cases

    Performance Optimization:
    - Use connection pooling for database operations
    - Implement efficient caching strategies
    - Optimize document processing pipelines
    - Use batch operations where possible
    - Monitor and optimize resource usage
    - Implement proper indexing strategies

    Dependencies:
    - azure-functions
    - azure-openai
    - azure-cosmos
    - azure-search-documents
    - azure-ai-formrecognizer
    - azure-identity
    - pymongo
    - motor (for async MongoDB operations)
    - openai
    - python-dotenv

    Key Conventions:
    1. Begin with proper Azure service initialization
    2. Create reusable functions for common operations
    3. Document configuration requirements and assumptions
    4. Use version control and proper CI/CD practices
    5. Implement proper connection string management
    6. Follow best practices for document processing
    7. Implement efficient document storage strategies

    Refer to the official documentation of Azure Functions, Azure OpenAI Services, Azure Cosmos DB, MongoDB API, and Azure Document Intelligence for best practices and up-to-date APIs.

================================================
File: config/settings.py
================================================
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Azure Document Intelligence Settings
DOCUMENTINTELLIGENCE_ENDPOINT = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
DOCUMENTINTELLIGENCE_KEY = os.getenv("DOCUMENTINTELLIGENCE_API_KEY")

# Processing Settings
MAX_FILE_SIZE = 50_000_000  # 50MB
SUPPORTED_FILE_TYPES = [".pdf"]

PANEL_SCHEDULE_PATTERNS = [
    "-PANEL-SCHEDULES-",
    "-ELECTRICAL-SCHEDULES-"
]

================================================
File: documents/lessonslearned.md
================================================
# Lessons Learned: Modularizing Your Python Project

## Overview
When building larger Python projects, it's essential to keep your code modular. This means separating your code into distinct files and folders, each dedicated to a specific purpose. Doing so ensures that your application remains clear, maintainable, and easy to expand. Below is a concise summary of refactoring opportunities and common categories you might use when organizing your Python application.

---

## 1. Refactoring Opportunities in `main.py`

1. **Logging Setup**  
   - **Category**: Utility Function  
   - **Purpose**: Configure and initialize logging.  
   - **Suggestion**: Move the `setup_logging` function to something like `utils/logging_utils.py`.

2. **Drawing Type Detection**  
   - **Category**: Utility Function  
   - **Purpose**: Encapsulate logic to determine the type of a drawing (e.g., based on filename).  
   - **Suggestion**: Put the `get_drawing_type` function in `utils/drawing_utils.py`.

3. **API Call Handling**  
   - **Category**: Utility Function  
   - **Purpose**: Manage safe API calls with retry or error handling.  
   - **Suggestion**: Extract the `async_safe_api_call` function to `utils/api_utils.py`.

4. **Batch Processing Logic**  
   - **Category**: Processing Logic / Business Logic  
   - **Purpose**: Handle processing of files in batches.  
   - **Suggestion**: Move `process_batch_async` into a dedicated module (e.g., `processing/batch_processor.py`).

5. **File Processing Logic**  
   - **Category**: Processing Logic / Business Logic  
   - **Purpose**: Handle logic for processing individual files (like PDFs).  
   - **Suggestion**: Place `process_pdf_async` into `processing/file_processor.py`.

---

## 2. Common Python Categories

Below are common categories (or “layers”) you might see in Python applications. Not all projects will need every category, but they can serve as guidelines:

1. **Utility Functions**  
   - **Role**: Provide stateless helpers (e.g., formatting, validation).
   - **Example**: `utils/file_utils.py`, `utils/string_utils.py`

2. **Business Logic / Processing Logic**  
   - **Role**: Encapsulate the core rules and operations of your application.
   - **Example**: `core/processing/batch_processor.py`

3. **Data Access Layer (DAL)**  
   - **Role**: Handle interactions with databases or data sources.
   - **Example**: `data_access/db_queries.py`

4. **Service Layer**  
   - **Role**: Coordinate between business logic and data access layers (often used in larger applications).
   - **Example**: `services/user_service.py`

5. **Presentation Layer**  
   - **Role**: Manage user-facing components (like web views or GUIs).
   - **Example**: `views/home_view.py` (in a web framework)

6. **Configuration**  
   - **Role**: Store app settings, constants, or environment variables.
   - **Example**: `config/settings.py`

7. **Error Handling**  
   - **Role**: Centralize exception handling and logging.
   - **Example**: `errors/exceptions.py`

8. **Testing**  
   - **Role**: Validate your code’s correctness through automated tests.
   - **Example**: `tests/test_batch_processor.py`

9. **Security**  
   - **Role**: Handle authentication, authorization, and data protection.
   - **Example**: `security/auth_middleware.py`

10. **Middleware** (mostly in web frameworks)  
    - **Role**: Process requests/responses in a pipeline before/after main logic.
    - **Example**: `middleware/request_logger.py`

11. **Plugins/Extensions**  
    - **Role**: Extend functionality without modifying the core codebase.
    - **Example**: `extensions/custom_logging.py`

12. **Domain Models**  
    - **Role**: Represent entities and their relationships in your domain.
    - **Example**: `models/user.py`

---

## 3. Role of `main.py` (or `app.py`)

Your `main.py` typically serves as the **entry point** and **orchestrator** for the application:

1. **Orchestration**  
   - High-level logic that defines the overall flow: setting up logging, configuring dependencies, and calling the key functions.  
   - Example:
     ```python
     if __name__ == "__main__":
         setup_logging()
         process_batch_async("some_folder")
     ```

2. **Entry Point**  
   - Contains the `if __name__ == "__main__":` guard, ensuring certain code only runs when executed directly.

3. **Integration**  
   - Coordinates modules and components, “pulling them in” via imports.  
   - Example:
     ```python
     from utils.logging_utils import setup_logging
     from processing.batch_processor import process_batch_async
     ```

### Why Call It an “Orchestrator”?
- Because `main.py` (or `app.py`) is responsible for **coordinating** various parts of your application rather than doing all the work itself. This separation of concerns keeps the file clean and maintainable.

---

## 4. Benefits of This Structure

- **Readability**: Each file/module focuses on one purpose, making it easier to understand.
- **Reusability**: Common tasks (like logging, API calls) are extracted to utilities and can be reused.
- **Maintainability**: When changes are needed, you update just one module instead of combing through a huge file.
- **Scalability**: As your project grows, you can easily add new modules or services without overburdening `main.py`.

---

## 5. Key Takeaways

- **Refactor** repetitive or utility logic out of `main.py` to keep it concise.  
- **Organize** your code into logical categories (utilities, business logic, data access, etc.).  
- **Use** a central orchestrator (`main.py`) to tie everything together.  

By applying these practices, you’ll ensure your project is structured, clear, and easy to maintain as it evolves.


================================================
File: documents/proj-work-flow.md
================================================
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



================================================
File: templates/a_rooms_template.json
================================================
{
    "room_id": "",
    "room_name": "",
    "walls": {
      "north": "",
      "south": "",
      "east": "",
      "west": ""
    },
    "ceiling_height": "",
    "dimensions": ""
  }

================================================
File: templates/e_rooms_template.json
================================================
{
  "room_id": "",
  "room_name": "",
  "circuits": {
    "lighting": [],
    "power": []
  },
  "light_fixtures": {
    "fixture_ids": [],
    "fixture_count": {}
  },
  "outlets": {
    "regular_outlets": 0,
    "controlled_outlets": 0
  },
  "data": 0,
  "floor_boxes": 0,
  "mechanical_equipment": [],
  "switches": {
    "type": "",
    "model": "",
    "dimming": ""
  }
}

================================================
File: templates/room_templates.py
================================================
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

================================================
File: tests/__init__.py
================================================
# Empty file to make the tests directory a Python package 

================================================
File: tests/test-command.md
================================================
python -m tests.test_processor

================================================
File: tests/test_drawing_processor_fix.py
================================================
# /tests/test_drawing_processor_fix.py

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any
from utils.drawing_processor import DrawingProcessor
from utils.common_utils import is_panel_schedule_file
from openai import AsyncOpenAI
import json
import os
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def test_single_file(file_path: Path, drawing_type: str) -> Dict[str, Any]:
    """
    Test processing of a single file.
    """
    try:
        processor = DrawingProcessor()
        client = AsyncOpenAI()
        
        logger.info(f"Testing file: {file_path}")
        logger.info(f"Drawing type: {drawing_type}")
        
        if is_panel_schedule_file(str(file_path)):
            logger.info("Panel schedule detected, using Document Intelligence")
            result = await processor.process_drawing(str(file_path))
            logger.info("Azure Document Intelligence processing successful")
        else:
            logger.info("Using PyMuPDF for processing")
            result = await processor.process_drawing(str(file_path))
            logger.info("PyMuPDF processing successful")
        
        # Test GPT processing
        structured_json = await processor.analyze_document(str(result), drawing_type, client)
        logger.info("GPT processing successful")
        
        # Try parsing the JSON to verify it's valid
        parsed_json = json.loads(structured_json)
        logger.info("JSON parsing successful")
        
        # Save the results for inspection
        output_dir = Path("test_outputs")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{file_path.stem}_test_result.json"
        with open(output_file, "w") as f:
            json.dump(parsed_json, f, indent=2)
        logger.info(f"Results saved to: {output_file}")
        
        return {
            "success": True,
            "result": parsed_json
        }
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

async def run_tests():
    """
    Run the test suite.
    """
    base_path = Path("/Users/collin/Desktop/ElecShuffleTest")
    test_files = [
        {
            "path": base_path / "Electrical/E5.00-PANEL-SCHEDULES-Rev.3 copy.pdf",
            "type": "Electrical"
        },
        {
            "path": base_path / "Architectural/A2.2-DIMENSION-FLOOR-PLAN-Rev.3.pdf",
            "type": "Architectural"
        }
    ]
    
    results = []
    for test_file in test_files:
        if not test_file["path"].exists():
            logger.warning(f"Test file not found: {test_file['path']}")
            continue
            
        result = await test_single_file(test_file["path"], test_file["type"])
        results.append({
            "file": str(test_file["path"]),
            "result": result
        })
    
    # Print results
    print("\nTest Results:")
    print("============")
    for result in results:
        print(f"\nFile: {result['file']}")
        if result['result']['success']:
            print("Status: Success")
            print("Processed data available in test_outputs directory")
        else:
            print("Status: Failed")
            print(f"Error: {result['result']['error']}")

def verify_environment():
    """Verify all required environment variables are set"""
    required_vars = [
        "DOCUMENTINTELLIGENCE_ENDPOINT",
        "DOCUMENTINTELLIGENCE_API_KEY",
        "OPENAI_API_KEY"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

if __name__ == "__main__":
    try:
        verify_environment()
        asyncio.run(run_tests())
    except Exception as e:
        logger.error(f"Test suite failed: {str(e)}")

================================================
File: tests/test_processor.py
================================================
import asyncio
from pathlib import Path
from utils.drawing_processor import DrawingProcessor

async def test_processing():
    processor = DrawingProcessor()
    
    # Test single file
    test_pdf = Path("path/to/test.pdf")
    result = await processor.process_drawing(test_pdf)
    print(f"Tables found: {len(result['tables'])}")
    print(f"Text blocks found: {len(result['text_blocks'])}")
    
    # Test batch processing
    files = [Path("file1.pdf"), Path("file2.pdf")]
    results = await processor.process_batch(files)
    for file, result in results.items():
        if "error" in result:
            print(f"Error processing {file}: {result['error']}")
        else:
            print(f"Processed {file}:")
            print(f"- Tables found: {len(result.get('tables', []))}")
            print(f"- Text blocks found: {len(result.get('text_blocks', []))}")
            if result.get('metadata'):
                print(f"- Pages: {result['metadata'].get('page_count')}")
                print(f"- Languages detected: {result['metadata'].get('languages', ['unknown'])}")

async def run_tests():
    """Run a complete test suite"""
    # Test valid file
    await test_processing()
    
    # Test non-existent file
    try:
        processor = DrawingProcessor()
        await processor.process_drawing(Path("nonexistent.pdf"))
    except FileNotFoundError as e:
        print(f"Successfully caught file not found: {e}")
    
    # Test batch processing with mixed valid/invalid files
    mixed_files = [
        Path("valid.pdf"),
        Path("nonexistent.pdf"),
        Path("another_valid.pdf")
    ]
    processor = DrawingProcessor()
    results = await processor.process_batch(mixed_files)
    print("\nBatch processing results:")
    for file, result in results.items():
        print(f"{file}: {'Success' if 'error' not in result else f'Error - {result['error']}'}")

if __name__ == "__main__":
    asyncio.run(run_tests()) 

================================================
File: utils/common_utils.py
================================================
import re
from pathlib import Path

def is_panel_schedule_file(file_path: str) -> bool:
    """
    Check if a file is likely a panel schedule based on its name.
    """
    file_name = Path(file_path).stem.lower()
    panel_keywords = ['panel', 'schedule', 'pnl', 'sch']
    return any(keyword in file_name for keyword in panel_keywords)

================================================
File: utils/document_processor.py
================================================
# Standard library imports
import os
import logging
from typing import Optional, Any, Dict
from pathlib import Path
import aiofiles
from dotenv import load_dotenv

# Azure imports
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest

# Update these variable names
DOCUMENTINTELLIGENCE_ENDPOINT = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
DOCUMENTINTELLIGENCE_KEY = os.getenv("DOCUMENTINTELLIGENCE_API_KEY")

# Processing Settings
MAX_FILE_SIZE = 50_000_000  # 50MB
SUPPORTED_FILE_TYPES = [".pdf"]

def verify_azure_credentials() -> bool:
    """Verify that Azure credentials are properly configured."""
    endpoint = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
    key = os.getenv("DOCUMENTINTELLIGENCE_API_KEY")
    
    if not endpoint or not key:
        logging.error("Azure credentials not found. Please check your .env file contains:")
        logging.error("DOCUMENTINTELLIGENCE_ENDPOINT=your_azure_endpoint")
        logging.error("DOCUMENTINTELLIGENCE_API_KEY=your_azure_key")
        return False
    return True

class DocumentProcessor:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
        if not self.endpoint:
            raise ValueError("Document Intelligence endpoint not provided")
            
        key = key or os.getenv("DOCUMENTINTELLIGENCE_API_KEY")
        if not key:
            raise ValueError("Document Intelligence API key not provided")
        
        self.credential = AzureKeyCredential(key)
        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint, 
            credential=self.credential,
            api_version="2024-02-29-preview"  # Added API version specification
        )

    async def analyze_document(self, file_path: Path) -> AnalyzeResult:
        """
        Analyzes a document using Azure Document Intelligence.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            AnalyzeResult: The analysis results from Azure Document Intelligence
            
        Raises:
            ValueError: If file doesn't exist or is empty
            Exception: For other processing errors
        """
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")
            
        try:
            async with aiofiles.open(file_path, "rb") as file:
                document_content = await file.read()
                if not document_content:
                    raise ValueError(f"Empty file: {file_path}")
                
                # Start the analysis
                poller = await self.client.begin_analyze_document(
                    "prebuilt-document",
                    document_content
                )
                
                # Get the result
                result = await poller.result()
                logging.info(f"Successfully analyzed document: {file_path}")
                return result
                
        except Exception as e:
            logging.error(f"Error analyzing document {file_path}: {str(e)}")
            raise

    async def extract_text_from_result(self, result: AnalyzeResult) -> str:
        """
        Extracts text content from analysis result.
        
        Args:
            result: The AnalyzeResult from document analysis
            
        Returns:
            str: Extracted text content
        """
        try:
            content = []
            for page in result.pages:
                for line in page.lines:
                    content.append(line.content)
            return "\n".join(content)
            
        except Exception as e:
            logging.error(f"Error extracting text from result: {str(e)}")
            raise

    async def process_document(self, file_path: Path) -> Dict[str, Any]:
        """
        Complete document processing pipeline.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dict containing processed results
        """
        try:
            # Analyze document
            result = await self.analyze_document(file_path)
            
            # Extract text
            text_content = await self.extract_text_from_result(result)
            
            # Extract tables if present
            tables = []
            if hasattr(result, 'tables'):
                for table in result.tables:
                    table_data = []
                    for cell in table.cells:
                        table_data.append({
                            'row_index': cell.row_index,
                            'column_index': cell.column_index,
                            'content': cell.content,
                            'row_span': cell.row_span,
                            'column_span': cell.column_span
                        })
                    tables.append(table_data)
            
            return {
                'file_name': file_path.name,
                'text_content': text_content,
                'tables': tables,
                'page_count': len(result.pages),
                'metadata': {
                    'document_type': result.doc_type if hasattr(result, 'doc_type') else None,
                    'confidence': result.confidence if hasattr(result, 'confidence') else None
                }
            }
            
        except Exception as e:
            logging.error(f"Error processing document {file_path}: {str(e)}")
            return {
                'file_name': file_path.name,
                'error': str(e)
            }

================================================
File: utils/drawing_processor.py
================================================
from typing import List, Dict, Any, Optional
import asyncio
import aiofiles
import os
import logging
from tqdm.asyncio import tqdm_asyncio
from .document_processor import DocumentProcessor
from openai import AsyncOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
from pathlib import Path
import json

logger = logging.getLogger(__name__)

DRAWING_INSTRUCTIONS = {
    "Electrical": "Focus on panel schedules, circuit info, equipment schedules with electrical characteristics, and installation notes.",
    "Mechanical": "Capture equipment schedules, HVAC details (CFM, capacities), and installation instructions.",
    "Plumbing": "Include fixture schedules, pump details, water heater specs, pipe sizing, and system instructions.",
    "Architectural": """
    Extract and structure the following information:
    1. Room details: Create a 'rooms' array with objects for each room, including:
       - 'number': Room number (as a string)
       - 'name': Room name
       - 'finish': Ceiling finish
       - 'height': Ceiling height
    2. Room finish schedules
    3. Door/window details
    4. Wall types
    5. Architectural notes
    Ensure all rooms are captured and properly structured in the JSON output.
    """,
    "General": "Organize all relevant data into logical categories based on content type."
}

class DrawingProcessor(DocumentProcessor):
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        super().__init__(endpoint, key)
        self.openai_client = AsyncOpenAI()

    async def process_drawing(self, file_path: str) -> Dict[str, Any]:
        """Process a drawing using Azure Document Intelligence."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Drawing file not found: {file_path}")
            
        file_size = os.path.getsize(file_path)
        if file_size > 50_000_000:  # 50MB limit
            return await self.process_large_drawing(file_path)

        try:
            # Updated to use direct file handling
            with open(file_path, "rb") as f:
                return await self._process_with_azure(f)
        except Exception as e:
            logger.error(f"Azure Document Intelligence processing failed: {e}")
            return await self._fallback_to_pymupdf(file_path)

    async def _process_with_azure(self, file_obj) -> Dict[str, Any]:
        """Process document with Azure Document Intelligence."""
        try:
            # Use the documented approach
            poller = await self.client.begin_analyze_document(
                "prebuilt-layout",
                analyze_request=file_obj,
                content_type="application/octet-stream"
            )
            
            result = await poller.result()

            # Parse according to documented schema
            parsed_data = {
                "content": {},
                "tables": [],
                "text_blocks": [],
                "metadata": {}
            }

            # Extract pages content
            if hasattr(result, 'pages'):
                parsed_data["content"]["pages"] = []
                for page in result.pages:
                    page_content = {
                        "number": page.page_number if hasattr(page, 'page_number') else 0,
                        "lines": [],
                        "tables": []
                    }
                    if hasattr(page, 'lines'):
                        for line in page.lines:
                            page_content["lines"].append({
                                "text": line.content if hasattr(line, 'content') else "",
                                "spans": line.spans if hasattr(line, 'spans') else []
                            })
                    parsed_data["content"]["pages"].append(page_content)

            # Extract paragraphs
            if hasattr(result, 'paragraphs'):
                parsed_data["text_blocks"] = [
                    {
                        "text": p.content if hasattr(p, 'content') else "",
                        "role": p.role if hasattr(p, 'role') else None,
                        "spans": p.spans if hasattr(p, 'spans') else []
                    }
                    for p in result.paragraphs
                ]

            # Extract tables
            if hasattr(result, 'tables'):
                for table in result.tables:
                    table_data = {
                        "row_count": table.row_count if hasattr(table, 'row_count') else 0,
                        "column_count": table.column_count if hasattr(table, 'column_count') else 0,
                        "cells": []
                    }
                    
                    if hasattr(table, 'cells'):
                        for cell in table.cells:
                            cell_data = {
                                "text": cell.content if hasattr(cell, 'content') else "",
                                "row_index": cell.row_index if hasattr(cell, 'row_index') else 0,
                                "column_index": cell.column_index if hasattr(cell, 'column_index') else 0,
                                "row_span": cell.row_span if hasattr(cell, 'row_span') else 1,
                                "column_span": cell.column_span if hasattr(cell, 'column_span') else 1
                            }
                            table_data["cells"].append(cell_data)
                    
                    parsed_data["tables"].append(table_data)

            # Extract metadata
            parsed_data["metadata"] = {
                "languages": result.languages if hasattr(result, 'languages') else [],
                "styles": result.styles if hasattr(result, 'styles') else []
            }

            return parsed_data

        except Exception as e:
            logger.error(f"Azure processing failed: {str(e)}")
            raise

    def _parse_drawing_content(self, result: Any) -> Dict[str, Any]:
        """
        Parse the content returned from Azure Document Intelligence.
        """
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

    def _process_table(self, table: Any) -> Dict[str, Any]:
        """
        Process a table from Azure Document Intelligence result.
        """
        processed_table = {
            "rows": len(table.rows),
            "columns": len(table.columns),
            "cells": []
        }
        
        for cell in table.cells:
            processed_table["cells"].append({
                "text": cell.content,
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "row_span": cell.row_span,
                "column_span": cell.column_span
            })
        
        return processed_table

    def _is_panel_schedule(self, table: Dict[str, Any]) -> bool:
        """
        Determine if a table is an electrical panel schedule.
        """
        panel_keywords = ["circuit", "breaker", "load", "amps", "poles", "phase"]
        first_row_text = " ".join(
            cell["text"].lower() 
            for cell in table["cells"] 
            if cell["row_index"] == 0
        )
        return any(keyword in first_row_text for keyword in panel_keywords)

    async def process_batch(self, file_paths: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Process multiple drawings in batch.
        """
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

    async def analyze_document(self, raw_content: str, drawing_type: str, client: AsyncOpenAI) -> str:
        """Analyze document content using GPT."""
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
            # Ensure raw_content is a simple string
            if not isinstance(raw_content, str):
                raw_content = str(raw_content)

            # Use the correct message format for OpenAI API 1.55.0
            response = await client.chat.completions.create(
                model="gpt-4o-mini",  # Keeping your specified model
                messages=[
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": raw_content
                    }
                ],
                temperature=0.2,
                max_tokens=16000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error processing {drawing_type} drawing with GPT: {str(e)}")
            raise

    async def analyze_document_from_url(self, document_url: str, drawing_type: str) -> Dict[str, Any]:
        """
        Analyze a document from a URL using Azure Document Intelligence.
        """
        try:
            poller = await self.client.begin_analyze_document_from_url(
                "prebuilt-document",
                document_url=document_url
            )
            result = await poller.result()
            return result.to_dict()
            
        except Exception as e:
            logger.error(f"Document Intelligence analysis from URL failed: {str(e)}")
            raise

    async def _fallback_to_pymupdf(self, file_path: str) -> Dict[str, Any]:
        """
        Fallback method when Azure Document Intelligence fails.
        Uses PyMuPDF for basic text and table extraction.
        """
        from .pdf_processor import extract_text_and_tables_from_pdf
        try:
            raw_content = await extract_text_and_tables_from_pdf(file_path)
            return {
                "text_blocks": [{"content": raw_content}],
                "tables": [],
                "metadata": {
                    "processed_by": "PyMuPDF fallback",
                    "file_path": file_path
                }
            }
        except Exception as e:
            logger.error(f"PyMuPDF fallback processing failed for {file_path}: {str(e)}")
            raise

================================================
File: utils/file_utils.py
================================================
import os
import logging
from typing import List, Optional
from pathlib import Path
from config.settings import PANEL_SCHEDULE_PATTERNS
from .common_utils import is_panel_schedule_file

logger = logging.getLogger(__name__)

def get_drawing_type(file_path: str, job_folder: str) -> Optional[str]:
    """
    Determine the drawing type based on the file path and job folder.
    
    Args:
    file_path (str): The full path to the PDF file.
    job_folder (str): The root job folder path.

    Returns:
    Optional[str]: The determined drawing type, or None if it can't be determined.
    """
    relative_path = os.path.relpath(file_path, job_folder)
    path_components = relative_path.lower().split(os.sep)

    drawing_types = {
        "architectural": ["architectural", "arch", "a"],
        "electrical": ["electrical", "elec", "e"],
        "mechanical": ["mechanical", "mech", "m"],
        "plumbing": ["plumbing", "plumb", "p"],
        "structural": ["structural", "struct", "s"],
        "kitchen": ["kitchen", "kit", "k"],
        "civil": ["civil", "civ", "c"],
        "fire_protection": ["fire protection", "fire", "fp"],
        "low_voltage": ["low voltage", "low-voltage", "lv"],
        # Add more drawing types here as needed
    }

    for component in path_components:
        for drawing_type, keywords in drawing_types.items():
            if any(keyword in component for keyword in keywords):
                return drawing_type

    logger.warning(f"Could not determine drawing type for {file_path}")
    return None

def traverse_job_folder(job_folder: str) -> List[str]:
    """
    Traverse the job folder and collect all PDF files.

    Args:
    job_folder (str): The root job folder path to traverse.

    Returns:
    List[str]: A list of full file paths to all PDF files found.
    """
    pdf_files = []
    try:
        for root, _, files in os.walk(job_folder):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        logger.info(f"Found {len(pdf_files)} PDF files in {job_folder}")
    except Exception as e:
        logger.error(f"Error traversing job folder {job_folder}: {str(e)}")
    return pdf_files

def cleanup_temporary_files(output_folder: str) -> None:
    """
    Clean up any temporary files created during processing.

    Args:
    output_folder (str): The folder containing output files.
    """
    # Implement cleanup logic here if needed
    pass

def get_project_name(job_folder: str) -> str:
    """
    Extract the project name from the job folder path.

    Args:
    job_folder (str): The root job folder path.

    Returns:
    str: The project name.
    """
    return os.path.basename(job_folder)

def is_panel_schedule_file(file_path: str) -> bool:
    filename = Path(file_path).stem.upper()
    return (filename.startswith('E') and 
            any(pattern in filename for pattern in PANEL_SCHEDULE_PATTERNS))

================================================
File: utils/pdf_processor.py
================================================
import pymupdf
import json
import os
from openai import AsyncOpenAI
from typing import Dict, Any, Tuple
import logging
from .drawing_processor import DrawingProcessor
from utils.file_utils import is_panel_schedule_file

logger = logging.getLogger(__name__)

async def extract_text_and_tables_from_pdf(pdf_path: str) -> str:
    """Legacy method using PyMuPDF for basic text and table extraction"""
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
    """Process PDF using Azure Document Intelligence with PyMuPDF fallback"""
    print(f"Processing PDF: {pdf_path}")
    
    if is_panel_schedule_file(str(pdf_path)):
        try:
            processor = DrawingProcessor()
            azure_result = await processor.process_drawing(pdf_path)
            raw_content = _convert_azure_to_raw_content(azure_result)
        except Exception as e:
            logger.error(f"Document Intelligence failed for panel schedule: {str(e)}")
            raw_content = await extract_text_and_tables_from_pdf(pdf_path)
    else:
        raw_content = await extract_text_and_tables_from_pdf(pdf_path)
    
    structured_data = await structure_panel_data(client, raw_content)
    
    panel_name = structured_data.get('panel_name', 'unknown_panel').replace(" ", "_").lower()
    filename = f"{panel_name}_electric_panel.json"
    filepath = os.path.join(output_folder, filename)
    
    with open(filepath, 'w') as f:
        json.dump(structured_data, f, indent=2)
    
    print(f"Saved structured panel data: {filepath}")
    return raw_content, structured_data

def _convert_azure_to_raw_content(azure_result: Dict[str, Any]) -> str:
    """Convert Azure Document Intelligence result to raw content format"""
    content = ""
    
    # Add text blocks
    for block in azure_result.get('text_blocks', []):
        content += "TEXT:\n" + block.get('content', '') + "\n"
    
    # Add tables
    for table in azure_result.get('tables', []):
        content += "TABLE:\n"
        if isinstance(table, dict):  # Ensure table is in correct format
            rows = table.get('cells', [])
            if rows:
                content += "\n".join([" | ".join(row) for row in rows]) + "\n"
    
    return content

================================================
File: utils/pdf_utils.py
================================================
# pdf_utils.py

import pdfplumber
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

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

