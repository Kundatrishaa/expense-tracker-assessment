from database import get_connection

# ----------------- Personal Expense Functions -----------------

def add_user(name, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

def get_user_id(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def get_user_email(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def add_expense(user_id, category, amount, description, month):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (user_id, category, amount, description, month) VALUES (?, ?, ?, ?, ?)",
        (user_id, category, amount, description, month),
    )
    conn.commit()
    conn.close()

def set_budget(user_id, category, month, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO budgets (user_id, category, month, amount)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, category, month) DO UPDATE SET amount = excluded.amount
    """, (user_id, category, month, amount))
    conn.commit()
    conn.close()

def get_total_spent(user_id, month):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id = ? AND month = ?",
        (user_id, month)
    )
    total = cur.fetchone()[0]
    conn.close()
    return total or 0

def get_spent_by_category(user_id, month):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND month = ? GROUP BY category",
        (user_id, month)
    )
    results = cur.fetchall()
    conn.close()
    return results

def get_budget_for_category(user_id, category, month):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT amount FROM budgets WHERE user_id = ? AND category = ? AND month = ?",
        (user_id, category, month)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

# ----------------- Group Expense Sharing Functions -----------------

def create_group(group_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO groups (name) VALUES (?)", (group_name,))
    conn.commit()
    conn.close()

def add_group_member(group_id, user_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO group_members (group_id, user_name) VALUES (?, ?)", (group_id, user_name))
    conn.commit()
    conn.close()

def get_group_id(group_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM groups WHERE name = ?", (group_name,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def get_group_members(group_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_name FROM group_members WHERE group_id = ?", (group_id,))
    members = [row[0] for row in cur.fetchall()]
    conn.close()
    return members

def add_shared_expense(group_id, payer_name, amount, description, date, participant_names):
    conn = get_connection()
    cur = conn.cursor()

    # Insert shared expense
    cur.execute("""
        INSERT INTO shared_expenses (group_id, payer_name, amount, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (group_id, payer_name, amount, description, date))
    expense_id = cur.lastrowid

    # Equal share for participants
    split_amount = round(amount / len(participant_names), 2)

    for name in participant_names:
        cur.execute("""
            INSERT INTO expense_participants (expense_id, user_name, share_amount)
            VALUES (?, ?, ?)
        """, (expense_id, name, split_amount))

    conn.commit()
    conn.close()

def get_balances(group_id):
    conn = get_connection()
    cur = conn.cursor()

    # Total paid per person
    cur.execute("""
        SELECT payer_name, SUM(amount) FROM shared_expenses
        WHERE group_id = ?
        GROUP BY payer_name
    """, (group_id,))
    paid = dict(cur.fetchall())

    # Total owed per person
    cur.execute("""
        SELECT user_name, SUM(share_amount) FROM expense_participants
        JOIN shared_expenses ON expense_participants.expense_id = shared_expenses.id
        WHERE shared_expenses.group_id = ?
        GROUP BY user_name
    """, (group_id,))
    owed = dict(cur.fetchall())

    # Net balances = paid - owed
    all_users = set(paid.keys()).union(owed.keys())
    balances = {user: round(paid.get(user, 0) - owed.get(user, 0), 2) for user in all_users}

    conn.close()
    return balances
