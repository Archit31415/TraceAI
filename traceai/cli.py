import sys
import time
import click
from traceai.interceptor import run_and_intercept
from traceai.parser import extract_all_crash_locations
from traceai.slicer import build_multi_file_context
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

    # Phase 1: Intercept application execution telemetry
    exit_code, stderr_output = run_and_intercept(command_list)

    if exit_code == 0:
        click.secho("\nExecution finished cleanly.", fg="green")
        sys.exit(0)
    else:
        # Start high-resolution internal metrics timer exactly at crash moment
        crash_time = time.perf_counter() 
        
        click.secho(f"Crash Detected! (Exit Code {exit_code})", fg="red", bold=True)
        
        # Phase 2: Context Gathering Engine (Multi-File Intelligence)
        locations = extract_all_crash_locations(stderr_output)
        context_string, file_bounds = None, {}
        
        if locations:
            context_string, file_bounds = build_multi_file_context(locations)
            
        # Phase 3 & 4: Get AI Stream and Render Live UI Component Layouts
        try:
            stream = get_debugging_stream(stderr_output, context_string)
            
            # Capture streamed output and log performance benchmarks
            full_text = render_stream_and_benchmark(stream, crash_time)
            
            # Phase 5: Interactive Auto-Fixer Patcher
            if context_string and file_bounds:
                propose_and_apply_fix(file_bounds, full_text)
                
        except Exception as e:
            click.secho(f"Failed to fetch AI analysis: {e}", fg="red")
            
        sys.exit(exit_code)

if __name__ == "__main__":
    main()