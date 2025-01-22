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
                
                # Correct parameters for SDK v4.0
                poller = await self.client.begin_analyze_document(
                    "prebuilt-layout",
                    analyze_request=document_content,  # This is the correct parameter name
                    content_type="application/octet-stream"
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