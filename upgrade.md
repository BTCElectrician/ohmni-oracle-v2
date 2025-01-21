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
