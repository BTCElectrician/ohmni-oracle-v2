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
