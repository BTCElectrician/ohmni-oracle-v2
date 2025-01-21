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