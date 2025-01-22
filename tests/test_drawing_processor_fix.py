# /tests/test_drawing_processor_fix.py

import sys
from pathlib import Path

# Add the root directory to the Python path before any local imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

import asyncio
import logging
from typing import Dict, Any
from utils.drawing_processor import DrawingProcessor
from utils.common_utils import is_panel_schedule_file
from openai import AsyncOpenAI
import json
import os
from dotenv import load_dotenv
import aiofiles

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log the current working directory
logger.info(f"Current working directory: {os.getcwd()}")

# Log the Python path
logger.info(f"Python path: {sys.path}")

# Log the updated Python path
logger.info(f"Updated Python path: {sys.path}")

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
            # Remove the model_id and content_type parameters
            with open(file_path, 'rb') as doc_file:
                document_bytes = doc_file.read()
                result = await processor.process_drawing(str(file_path))
            logger.info("Azure Document Intelligence processing successful")
        else:
            logger.info("Using PyMuPDF for processing")
            result = await processor.process_drawing(str(file_path))
            logger.info("PyMuPDF processing successful")
        
        # Test GPT processing
        structured_json = await processor.analyze_document(str(result), drawing_type, client)
        logger.info("GPT processing successful")
        
        # Add validation for empty responses
        if not structured_json or not structured_json.strip():
            raise ValueError("GPT response is empty")
            
        # Try parsing the JSON to verify it's valid
        try:
            # Remove the ```json and ``` markers if they exist
            json_str = structured_json
            if json_str.startswith('```json'):
                json_str = json_str.split('```json')[1]
            if json_str.endswith('```'):
                json_str = json_str.rsplit('```', 1)[0]
            json_str = json_str.strip()
            
            parsed_json = json.loads(json_str)
            logger.info("JSON parsing successful")
        except json.JSONDecodeError as je:
            logger.error(f"JSON parsing failed: {je}")
            raise
        
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

async def test_drawing_processor(base_path: str):
    """Test the DrawingProcessor class with actual files."""
    base_path = Path(base_path)
    output_dir = base_path / "output"
    output_dir.mkdir(exist_ok=True)
    
    logger.info(f"Base path: {base_path}")
    logger.info(f"Output directory: {output_dir}")
    
    processor = DrawingProcessor()
    
    # Process all PDF files in the directory structure
    for drawing_type in ["Electrical", "Architectural", "Mechanical", "Plumbing"]:
        type_dir = base_path / drawing_type
        logger.info(f"Checking directory: {type_dir}")
        
        if not type_dir.exists():
            logger.info(f"Directory does not exist: {type_dir}")
            continue
            
        for pdf_file in type_dir.glob("*.pdf"):
            logger.info(f"Processing file: {pdf_file}")
            
            try:
                # Process the file
                result = await processor._fallback_to_pymupdf(str(pdf_file))
                logger.info("PyMuPDF extraction completed")
                
                # Process with GPT
                structured_json = await processor.analyze_document(
                    result['text_blocks'][0]['content'], 
                    drawing_type,
                    processor.openai_client
                )
                logger.info("GPT processing completed")
                
                # Save the results
                output_path = output_dir / f"{pdf_file.stem}_structured.json"
                logger.info(f"Saving to: {output_path}")
                
                async with aiofiles.open(output_path, 'w') as f:
                    await f.write(structured_json)
                logger.info(f"File saved successfully: {output_path}")
                
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {str(e)}")
                raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m tests.test_drawing_processor_fix /path/to/ElecShuffleTest")
        sys.exit(1)
        
    base_path = sys.argv[1]
    asyncio.run(test_drawing_processor(base_path))