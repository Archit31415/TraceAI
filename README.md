# TraceAI

## Setup and Installation

### Prerequisites
* Python 3.9 or higher
* A Google Gemini API Key configured in a `.env` file

### Installation
```bash
git clone <repository-url>
cd TraceAI
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
pip install .

```

---

## Architecture Diagram

```text
 ┌─────────────────┐       ┌─────────────────────────────────┐
 │                 │       │ Phase 1: Interceptor            │
 │  User Command   │ ─────▶│ - Spawns child process          │
 │ (traceai py...) │       │ - Pipes stdout to terminal      │
 │                 │       │ - Traps & buffers stderr        │
 └─────────────────┘       └─────────────────────────────────┘
                                           │ (If Exit Code > 0)
                                           ▼
                           ┌─────────────────────────────────┐
                           │ Phase 2: Context Gathering      │
                           │ - Regex engine parses trace     │
                           │ - Locates exact file & line     │
                           │ - Slices +/-10 lines of code    │
                           └─────────────────────────────────┘
                                           │
                                           ▼
                           ┌─────────────────────────────────┐
                           │ Phase 3: AI & Network Layer     │
                           │ - Assembles prompt payload      │
                           │ - Streams to Gemini API         │
                           └─────────────────────────────────┘
                                           │
                                           ▼
                           ┌─────────────────────────────────┐
                           │ Phase 4: UI & Metrics           │
                           │ - Rich Markdown live render     │
                           │ - Code syntax highlighting      │
                           │ - TTFT & Latency calculation    │
                           └─────────────────────────────────┘

```

---

## Core Features

### Multi-File Intelligence

TraceAI reads your entire error log from bottom to top to find every local file involved in a crash. Instead of looking only at the exact line that failed, it gathers code snippets from the caller functions further up the stack. This gives the AI the complete context of how data traveled through your application, helping it find logic errors that happened before the actual crash.

### Interactive Auto-Fixer

After finding the bug, the tool generates a precise code fix for the target file and shows you a standard, color-coded unified diff directly in your terminal. This preview highlights exactly which lines will be removed and which lines will be added. The tool then pauses and asks for confirmation, allowing you to safely patch your source file with a single keystroke.

---

## Demo Session

![TraceAI Debugging Session](demo.png)