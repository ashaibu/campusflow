
VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}


def calculate_priority(urgency, affected_users):
    """Calculate priority using the CampusFlow rules."""
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def validate_ticket(title, category, urgency, affected_users):
    """Reject invalid ticket details."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be blank.")

    if category not in VALID_CATEGORIES:
        raise ValueError("Invalid category.")

    if urgency not in VALID_URGENCIES:
        raise ValueError("Invalid urgency.")

    # bool is a subclass of int in Python, so reject it explicitly.
    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be a positive integer.")

    if affected_users <= 0:
        raise ValueError("Affected users must be a positive integer.")


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate details, create a ticket, and append it to the list."""
    validate_ticket(title, category, urgency, affected_users)

    # Find the largest existing numeric ticket ID.
    highest_id = 0

    for ticket in tickets:
        ticket_id = ticket["id"]
        if (
            isinstance(ticket_id, str)
            and ticket_id.startswith("T")
            and ticket_id[1:].isdigit()
        ):
            highest_id = max(highest_id, int(ticket_id[1:]))

    new_id = f"T{highest_id + 1:03d}"

    ticket = {
        "id": new_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)
    return ticket


def get_ticket(tickets, ticket_id):
    """Find a ticket by ID."""
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