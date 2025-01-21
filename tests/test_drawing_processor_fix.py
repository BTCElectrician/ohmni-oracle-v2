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