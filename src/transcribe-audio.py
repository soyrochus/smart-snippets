#!/usr/bin/env python3
"""
Console app to transcribe an audio file to text using OpenAI's gpt-4o-transcribe model

Usage:
  python3 transcribe-audio.py <input_audio> [-o OUTPUT_FILE] [-l LANGUAGE] [-p PROMPT]

Arguments:
  <input_audio>           Path to the input audio file (e.g., .mp3, .wav, .ogg)

Options:
  -o, --output OUTPUT     Path to the output text file. If not provided, saves as transcript_<original_file_name>.txt
  -l, --language LANGUAGE The language of the input audio in ISO-639-1 format (e.g. en, es, fr). Optional.
  -p, --prompt PROMPT     Optional text to guide the model's style or continue a previous audio segment. Must be in the language of the input audio / language argument. Optional.

Requires:
  uv add openai python-dotenv

The OpenAI API key is read from a .env file or the OPENAI_API_KEY environment variable.
"""
import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI



def get_api_key():
    """Load API key from .env or environment variable"""
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


api_key = get_api_key()
if  api_key is None:
    print(
        "Error: OPENAI_API_KEY not set in .env or environment variables",
        file=sys.stderr
    )
    sys.exit(1)
else:
    # Initialize OpenAI client with the API key

    client = OpenAI(api_key=api_key)



def transcribe_audio(input_path: str, language: str = None, prompt: str = None) -> str:
    """
    Transcribe the given audio file using OpenAI's gpt-4o-transcribe model.
    Returns the transcribed text.
    """
    try:
        with open(input_path, "rb") as audio_file:
            response =  client.audio.transcriptions.create(model="gpt-4o-transcribe",
            file=audio_file)
            
        with open(input_path, "rb") as audio_file:
            # Only include language/prompt if provided (kwargs pattern)
            kwargs = {"model": "gpt-4o-transcribe", "file": audio_file}
            if language:
                kwargs["language"] = language
            if prompt:
                kwargs["prompt"] = prompt
            response = client.audio.transcriptions.create(**kwargs)    
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        sys.exit(1)
    # Depending on response type, extract text attribute or use string directly
    if isinstance(response, str):
        return response
    return getattr(response, "text", "")  # response.text holds transcript text ([github.com](https://github.com/openai/openai-python/issues/1633?utm_source=chatgpt.com))



def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio to text using OpenAI's gpt-4o-transcribe model"
    )
    parser.add_argument(
        "input", help="Path to the input audio file (e.g., .mp3, .wav, .ogg)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Path to the output text file"
    )
    parser.add_argument(
        "-l", "--language",
        help="The language of the input audio in ISO-639-1 format (e.g. en, es, fr). Optional."
    )
    parser.add_argument(
        "-p", "--prompt",
        help="Optional text to guide the model's style or continue a previous audio segment. Must be in the language of the input audio / language argument. Optional."
    )

    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print(
            "Error: OPENAI_API_KEY not set in .env or environment variables",
            file=sys.stderr
        )
        sys.exit(1)

    transcript = transcribe_audio(args.input, language=args.language, prompt=args.prompt)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as out_f:
                out_f.write(transcript)
            print(transcript)
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        base_name = os.path.basename(args.input)
        output_name = f"transcript_{base_name}.txt"
        try:
            with open(output_name, "w", encoding="utf-8") as out_f:
                out_f.write(transcript)
            print(f"Transcript saved to {output_name}")
        except Exception as e:
            print(f"Error writing transcript file: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
