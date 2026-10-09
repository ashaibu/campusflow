import json

import pytest

from campusflow.storage import load_tickets, save_tickets


def test_missing_file_returns_empty_list(tmp_path):
    path = tmp_path / "missing.json"

    assert load_tickets(path) == []


def test_save_and_reload_tickets(tmp_path):
    path = tmp_path / "tickets.json"
    tickets = [
        {
            "id": "T001",
            "title": "Campus Wi-Fi is down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 15,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
        }
    ]

    save_tickets(tickets, path)

    assert load_tickets(path) == tickets


def test_malformed_json_raises_error_without_erasing_file(tmp_path):
    path = tmp_path / "broken.json"
    original_content = "{invalid json"
    path.write_text(original_content, encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid ticket JSON"):
        load_tickets(path)

    assert path.read_text(encoding="utf-8") == original_content


def test_non_list_json_raises_error(tmp_path):
    path = tmp_path / "wrong.json"
    path.write_text(json.dumps({"ticket": "T001"}), encoding="utf-8")

    with pytest.raises(ValueError, match="JSON list"):
        load_tickets(path)