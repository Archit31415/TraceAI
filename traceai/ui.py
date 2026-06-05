import time
from typing import Generator
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

def render_stream_and_benchmark(response_stream: Generator, crash_time: float):
    accumulated_text = ""
    first_token_time = None
    
    console.print("\n[bold cyan]TraceAI Analysis[/bold cyan]")
    
    with Live(Markdown(accumulated_text), console=console, refresh_per_second=15) as live:
        try:
            for chunk in response_stream:
                if chunk.text:
                    if first_token_time is None:
                        first_token_time = time.perf_counter()
                    
                    accumulated_text += chunk.text
                    live.update(Markdown(accumulated_text))
                    
        except Exception as e:
            live.update(Markdown(f"**Stream Interrupted:** {str(e)}"))

    end_time = time.perf_counter()
    
    ttft = (first_token_time - crash_time) if first_token_time else 0
    total_time = end_time - crash_time
    
    metrics_panel = Panel(
        f"⏱[bold green]Time to First Token (TTFT):[/bold green] {ttft:.2f}s\n"
        f"[bold blue]Total Execution Time:[/bold blue] {total_time:.2f}s",
        title="[bold]Performance Metrics[/bold]",
        border_style="dim",
        expand=False
    )
    
    console.print("\n")
    console.print(metrics_panel)

    return accumulated_text