import subprocess
import sys
from typing import Tuple, Optional

def run_and_intercept(command: list[str]) -> Tuple[int, Optional[str]]:
    try:
        process = subprocess.Popen(
            command,
            stdout=sys.stdout,       
            stderr=subprocess.PIPE,  
            text=True                
        )
        
        _, stderr_output = process.communicate()
        
        return process.returncode, stderr_output
        
    except FileNotFoundError:
        return 1, f"Error: The command '{command[0]}' was not found on your system."
    except Exception as e:
        return 1, f"An unexpected execution error occurred: {str(e)}"

# Local Testing
if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        target_command = sys.argv[1:]
        print(f"Launching Wrapper for: {' '.join(target_command)}\n{'-'*40}")
        
        exit_code, captured_error = run_and_intercept(target_command)
                
        if exit_code == 0:
            print("Execution finished cleanly (Exit Code 0).")
            print("No errors intercepted.")
        else:
            print(f"Crash Detected! (Exit Code {exit_code})")
            print("\nINTERCEPTED STDERR")
            print(captured_error.strip() if captured_error else "No stderr output.")
    else:
        print("Please provide a command to test.")
        print("Example: python interceptor.py python -c 'print(1/0)'")