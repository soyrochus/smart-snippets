#!/usr/bin/env python3
"""Inspect GitHub Copilot Chat log exports."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable, List, Tuple

try:
    from rich.console import Console
    from rich.markdown import Markdown
except Exception:  # pragma: no cover - optional dependency
    Console = None
    Markdown = None


try:
    import markdown as md_lib
except Exception:  # pragma: no cover - optional dependency
    md_lib = None


from ai import summarize_text


Message = Tuple[str, str]


def load_chat(path: str) -> List[Message]:
    """Return conversation as a list of ``(speaker, text)`` tuples."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    conversation: List[Message] = []
    for req in data.get("requests", []):
        user_text = req.get("message", {}).get("text", "")
        conversation.append(("User", user_text))

        response_parts: List[str] = []
        for part in req.get("response", []):
            if isinstance(part, str):
                response_parts.append(part)
            elif isinstance(part, dict):
                for key in ("value", "text", "response"):
                    if key in part:
                        response_parts.append(part[key])
                        break
        ai_text = "".join(response_parts)
        conversation.append(("AI", ai_text))
    return conversation


def format_markdown(conv: Iterable[Message]) -> str:
    """Return the conversation formatted as Markdown."""
    lines: List[str] = []
    for speaker, text in conv:
        lines.append(f"**{speaker}:**\n")
        lines.append(text.strip())
        lines.append("")
    return "\n".join(lines).strip()


def format_ascii(conv: Iterable[Message]) -> None:
    """Render the conversation to the terminal with colors using Rich."""
    if Console and Markdown:
        console = Console()
        for speaker, text in conv:
            console.print(f"[bold]{speaker}:[/bold]")
            console.print(Markdown(text))
    else:
        print(format_markdown(conv))


def format_html(conv: Iterable[Message]) -> str:
    """Return the conversation as HTML."""
    md_text = format_markdown(conv)
    if md_lib is None:
        return "<pre>" + md_text + "</pre>"
    return md_lib.markdown(md_text)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a GitHub Copilot chat log",
        add_help=False,
    )
    parser.add_argument("json_file", help="Path to chat export JSON")
    parser.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        help="Render conversation with colored ASCII",
    )
    parser.add_argument(
        "-h", "--html", dest="html", action="store_true", help="Output as HTML"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Summarize conversation using AI (future feature)",
    )
    parser.add_argument("--help", action="help", help="Show this help message")

    args = parser.parse_args()

    try:
        conversation = load_chat(args.json_file)
    except FileNotFoundError:
        print(f"Error: cannot read file '{args.json_file}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON - {exc}", file=sys.stderr)
        sys.exit(1)

    if args.summary:
        try:
            joined = "\n".join(text for _, text in conversation)
            print(summarize_text(joined))
        except Exception as exc:  # pragma: no cover - placeholder
            print(f"Error during summarization: {exc}", file=sys.stderr)
            sys.exit(1)
        return

    if args.html:
        print(format_html(conversation))
    elif args.ascii:
        format_ascii(conversation)
    else:
        print(format_markdown(conversation))


if __name__ == "__main__":
    main()
