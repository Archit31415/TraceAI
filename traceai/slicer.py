import os
from typing import Optional

def extract_code_context(file_path: str, line_num: int, window: int = 10):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        start_index = max(0, line_num - window - 1)
        end_index = min(len(lines), line_num + window)
        
        context = "".join(lines[start_index:end_index])
        
        return context, start_index + 1, end_index
    except Exception:
        return None, None, None


def build_multi_file_context(locations: list[tuple[str, int]]) -> tuple[str, dict]:

    combined_context = ""
    file_bounds = {}

    for i, (path, line) in enumerate(locations):
        window = 10 if i == len(locations) - 1 else 4
        
        context_text, start, end = extract_code_context(path, line, window=window)
        
        if context_text:
            combined_context += f"\nFile: {path} (Lines {start}-{end})\n"
            combined_context += context_text
            
            if path not in file_bounds:
                file_bounds[path] = (start, end)

    return combined_context, file_bounds