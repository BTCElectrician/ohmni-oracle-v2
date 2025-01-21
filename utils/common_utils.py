import re
from pathlib import Path

def is_panel_schedule_file(file_path: str) -> bool:
    """
    Check if a file is likely a panel schedule based on its name.
    """
    file_name = Path(file_path).stem.lower()
    panel_keywords = ['panel', 'schedule', 'pnl', 'sch']
    return any(keyword in file_name for keyword in panel_keywords)