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
from .common_utils import is_panel_schedule_file

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
            
        # Get the base directory of the input file
        base_dir = Path(file_path).parent.parent
        output_dir = base_dir / "output"
        output_dir.mkdir(exist_ok=True)
        
        file_size = os.path.getsize(file_path)
        if file_size > 50_000_000:  # 50MB limit
            return await self.process_large_drawing(file_path)

        try:
            # First check if it's a panel schedule
            if is_panel_schedule_file(str(file_path)):
                logger.info("Panel schedule detected, using Document Intelligence")
                async with aiofiles.open(file_path, "rb") as f:
                    file_content = await f.read()
                    return await self._process_with_azure(file_content)
            else:
                # For non-panel schedule drawings, use PyMuPDF directly
                logger.info("Non-panel schedule drawing, using PyMuPDF")
                return await self._fallback_to_pymupdf(file_path)
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise

    async def _process_with_azure(self, file_obj) -> Dict[str, Any]:
        """Process document with Azure Document Intelligence."""
        try:
            # Create the analyze request with the correct parameters
            poller = await self.client.begin_analyze_document(
                "prebuilt-layout",
                body={"analyze_request": file_obj},  # Add body parameter
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
                analyze_request=document_url  # Updated parameter name
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
            logger.info(f"Starting PyMuPDF extraction for: {file_path}")
            raw_content = await extract_text_and_tables_from_pdf(file_path)
            logger.info(f"PyMuPDF extraction completed. Content length: {len(str(raw_content))}")
            
            result = {
                "text_blocks": [{"content": raw_content}],
                "tables": [],
                "metadata": {
                    "processed_by": "PyMuPDF fallback",
                    "file_path": file_path
                }
            }
            logger.info("PyMuPDF result structure created successfully")
            return result
            
        except Exception as e:
            logger.error(f"PyMuPDF fallback processing failed for {file_path}: {str(e)}")
            raise