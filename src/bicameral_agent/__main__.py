"""Entry point for running the bicameral agent."""
from __future__ import annotations

import argparse
import logging

from .orchestrator import run_orchestrator


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the bicameral agent")
    parser.add_argument("prompt", help="Path to the system prompt text file")
    parser.add_argument("--memoryfile", help="Path to the agent memory file", default=None)
    parser.add_argument("--init", action="store_true", help="Create the memory file if it does not exist")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging to the console")
    args = parser.parse_args()

    try:
        run_orchestrator(args.prompt, memoryfile=args.memoryfile, init=args.init, debug=args.debug)
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Agent terminated with an error: %s", exc)


if __name__ == "__main__":  # pragma: no cover
    main()

