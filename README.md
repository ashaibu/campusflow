# campusflow

# CampusFlow Helpdesk

CampusFlow is a Python command-line helpdesk application designed to help an IT support team create, prioritize, assign, track, and report support tickets.

This project was developed as a team sprint to practice Python programming, modular code organization, testing, JSON file storage, Git, GitHub, and collaborative development.

## Features

* **Create tickets:** Record a ticket title, category, urgency, and number of affected users.
* **Automatic prioritization:** Calculate ticket priority based on urgency and the number of affected users.
* **Assign tickets:** Assign tickets to staff members.
* **Track ticket status:** Move tickets through the support workflow.
* **Work queue:** Display unresolved tickets in priority order.
* **Reports:** View total tickets and counts by status and priority.
* **JSON persistence:** Save tickets and reload them when the application restarts.
* **Input validation:** Reject invalid ticket details and invalid status transitions.
* **Automated tests:** Verify ticket logic, storage, reporting, and important edge cases.

## Technology Stack

* Python 3
* JSON for file-based persistence
* pytest for automated testing
* Git and GitHub for version control and collaboration

## Project Structure

```text
campusflow/
├── campusflow/
│   ├── __init__.py
│   ├── cli.py
│   ├── tickets.py
│   ├── storage.py
│   └── reports.py
├── tests/
│   ├── test_tickets.py
│   └── test_storage_reports.py
├── main.py
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

* Python 3.12 or a compatible Python 3 version
* Git
* A terminal or command-line interface

### 1. Clone the repository

```bash
git clone https://github.com/ashaibu/campusflow.git
cd campusflow
```

### 2. Create a virtual environment

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the test dependency

```bash
python -m pip install pytest
```

### 4. Run the application

```bash
python main.py
```

Follow the numbered menu to create tickets, view the work queue, assign tickets, change statuses, view reports, or exit.

## Ticket Priorities

CampusFlow calculates priority using urgency and the number of affected users.

| Rule                                        | Priority |
| ------------------------------------------- | -------- |
| High urgency and at least 10 affected users | Critical |
| High urgency or at least 10 affected users  | High     |
| Medium urgency or at least 3 affected users | Medium   |
| Otherwise                                   | Low      |

The rules are evaluated from highest priority to lowest priority.

## Ticket Status Workflow

Tickets follow this workflow:

```text
open → in_progress → resolved
```

A ticket must be assigned before it can move to `in_progress`. A resolved ticket must be explicitly reopened before further status progression.

The work queue excludes resolved tickets and sorts unresolved tickets by priority, with ticket ID used to break ties.

## Running the Tests

From the project root, activate your virtual environment and run:

```bash
python -m pytest -v
```

The project passed **25 automated tests** during the development sprint.

## Data Storage

Tickets are stored locally in `tickets.json`. The application loads saved tickets on startup and saves changes as tickets are created, assigned, updated, or the application exits.

The local data file is excluded from Git so personal test data is not committed to the repository.

## Team Collaboration

The project was developed collaboratively, with work divided across two teams:

* **Team A:** Ticket engine, priority calculation, assignment, status transitions, and ticket tests.
* **Team B:** JSON storage, reports, and CLI-related integration.

The teams used GitHub pull requests to review and merge their work.

## Learning Outcomes

This project provided practical experience with:

* Writing and organizing Python modules and functions.
* Validating user input and handling exceptions.
* Working with lists, dictionaries, and JSON.
* Writing automated tests with pytest.
* Using Git branches, commits, pull requests, and merges.
* Reviewing AI-generated suggestions critically and improving incomplete implementations.

## Future Improvements

Possible future enhancements include:

* More comprehensive automated tests for CLI interactions.
* Improved handling of malformed or missing ticket data.
* Search and filtering options for tickets.
* A graphical or web-based interface.
* A database-backed storage layer.

## License

No license has been specified for this project yet.
