import json
from pathlib import Path


def load_tickets(path):
    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid ticket JSON in {file_path}: {error}"
        ) from error

    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a JSON list.")

    return tickets


def save_tickets(tickets, path):
    file_path = Path(path)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2)