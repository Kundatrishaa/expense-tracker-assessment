# Personal Expense Tracker (Python + SQLite)

A simple terminal-based Expense Tracker that helps you log daily expenses, set monthly budgets, and track your spending across different categories. Built for the L7 Informatics Internship Assignment.



## Features

- Log expenses with category, amount, description, and date
- Set monthly budgets for each category
- Get alerts when you're close to or over budget (with **email notifications**)
- View total monthly spending and category-wise breakdowns
- Split expenses between group members (Splitwise-style)
- Handles edge cases like empty inputs, invalid amounts, or wrong formats
- SQLite database (via `sqlite3`) to store everything locally



## Requirements

- Python 3.7 or higher
- No external packages required (uses only standard libraries)



## How to Run the Application

1. Clone the repository  
   ```bash
   git clone https://github.com/Kundatrishaa/expense-tracker.git
   cd expense-tracker

2. Run the program
  ```bash
   python app.py
   ```


## Folder Structure

expense-tracker/
├── app.py           # Main app logic
├── models.py        # Functions for interacting with the database
├── database.py      # Initializes SQLite DB and tables
├── email_utils.py   # Handles email notifications
├── README.md
└── expenses.db      # (auto-created on first run)


## Testing & Edge Cases

Edge cases handled:
- Empty inputs for name, category, description, etc.
- Invalid or negative amounts
- Incorrect date format (requires YYYY-MM)
- Invalid menu selections (e.g., letters or out-of-range numbers)
The app will prompt the user and ask to retry if any invalid input is detected.


## Expense Sharing (Splitwise-style)

You can now split group expenses with your friends! The app allows you to:

- Create groups (e.g., "Trip Goa")

- Add members to the group

- Record shared expenses (e.g., "Hotel stay", "Dinner", etc.)

- Automatically split the total and track how much each person owes or is owed

Example:

I pays ₹3000 for hotel

Group: Me, You

App splits ₹1500 each

Final balance:

I get ₹1500

You owe ₹1500

Everything is tracked, and you can view balances anytime from the Group Expense Sharing menu.


## What's Implemented from the Assignment

| Requirement                                      | Status                     |
|--------------------------------------------------|----------------------------|
| Log daily expenses with categories               | ✅ Completed               |
| Set monthly budgets per category                 | ✅ Completed               |
| Alerts for exceeding budget                      | ✅ Completed               |
| Total monthly spending report                    | ✅ Completed               |
| Category-wise budget comparison                  | ✅ Completed               |
| Different budgets for different months           | ✅ Completed               |
| Alerts when 90% of budget is used                | ✅ Completed               |
| Edge case handling                               | ✅ Implemented             |
| ORM or SQL abstraction                           | ✅ Implemented (SQLite)    |
| Docker + build steps                             | ✅ Completed               |
| Email alerts                                     | ✅ Completed               |
| Expense sharing (Splitwise-style)                | ✅ Completed              |


## Docker Support (Optional)

To build and run the app using Docker:
```bash
docker build -t expense-tracker .
docker run -it expense-tracker
```


## Notes

- This is a terminal-only app — no frontend
- All data is stored locally in expenses.db
- Email alerts use your configured sender email (Gmail with app password)
- Built for simplicity and clarity

