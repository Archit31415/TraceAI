import sys
import click
from traceai.interceptor import run_and_intercept

@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('target_command', nargs=-1, type=click.UNPROCESSED)
def main(target_command):
    # If the user just types 'traceai' with no arguments
    if not target_command:
        click.secho("Please provide a command to run.", fg="yellow", bold=True)
        click.echo("Usage: traceai [COMMAND]...")
        click.echo("Example: traceai python broken_script.py")
        sys.exit(1)

    command_list = list(target_command)
    
    click.secho(f"TraceAI running: {' '.join(command_list)}\n", fg="cyan", bold=True)

    exit_code, stderr_output = run_and_intercept(command_list)

    if exit_code == 0:
        click.secho("\nExecution finished cleanly (Exit Code 0).", fg="green", bold=True)
        sys.exit(0)
    else:
        click.secho(f"\nCrash Detected! (Exit Code {exit_code})", fg="red", bold=True)
        click.secho("INTERCEPTED STDERR", fg="yellow")
        
        click.echo(stderr_output.strip() if stderr_output else "No stderr output.")
        
        click.secho("\n[TraceAI] Next Phase: This stack trace will be sent to the AI Context Engine...", dim=True)
        
        sys.exit(exit_code)

if __name__ == "__main__":
    main()