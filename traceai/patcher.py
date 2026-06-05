import difflib
import re
import click
from rich.console import Console
from rich.syntax import Syntax

console = Console()

def extract_code_block(markdown_text: str) -> str:
    """
    Finds the last markdown code block in the AI response.
    """
    matches = re.findall(r'```[a-zA-Z]*\n(.*?)```', markdown_text, re.DOTALL)
    if matches:
        return matches[-1] 
    return None

def propose_and_apply_fix(file_path: str, start_line: int, end_line: int, full_response: str):
    proposed_code = extract_code_block(full_response)
    
    if not proposed_code:
        return 

    with open(file_path, 'r') as f:
        original_lines = f.readlines()

    start_idx = max(0, start_line - 1)
    end_idx = min(len(original_lines), end_line)

    # Normalize missing trailing newlines to prevent visualization grouping anomalies
    original_lines_list = [line if line.endswith('\n') else line + '\n' for line in original_lines]

    proposed_lines_list = proposed_code.splitlines(keepends=True)
    proposed_lines_list = [line if line.endswith('\n') else line + '\n' for line in proposed_lines_list]

    # Splice the AI replacement logic into position
    new_lines = original_lines_list[:start_idx] + proposed_lines_list + original_lines_list[end_idx:]
    new_content = "".join(new_lines)

    # Compute a clean unified diff utilizing the sanitized sequences
    diff = list(difflib.unified_diff(
        original_lines_list,
        new_lines,
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
        n=3
    ))

    if not diff:
        console.print("\n[dim]No structural changes detected in the AI fix.[/dim]")
        return

    diff_text = "".join(diff)
    syntax = Syntax(diff_text, "diff", theme="monokai", background_color="default")
    
    console.print("\n[bold cyan]🛠️  Interactive Auto-Fixer[/bold cyan]")
    console.print("━" * 40)
    console.print(syntax)
    console.print()

    if click.confirm(f"Apply this fix to {file_path}?"):
        with open(file_path, 'w') as f:
            f.write(new_content)
        console.print(f"[bold green]✅ Successfully patched {file_path}[/bold green]\n")
    else:
        console.print("[dim]Fix discarded. File remains unchanged.[/dim]\n")