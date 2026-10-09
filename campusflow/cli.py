from campusflow.tickets import (
    create_ticket,
    assign_ticket,
    change_status,
    get_work_queue,
)
from campusflow.storage import load_tickets, save_tickets
from campusflow.reports import generate_report

DATA_FILE = "tickets.json"


def run():
    tickets = load_tickets(DATA_FILE)

    print("Welcome to CampusFlow Helpdesk!")

    while True:
        print("\n1. Create ticket")
        print("2. View work queue")
        print("3. Assign ticket")
        print("4. Change ticket status")
        print("5. View report")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        # Option 1: Create a ticket
        if choice == "1":
            try:
                title = input("Ticket title: ")
                category = input(
                    "Category (Network/Hardware/Software/Other): "
                )
                urgency = input("Urgency (low/medium/high): ")
                affected_users = int(
                    input("Number of affected users: ")
                )

                ticket = create_ticket(
                    tickets, title, category, urgency, affected_users
                )
                save_tickets(tickets, DATA_FILE)

                print(f"Ticket created: {ticket['id']}")
                print(f"Priority: {ticket['priority']}")

            except ValueError as error:
                print(f"Error: {error}")

        # Option 2: View the work queue
        elif choice == "2":
            queue = get_work_queue(tickets)

            if not queue:
                print("No unresolved tickets in the work queue.")
            else:
                print("\n--- Work Queue ---")
                for ticket in queue:
                    print(
                        f"{ticket['id']} | {ticket['priority']} | "
                        f"{ticket['status']} | {ticket['title']}"
                    )

        # Option 3: Assign a ticket
        elif choice == "3":
            ticket_id = input("Ticket ID to assign: ").strip()
            assignee = input("Staff member name: ").strip()

            try:
                ticket = assign_ticket(tickets, ticket_id, assignee)
                save_tickets(tickets, DATA_FILE)
                print(
                    f"{ticket_id} assigned to "
                    f"{ticket['assigned_to']}."
                )

            except ValueError as error:
                print(f"Error: {error}")

        # Option 4: Change ticket status
        elif choice == "4":
            ticket_id = input("Ticket ID: ").strip()
            new_status = input(
                "New status (in_progress/resolved/open): "
            ).strip()

            try:
                ticket = change_status(tickets, ticket_id, new_status)
                save_tickets(tickets, DATA_FILE)
                print(
                    f"{ticket_id} status changed to "
                    f"{ticket['status']}."
                )

            except ValueError as error:
                print(f"Error: {error}")

        # Option 5: View the report
        elif choice == "5":
            report = generate_report(tickets)

            print("\n--- Ticket Report ---")
            print(f"Total tickets: {report['total']}")

            print("\nBy status:")
            for status, count in report["by_status"].items():
                print(f"{status}: {count}")

            print("\nBy priority:")
            for priority, count in report["by_priority"].items():
                print(f"{priority}: {count}")

        # Option 6: Save and exit
        elif choice == "6":
            save_tickets(tickets, DATA_FILE)
            print("Tickets saved. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    run()

