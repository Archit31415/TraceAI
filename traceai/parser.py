import re
from typing import Tuple, Optional
import os

def extract_all_crash_locations(stderr: str) -> list[tuple[str, int]]:

    py_matches = re.findall(r'File "(?P<path>[^"]+)", line (?P<line>\d+)', stderr)
    node_matches = re.findall(r'at .*?\(?(?P<path>[^\s:]+\.[a-zA-Z0-9]+):(?P<line>\d+)', stderr)
    
    all_matches = py_matches + node_matches
    unique_locations = []
    seen = set()

    for path, line in all_matches:
        if any(ignore in path for ignore in ["site-packages", "node_modules", "/lib/python"]):
            continue
            
        if os.path.exists(path):
            loc = (path, int(line))
            if loc not in seen:
                unique_locations.append(loc)
                seen.add(loc)
                
    return unique_locations
