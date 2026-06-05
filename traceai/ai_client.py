import os
from typing import Optional
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types
from pathlib import Path

# Load .env searching upwards from the current directory
load_dotenv(find_dotenv())
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client() if api_key else None

SYSTEM_PROMPT = """
You are a concise, expert terminal debugging assistant.
You will receive a stack trace and the code context for MULTIPLE local files involved in the execution path.
Analyze the flow to find the true root cause (which may be in a caller function, not the final crash site).

CRITICAL INSTRUCTION FOR FIXES:
You must provide the fix in a single Markdown code block at the end of your response. 
1. The FIRST LINE inside your code block MUST be a comment specifying the exact file path you are fixing, like this:
# file: exact/path/to/file.py

2. The rest of the code block MUST contain the ENTIRE corrected context window for that specific file. Do not use placeholders. Rewrite the exact lines provided in the context with your fix applied.
"""

def assemble_payload(stderr: str, code_context: Optional[str]) -> str:
    payload = f"### CRASH LOG (STDERR)\n```text\n{stderr.strip()}\n```\n"
    if code_context:
        payload += f"\n### LOCAL SOURCE CODE CONTEXT\n```python\n{code_context}\n```\n"
    else:
        payload += "\n### LOCAL SOURCE CODE CONTEXT\n*No local file context could be extracted.*"
    payload += "\nAnalyze the crash and provide the exact fix."
    return payload

def get_debugging_stream(stderr: str, code_context: Optional[str] = None):
    """Returns the live stream generator to be consumed by the UI layer."""
    global client
    if not client:
        raise ValueError("GEMINI_API_KEY environment variable not found or client failed to initialize.")
        
    user_prompt = assemble_payload(stderr, code_context)
    
    return client.models.generate_content_stream(
        model='gemini-2.5-flash-lite',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.0,
        )
    )