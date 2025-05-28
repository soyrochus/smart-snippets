# smart-snippets

A collection of useful, standalone Python scripts demonstrating features of the OpenAI API.

## Overview

**smart-snippets** is a lightweight repository containing working, functional scripts that showcase how to interact with the OpenAI API. Each snippet is a self-contained console application you can run out of the box. More scripts will be added over time.

## Current Scripts

### `transcribe_audio.py`

A simple console tool that:

1. Reads an audio file (MP3, WAV, OGG, etc.)
2. Sends it to OpenAI’s new `gpt-4o-transcribe` model for transcription
3. Outputs the transcribed text to:

   * Standard output (printed) if an output path is specified
   * A file named `transcript_<original_file_name>.txt` by default

**Usage:**

```bash
python3 transcribe_audio.py path/to/audio.mp3 [-o path/to/output.txt]
```

### `chat-peek`

A CLI tool for inspecting exported chat logs from GitHub Copilot Chat.

**Usage:**

```bash
chat-peek session.json
chat-peek -a session.json
chat-peek -h session.json > out.html
```

`chat-peek` works with the base dependencies of this project. For colored
terminal output or HTML rendering, install the optional packages `rich` and
`markdown`.

## Installation

This project uses `uv` for dependency management with a `pyproject.toml`.

1. Clone the repo:

```bash

git clone https://github.com/soyrochus/smart-snippets.git
cd smart-snippets

```

2. Install dependencies via `uv sync`:

```bash
   uv sync
```
For uv see https://docs.astral.sh/uv/

This will read the `pyproject.toml` and install all required packages.

## Configuration

1. Create a `.env` file in the project root containing your OpenAI API key:

```dotenv

OPENAI_API_KEY=your_key_here

```

2. Alternatively, set the `OPENAI_API_KEY` environment variable:
  
```bash
export OPENAI_API_KEY=[your_key_here]

```

## License and Copyright

Copyright (c) 2025, Iwan van der Kleijn

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
