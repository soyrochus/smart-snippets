"""Console based I/O API for bicameral agent."""
from __future__ import annotations


def send_message(text: str) -> None:
    """Send a message to the user via stdout."""
    print(text)


def receive_response() -> str:
    """Return the next line of user input."""
    return input("> ")