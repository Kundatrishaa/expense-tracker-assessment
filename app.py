from models import (
    add_user,
    get_user_id,
    add_expense,
    set_budget,
    get_total_spent,
    get_spent_by_category,
    get_budget_for_category,
    create_group,
    add_group_member,
    get_group_id,
    get_group_members,
    add_shared_expense,
    get_balances,
    get_user_email
)
from database import init_db
from datetime import datetime
from email_utils import send_budget_alert


def get_valid_input(prompt, allow_empty=False):
    while True:
        user_input = input(prompt).strip()
        if not user_input and not allow_empty:
            print("Input cannot be empty. Please try again.")
        else:
            return user_input

def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

def get_valid_month(prompt):
    while True:
        month_input = input(prompt).strip()
        try:
            datetime.strptime(month_input, "%Y-%m")
            return month_input
        except ValueError:
            print("Invalid format. Please enter month in YYYY-MM format.")

def handle_group_menu():
    while True:
        print("\n--- Group Expense Sharing ---")
        print("1. Create Group")
        print("2. Add Member to Group")
        print("3. Add Shared Expense")
        print("4. View Group Balances")
        print("5. Back to Main Menu")
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            group_name = get_valid_input("Enter group name: ")
            create_group(group_name)
            print("Group created successfully.")

        elif choice == "2":
            group_name = get_valid_input("Enter group name: ")
            group_id = get_group_id(group_name)
            if not group_id:
                print("Group not found.")
                continue
            user_name = get_valid_input("Enter member name to add: ")
            add_group_member(group_id, user_name)
            print(f"{user_name} added to group '{group_name}'.")

        elif choice == "3":
            group_name = get_valid_input("Enter group name: ")
            group_id = get_group_id(group_name)
            if not group_id:
                print("Group not found.")
                continue
            payer = get_valid_input("Who paid? ")
            amount = get_valid_amount("Enter total amount: ")
            description = get_valid_input("Enter description: ", allow_empty=True)
            date = get_valid_input("Enter date (YYYY-MM-DD): ")
            members = get_group_members(group_id)

            if not members:
                print("No members in group to split with.")
                continue

            print(f"Group members: {', '.join(members)}")
            participant_input = get_valid_input("Enter names of participants (comma-separated): ")
            participant_list = [name.strip() for name in participant_input.split(",") if name.strip()]
            if payer not in participant_list:
                participant_list.append(payer)

            add_shared_expense(group_id, payer, amount, description, date, participant_list)
            print("Shared expense added successfully.")

        elif choice == "4":
            group_name = get_valid_input("Enter group name: ")
            group_id = get_group_id(group_name)
            if not group_id:
                print("Group not found.")
                continue
            balances = get_balances(group_id)
            print(f"\n--- Balances for '{group_name}' ---")
            for user, balance in balances.items():
                status = "owes" if balance < 0 else "gets"
                print(f"{user} {status} ₹{abs(balance):.2f}")
        
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    init_db()

    print("Welcome to Expense Tracker")
    name = get_valid_input("Enter your name: ")

    user_id = get_user_id(name)
    if not user_id:
        email = get_valid_input("Enter your email address: ")
        add_user(name, email)
        user_id = get_user_id(name)
        print("User created successfully!\n")
    else:
        print(f"Welcome back, {name}!\n")

    email = get_user_email(name)  

    while True:
        print("Choose an option:")
        print("1. Add Expense")
        print("2. Set Budget")
        print("3. View Monthly Report")
        print("4. Exit")
        print("5. Group Expense Sharing")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            category = get_valid_input("Enter expense category (e.g., Food, Transport): ")
            amount = get_valid_amount("Enter amount spent: ")
            description = get_valid_input("Enter short description: ", allow_empty=True)
            month = get_valid_month("Enter month (YYYY-MM): ")

            add_expense(user_id, category, amount, description, month)
            print("Expense added successfully.")

            budget = get_budget_for_category(user_id, category, month)
            spent = sum(x[1] for x in get_spent_by_category(user_id, month) if x[0] == category)

            if budget == 0:
                print(f"Warning: No budget set for '{category}' in {month}. Consider setting one.")
            elif spent > budget:
                print(f"Alert: You have exceeded your budget for {category} this month!")
                send_budget_alert(email, name, category, spent, budget)
            elif spent >= 0.9 * budget:
                print(f"Warning: You are at 90% of your {category} budget.")
                send_budget_alert(email, name, category, spent, budget)

        elif choice == "2":
            category = get_valid_input("Enter budget category: ")
            month = get_valid_month("Enter month (YYYY-MM): ")
            existing_budget = get_budget_for_category(user_id, category, month)

            if existing_budget > 0:
                print(f"A budget for {category} in {month} already exists: ₹{existing_budget}")
                confirm = input("Do you want to update it? (yes/no): ").strip().lower()
                if confirm != "yes":
                    print("Budget update cancelled.")
                    continue

            amount = get_valid_amount("Enter new budget amount: ")
            set_budget(user_id, category, month, amount)
            print("Budget set.")

        elif choice == "3":
            month = get_valid_month("Enter month to view report (YYYY-MM): ")
            total = get_total_spent(user_id, month)
            print(f"\nTotal spent in {month}: ₹{total:.2f}")

            by_cat = get_spent_by_category(user_id, month)
            if not by_cat:
                print("No expenses found.")
            else:
                print("\nCategory-wise breakdown:")
                for cat, amt in by_cat:
                    budget = get_budget_for_category(user_id, cat, month)
                    print(f"- {cat}: ₹{amt:.2f} (Budget: ₹{budget:.2f})")

        elif choice == "4":
            print("Goodbye!")
            break

        elif choice == "5":
            handle_group_menu()

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
