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
