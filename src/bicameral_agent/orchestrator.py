"""Orchestrator for the bicameral agent."""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

from openai import OpenAI, OpenAIError
from .in_out import send_message, receive_response
from .memory import get_memory, update_memory
from ai import get_openai_client

logger = logging.getLogger(__name__)



def run_orchestrator(prompt_path: str, memoryfile: str = None, init: bool = False, debug: bool = False) -> None:
    """Run the bicameral agent using ``prompt_path`` as the system prompt."""
    log_level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    prompt = Path(prompt_path).read_text(encoding="utf-8")
    client = get_openai_client()

    # Patch memory file and init flag for memory functions
    import bicameral_agent.memory as memory_mod
    if memoryfile:
        memory_mod.MEMORY_FILE = memoryfile
    memory_mod.INIT_MEMORY = init

    functions = [
        {
            "name": "get_memory",
            "description": "Retrieve the persistent agent state as a JSON object.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "update_memory",
            "description": "Persist the provided agent state.",
            "parameters": {
                "type": "object",
                "properties": {"state": {"type": "object"}},
                "required": ["state"],
            },
        },
        {
            "name": "send_message",
            "description": "Display a message to the user.",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        },
        {
            "name": "receive_response",
            "description": "Block until the user provides input.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    ]

    messages = [
        {"role": "system", "content": prompt},
    ]

    model_name = os.environ.get("OPENAI_MODEL_ID", "gpt-4o")
    while True:
        try:
            response = client.chat.completions.create(
                model=model_name, messages=messages, functions=functions, function_call="auto"
            )
        except OpenAIError as exc:
            logger.exception("OpenAI API call failed: %s", exc)
            break

        choice = response.choices[0]
        message = choice.message
        logger.info("LLM reply: role=%s", message.role)
        if message.content:
            logger.debug("content: %s", message.content)
        if message.function_call:
            logger.info("function_call: %s", message.function_call)

        messages.append(message.model_dump())

        if message.function_call:
            fn_name = message.function_call.name
            try:
                args = json.loads(message.function_call.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            result: Any = None
            if fn_name == "get_memory":
                result = get_memory()
            elif fn_name == "update_memory":
                update_memory(args.get("state", {}))
                result = {"status": "ok"}
            elif fn_name == "send_message":
                send_message(args.get("text", ""))
                result = {"status": "sent"}
            elif fn_name == "receive_response":
                user_in = receive_response()
                result = {"response": user_in}
            else:
                result = {"error": f"Unknown function {fn_name}"}
            messages.append(
                {"role": "function", "name": fn_name, "content": json.dumps(result)}
            )
            continue

        if choice.finish_reason == "stop":
            break

