import os
import sys
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

SYSTEM_PROMPT = """You are TraceAI, an elite, hyper-concise terminal debugging assistant.
Your goal is to diagnose script crashes and provide immediate, accurate fixes.

Rules for your response:
1. NO conversational filler (e.g., never say "Here is the fix", "I can help", or "Sure").
2. Root Cause: Identify exactly why the code failed in 1-2 short sentences.
3. The Fix: Provide the corrected code snippet.
4. Format your entire output in clean Markdown. Use code blocks for all code.
"""

def assemble_payload(stderr: str, code_context: Optional[str]) -> str:
    payload = f"### CRASH LOG (STDERR)\n```text\n{stderr.strip()}\n```\n"
    
    if code_context:
        payload += f"\n### LOCAL SOURCE CODE CONTEXT\n```python\n{code_context}\n```\n"
    else:
        payload += "\n### LOCAL SOURCE CODE CONTEXT\n*No local file context could be extracted.*"
        
    payload += "\nAnalyze the crash and provide the exact fix."
    return payload


def stream_debugging_analysis(stderr: str, code_context: Optional[str] = None):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\nError: GEMINI_API_KEY environment variable not found.")
        print("Please create a .env file in your project root and add your key.")
        sys.exit(1)

    client = genai.Client()
    
    user_prompt = assemble_payload(stderr, code_context)

    try:
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash-lite',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.0, 
            )
        )
        
        print("\n[TraceAI Analysis]\n")
        
        for chunk in response_stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                
        
    except Exception as e:
        print(f"\nAI Network Error: {str(e)}")


# Local Testing Block
if __name__ == "__main__":
    sample_stderr = """
Traceback (most recent call last):
  File "broken.py", line 4, in <module>
    print(amt[10])
IndexError: list index out of range
"""

    sample_context = """
   1 | def calculate_totals():
   2 |     amt = [5, 10, 15, 20]
>> 4 |     print(amt[10])
   5 |     return True
"""
    
    print("Initiating TraceAI Network Test...")
    stream_debugging_analysis(sample_stderr, sample_context)