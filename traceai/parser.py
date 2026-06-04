import re
from typing import Tuple, Optional

def extract_crash_location(stderr: str) -> Tuple[Optional[str], Optional[int]]:
    
    # Scans the raw stderr string to extract the file path and line number.
    # Supports Python and Node.js traceback formats.
    
    if not stderr:
        return None, None

    # Python Parsing

    python_pattern = r'File "([^"]+)", line (\d+)'
    py_matches = re.findall(python_pattern, stderr)
    
    if py_matches:
        file_path, line_num = py_matches[-1]
        return file_path, int(line_num)

    # Node.js Parsing
    node_top_pattern = r'^([^\s]+):(\d+)'
    node_top_match = re.search(node_top_pattern, stderr, re.MULTILINE)
    
    if node_top_match:
        return node_top_match.group(1), int(node_top_match.group(2))

    node_stack_pattern = r'at .*?\((.*?):(\d+):\d+\)'
    node_matches = re.findall(node_stack_pattern, stderr)
    
    if node_matches:
        file_path, line_num = node_matches[0]
        return file_path, int(line_num)

    return None, None

# Local Testing Block
if __name__ == "__main__":
    sample_python_stderr = """
Traceback (most recent call last):
  File "/usr/local/lib/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/Users/dev/traceai/tests/broken.py", line 15, in <module>
    calculate_metrics()
  File "/Users/dev/traceai/tests/broken.py", line 12, in calculate_metrics
    return 1 / 0
ZeroDivisionError: division by zero
    """

    sample_node_stderr = """
/Users/dev/traceai/tests/server.js:4
console.log(user.name);
                 ^
TypeError: Cannot read properties of undefined (reading 'name')
    at Object.<anonymous> (/Users/dev/traceai/tests/server.js:4:18)
    at Module._compile (node:internal/modules/cjs/loader:1105:14)
    """

    print("Testing Python Parser")
    py_file, py_line = extract_crash_location(sample_python_stderr)
    print(f"File: {py_file}")
    print(f"Line: {py_line}\n")
    
    print("Testing Node.js Parser")
    node_file, node_line = extract_crash_location(sample_node_stderr)
    print(f"File: {node_file}")
    print(f"Line: {node_line}")