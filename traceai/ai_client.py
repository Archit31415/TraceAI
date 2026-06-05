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

SYSTEM_PROMPT = """You are TraceAI, an elite, hyper-concise terminal debugging assistant.
Your goal is to diagnose script crashes and provide immediate, accurate fixes.

Rules for your response:
1. NO conversational filler (e.g., never say "Here is the fix", "I can help", or "Sure").
2. Root Cause: Identify exactly why the code failed in 1-2 short sentences.
3. The Fix: Provide the corrected code snippet.
4. Format your entire output in clean Markdown. Use code blocks for all code.

CRITICAL INSTRUCTION FOR INTERACTIVE FIXES:
You must provide the final corrected code inside a single Markdown code block at the absolute end of your response. 
This specific code block MUST contain the ENTIRE corrected context window provided to you. Do not use ellipsis or placeholders like `...`. Rewrite the exact lines provided in the source context with your changes applied so that the block can be extracted and injected directly back into the user's file.
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