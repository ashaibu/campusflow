def generate_report(tickets):
    statuses = ["open", "in_progress", "resolved"]
    priorities = ["critical", "high", "medium", "low"]

    status_counts = {status: 0 for status in statuses}
    priority_counts = {priority: 0 for priority in priorities}

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]

        if status in status_counts:
            status_counts[status] += 1

        if priority in priority_counts:
            priority_counts[priority] += 1

    return {
        "total": len(tickets),
        "by_status": status_counts,
        "by_priority": priority_counts,
    }