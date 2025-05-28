Certainly. Here is a **coherent, unambiguous prompt** for your agent that combines both your new requirements (extracting the AI connection logic from `transcribe-audio` into `ai.py`, modularizing it) and the requirements for the new `chatk-peek` chat log inspector script. The result is suitable for tasking an LLM to design or implement the change, without drifting into general refactoring territory:

---

## Prompt: Modularization and Extension of the Smart-Snippets Toolkit

**Task Overview:**
You are to improve modularity and extensibility in the `smart-snippets` project by extracting AI connection logic into a separate, reusable module, and by adding a new script for chat log inspection and reporting.

---

### Part 1: Modularizing AI Connection Logic

* **Extract** all logic related to connecting and interacting with AI models (such as OpenAI APIs, LLMs, etc.) from the existing `transcribe-audio` script.
* Place this logic in a new module named `ai.py`.

  * The new module should expose a clear, well-documented interface for other scripts in the project to use.
  * Ensure any credentials/configuration are handled in a reusable and secure way.
  * Update `transcribe-audio` (and any other affected scripts) to import and use `ai.py` for all AI interactions.

---

### Part 2: Implement the `chat-peek` Chat Log Inspector Script

**Context:**
We want to add a script which provides inspection and reporting on exported chat logs (JSON format) from GitHub Copilot Chat . This script is intended for command-line use, with output suitable for piping, redirection, or further automation.

#### Functional Requirements

1. **Input:**

   * Accept a chat log export in JSON format as a required argument.
   * Validate input and provide clear errors for unreadable or malformed files.

2. **Default Output:**

   * Print a human-readable transcript of the conversation to stdout, formatted as Markdown.
   * Alternate clearly between user and AI turns, preserving conversational order.

3. **Alternate Output Modes:**

   * `-a` / `--ascii`: Render the conversation in the terminal using colored ASCII formatting (e.g., with `rich`), distinguishing user, AI, and code blocks.
   * `-h` / `--html`: Output conversation as HTML (to stdout), preserving markdown and visual distinctions.

4. **General Behavior:**

   * Output must be suitable for piping/redirection (no interactive prompts).
   * No file writing unless the user redirects output.

5. **Extensibility:**

   * Organize code and function signatures for easy addition of new output modes, analytics, or AI-powered features (e.g., summary).
   * Ensure input/output interfaces are compatible with other toolkit scripts.

6. **Dependencies & Portability:**

   * Use only widely available open-source Python libraries; degrade gracefully if optional ones are missing.
   * Support Python 3.10+ on Unix-like and Windows systems.

#### Non-Functional Requirements

* **Performance:** Efficiently handle chat logs with hundreds of messages.
* **Robustness:** Do not crash on unexpected input; print errors and exit nonzero.
* **Maintainability:** Code must be clean, modular, and commented.
* **Testing:** Core logic (parsing, formatting) should be unit-testable.

#### Future-Proofing

* Structure code so it can easily call out to `ai.py` for future AI-powered features (e.g., summary, semantic search).
* Include stubs or hooks for future “query” features (e.g., `--summary`).

**Output:**
A modular Python script (or module) named `chat-peek`, which implements the above requirements.

---

**Example CLI Usage:**

```bash
chat-peek session.json
chat-peek -a session.json
chat-peek -h session.json > out.html
```

---

**Instructions:**
Use the new AI.py module which you refactored in Part 1
Generate code meeting these requirements. The example json is stored in the chat_export.json file in the project root
Document any external dependencies clearly.
Where relevant, ensure the AI integration points use the newly created `ai.py` module.

