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