import os
from typing import Optional

def extract_code_context(file_path: str, line_num: int, window: int = 10):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        start_index = max(0, line_num - window - 1)
        end_index = min(len(lines), line_num + window)
        
        # We join the raw lines so the AI sees exactly what is in the file
        context = "".join(lines[start_index:end_index])
        
        # Return the context AND the 1-indexed line bounds
        return context, start_index + 1, end_index
    except Exception:
        return None, None, None
