#!/usr/bin/env python3
"""Utility functions for interacting with AI services."""
from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_openai_api_key() -> Optional[str]:
    """Return the OpenAI API key from environment variables or .env."""
    return os.getenv("OPENAI_API_KEY")


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Return an ``OpenAI`` client instance using the given or configured key."""
    if api_key is None:
        api_key = get_openai_api_key()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not set in .env or environment variables"
        )
    return OpenAI(api_key=api_key)


def transcribe_audio(
    input_path: str,
    *,
    language: Optional[str] = None,
    prompt: Optional[str] = None,
) -> str:
    """Return the transcript of ``input_path`` using ``gpt-4o-transcribe``."""
    client = get_openai_client()
    with open(input_path, "rb") as audio_file:
        kwargs = {"model": "gpt-4o-transcribe", "file": audio_file}
        if language:
            kwargs["language"] = language
        if prompt:
            kwargs["prompt"] = prompt
        response = client.audio.transcriptions.create(**kwargs)
    return response.text if hasattr(response, "text") else str(response)


def summarize_text(_text: str) -> str:
    """Placeholder for future AI-powered summarization."""
    raise NotImplementedError("Summary feature not implemented yet.")


__all__ = [
    "get_openai_api_key",
    "get_openai_client",
    "transcribe_audio",
    "summarize_text",
]
