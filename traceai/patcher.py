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


def propose_and_apply_fix(file_bounds: dict, full_response: str):
    proposed_code = extract_code_block(full_response)
    if not proposed_code:
        return

    proposed_lines_list = proposed_code.splitlines(keepends=True)
    first_line = proposed_lines_list[0].strip()
    match = re.match(r'^[/#*]+\s*file:\s*(.+)$', first_line, re.IGNORECASE)

    if not match:
        console.print("\n[dim]AI did not specify a target file. Manual fix required.[/dim]")
        return

    target_file = match.group(1).strip()
    if target_file not in file_bounds:
        console.print(f"\n[dim]AI suggested fixing {target_file}, but it is out of context.[/dim]")
        return

    start_line, end_line = file_bounds[target_file]
    
    proposed_lines_list = proposed_lines_list[1:]

    with open(target_file, 'r') as f:
        original_lines = f.readlines()

    start_idx = max(0, start_line - 1)
    end_idx = min(len(original_lines), end_line)

    original_lines_list = [line if line.endswith('\n') else line + '\n' for line in original_lines]
    proposed_lines_list = [line if line.endswith('\n') else line + '\n' for line in proposed_lines_list]

    new_lines = original_lines_list[:start_idx] + proposed_lines_list + original_lines_list[end_idx:]
    new_content = "".join(new_lines)

    diff = list(difflib.unified_diff(
        original_lines_list, new_lines,
        fromfile=f"a/{target_file}", tofile=f"b/{target_file}", n=3
    ))

    if not diff:
        return

    diff_text = "".join(diff)
    syntax = Syntax(diff_text, "diff", theme="monokai", background_color="default")
    
    console.print("\n[bold cyan]Interactive Auto-Fixer[/bold cyan]")
    console.print(syntax)
    console.print()

    if click.confirm(f"Apply this fix to {target_file}?"):
        with open(target_file, 'w') as f:
            f.write(new_content)
        console.print(f"[bold green]Successfully patched {target_file}[/bold green]\n")
    else:
        console.print("[dim]Fix discarded. File remains unchanged.[/dim]\n")