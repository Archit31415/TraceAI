import sys
import time
import click
from traceai.interceptor import run_and_intercept
from traceai.parser import extract_crash_location
from traceai.slicer import extract_code_context
from traceai.ai_client import get_debugging_stream
from traceai.ui import render_stream_and_benchmark
from traceai.patcher import propose_and_apply_fix

@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('target_command', nargs=-1, type=click.UNPROCESSED)
def main(target_command):
    if not target_command:
        click.secho("Please provide a command to run.", fg="yellow")
        sys.exit(1)

    command_list = list(target_command)
    click.secho(f"TraceAI running: {' '.join(command_list)}\n", fg="cyan", bold=True)

    exit_code, stderr_output = run_and_intercept(command_list)

    if exit_code == 0:
        click.secho("\nExecution finished cleanly.", fg="green")
        sys.exit(0)
    else:
        crash_time = time.perf_counter() 
        
        click.secho(f"Crash Detected! (Exit Code {exit_code})", fg="red", bold=True)
        
        file_path, line_num = extract_crash_location(stderr_output)
        context, start_line, end_line = None, None, None
        
        if file_path and line_num:
            context, start_line, end_line = extract_code_context(file_path, line_num)
            
        try:
            stream = get_debugging_stream(stderr_output, context)
            
            full_text = render_stream_and_benchmark(stream, crash_time)
            
            if context and start_line and end_line:
                propose_and_apply_fix(file_path, start_line, end_line, full_text)
                
        except Exception as e:
            click.secho(f"Failed to fetch AI analysis: {e}", fg="red")
            
        sys.exit(exit_code)