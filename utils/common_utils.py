import re
from pathlib import Path

def is_panel_schedule_file(file_path: str) -> bool:
    """
    Check if a file is likely an electrical panel schedule based on its name.
    Looks for both electrical prefix (E) and panel schedule indicators.
    """
    file_name = Path(file_path).stem.lower()
    return (
        ('e' in file_name or 'electrical' in file_name) and 
        any(keyword in file_name for keyword in ['panel', 'schedule', 'pnl', 'sch'])
    )