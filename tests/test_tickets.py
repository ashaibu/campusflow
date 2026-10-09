
import pytest

from campusflow.tickets import calculate_priority, validate_ticket


@pytest.mark.parametrize(
    "urgency,users,expected",
    [
        ("high", 10, "critical"),
        ("high", 2, "high"),
        ("low", 10, "high"),
        ("medium", 3, "medium"),
        ("low", 3, "medium"),
        ("low", 1, "low"),
    ],
)
def test_calculate_priority(urgency, users, expected):
    assert calculate_priority(urgency, users) == expected


def test_rejects_blank_title():
    with pytest.raises(ValueError, match="title"):
        validate_ticket("   ", "Network", "high", 5)


@pytest.mark.parametrize("users", [0, -1, 2.5, "5", True])
def test_rejects_invalid_affected_users(users):
    with pytest.raises(ValueError, match="positive integer"):
        validate_ticket("Wi-Fi issue", "Network", "high", users)


def test_rejects_invalid_category():
    with pytest.raises(ValueError, match="category"):
        validate_ticket("Wi-Fi issue", "Invalid", "high", 5)


def test_rejects_invalid_urgency():
    with pytest.raises(ValueError, match="urgency"):
        validate_ticket("Wi-Fi issue", "Network", "urgent", 5)


from campusflow.tickets import create_ticket


def test_create_ticket_assigns_fields_and_priority():
    tickets = []

    ticket = create_ticket(
        tickets, "Campus Wi-Fi is down", "Network", "high", 15
    )

    assert ticket["id"] == "T001"
    assert ticket["priority"] == "critical"
    assert ticket["status"] == "open"
    assert ticket["assigned_to"] is None
    assert len(tickets) == 1


def test_ticket_ids_continue_after_existing_tickets():
    tickets = [
        {"id": "T001"},
        {"id": "T003"},
    ]

    ticket = create_ticket(
        tickets, "Broken keyboard", "Hardware", "low", 1
    )

    assert ticket["id"] == "T004"


def get_ticket(tickets, ticket_id):
    """Find a ticket by ID or raise an error."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} not found.")


def assign_ticket(tickets, ticket_id, assigned_to):
    """Assign an open ticket to a staff member."""
    ticket = get_ticket(tickets, ticket_id)

    if ticket["status"] != "open":
        raise ValueError("Only open tickets can be assigned.")

    if not isinstance(assigned_to, str) or not assigned_to.strip():
        raise ValueError("Assignee cannot be blank.")

    ticket["assigned_to"] = assigned_to.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    """Apply the permitted ticket status transitions."""
    ticket = get_ticket(tickets, ticket_id)
    current_status = ticket["status"]

    if new_status == "in_progress":
        if current_status != "open":
            raise ValueError("Only open tickets can start in progress.")
        if not ticket["assigned_to"]:
            raise ValueError("Ticket must be assigned before work starts.")

    elif new_status == "resolved":
        if current_status != "in_progress":
            raise ValueError("Only in-progress tickets can be resolved.")

    elif new_status == "open":
        if current_status != "resolved":
            raise ValueError("Only resolved tickets can be reopened.")

    else:
        raise ValueError("Invalid status.")

    ticket["status"] = new_status
    return ticket


def get_work_queue(tickets):
    """Return unresolved tickets, highest priority first."""
    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    queue = [
        ticket for ticket in tickets
        if ticket["status"] in {"open", "in_progress"}
    ]

    return sorted(
        queue,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )


from campusflow.tickets import (
    assign_ticket,
    change_status,
    get_ticket,
    get_work_queue,
)


def make_ticket(tickets, title, urgency, users):
    return create_ticket(tickets, title, "Network", urgency, users)


def test_assignment_and_status_workflow():
    tickets = []
    ticket = make_ticket(tickets, "Wi-Fi down", "high", 15)

    assign_ticket(tickets, ticket["id"], "Alex")
    change_status(tickets, ticket["id"], "in_progress")
    change_status(tickets, ticket["id"], "resolved")

    assert ticket["assigned_to"] == "Alex"
    assert ticket["status"] == "resolved"


def test_cannot_start_without_assignment():
    tickets = []
    ticket = make_ticket(tickets, "Wi-Fi down", "high", 15)

    with pytest.raises(ValueError, match="assigned"):
        change_status(tickets, ticket["id"], "in_progress")


def test_resolved_ticket_can_only_reopen_explicitly():
    tickets = []
    ticket = make_ticket(tickets, "Wi-Fi down", "low", 1)

    assign_ticket(tickets, ticket["id"], "Alex")
    change_status(tickets, ticket["id"], "in_progress")
    change_status(tickets, ticket["id"], "resolved")
    change_status(tickets, ticket["id"], "open")

    assert ticket["status"] == "open"


def test_work_queue_sorts_by_priority_then_id_and_excludes_resolved():
    tickets = [
        {"id": "T003", "priority": "high", "status": "open"},
        {"id": "T002", "priority": "critical", "status": "open"},
        {"id": "T001", "priority": "high", "status": "in_progress"},
        {"id": "T004", "priority": "low", "status": "resolved"},
    ]

    queue = get_work_queue(tickets)

    assert [ticket["id"] for ticket in queue] == ["T002", "T001", "T003"]


def test_get_ticket_rejects_unknown_id():
    with pytest.raises(ValueError, match="not found"):
        get_ticket([], "T999")