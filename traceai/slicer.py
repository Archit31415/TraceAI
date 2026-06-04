import os
from typing import Optional

def extract_code_context(file_path: str, line_number: int, window: int = 10) -> Optional[str]:
    # Opens a source file and extracts a sliding window of code around the crashing line.

    if not file_path or not line_number:
        return None

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception:
        return None

    total_lines = len(lines)
    if total_lines == 0:
        return None

    start_index = max(0, line_number - window - 1)
    
    end_index = min(total_lines, line_number + window)

    snippet_lines = []
    
    for i in range(start_index, end_index):
        current_line_num = i + 1
        
        marker = ">> " if current_line_num == line_number else "   "
        
        raw_code = lines[i].rstrip('\n')
        
        snippet_lines.append(f"{marker}{current_line_num:4d} | {raw_code}")

    return "\n".join(snippet_lines)

# Local Testing Block
if __name__ == "__main__":
    import tempfile

    dummy_code = """import math
import sys

def initialize_system():
    print("System booting...")
    return True

def trigger_crash():
    # This line will cause a ZeroDivisionError
    value = 100 / 0
    return value

def cleanup():
    print("Shutting down.")

if __name__ == "__main__":
    initialize_system()
    trigger_crash()
    cleanup()
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix=".py", delete=False) as temp_file:
        temp_file.write(dummy_code)
        temp_file_path = temp_file.name

    print("--- Testing Context Extraction (Target: Line 10) ---")
    
    target_crash_line = 10
    
    context = extract_code_context(temp_file_path, target_crash_line, window=3)
    
    if context:
        print(context)
    else:
        print("Failed to extract context.")

    os.unlink(temp_file_path)