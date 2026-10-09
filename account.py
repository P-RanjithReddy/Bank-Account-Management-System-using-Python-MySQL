from decimal import Decimal, InvalidOperation
from mysql.connector import Error
from database import get_connection

def read_money(prompt, allow_zero=False):
    while True:
        raw = input(prompt).strip()
        try:
            value = Decimal(raw)
            if not value.is_finite() or value < 0 or (value == 0 and not allow_zero):
                raise ValueError
            return value.quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            print("Enter a valid positive amount" + (" or zero." if allow_zero else "."))

def read_phone():
    while True:
        phone = input("Phone number (10 to 15 digits, optional leading +): ").strip()
        digits = phone[1:] if phone.startswith("+") else phone
        if digits.isdigit() and 10 <= len(digits) <= 15:
            return phone
        print("Invalid phone number. Enter 10–15 digits.")

def create_account():
    name = input("Customer name: ").strip()
    if not name:
        print("Customer name cannot be empty.")
        return
    phone = read_phone()
    while True:
        account_type = input("Account type (Savings/Current): ").strip().title()
        if account_type in ("Savings", "Current"):
            break
        print("Choose Savings or Current.")
    account_number = input("Unique account number (e.g. 1001001): ").strip()
    if not account_number or not account_number.isalnum():
        print("Account number must contain letters/numbers and cannot be empty.")
        return
    initial = read_money("Initial deposit (enter 0 if none): ₹", allow_zero=True)
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO accounts (account_number, customer_name, phone, account_type, balance) VALUES (%s,%s,%s,%s,%s)",
            (account_number, name, phone, account_type, initial)
        )
        if initial > 0:
            cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s,'DEPOSIT',%s)",
                (account_number, initial)
            )
        conn.commit()
        print(f"Account created successfully. Account number: {account_number}")
    except Error as exc:
        conn.rollback()
        if getattr(exc, "errno", None) == 1062:
            print("That account number already exists. Use a unique account number.")
        else:
            print(f"Could not create account: {exc}")
    finally:
        cursor.close()
        conn.close()

def display_account():
    account_number = input("Account number: ").strip()
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM accounts WHERE account_number=%s", (account_number,))
        row = cursor.fetchone()
        if not row:
            print("Account not found.")
            return
        print("\n--- ACCOUNT DETAILS ---")
        print(f"Account Number : {row['account_number']}")
        print(f"Customer Name  : {row['customer_name']}")
        print(f"Phone          : {row['phone']}")
        print(f"Account Type   : {row['account_type']}")
        print(f"Current Balance: ₹{row['balance']}")
        print(f"Created Date   : {row['created_date']}")
    except Error as exc:
        print(f"Database error: {exc}")
    finally:
        cursor.close(); conn.close()

def check_balance():
    account_number = input("Account number: ").strip()
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_number=%s", (account_number,))
        row = cursor.fetchone()
        print(f"Current balance: ₹{row[0]}" if row else "Account not found.")
    except Error as exc:
        print(f"Database error: {exc}")
    finally:
        cursor.close(); conn.close()

def deposit_money():
    account_number = input("Account number: ").strip()
    amount = read_money("Deposit amount: ₹")
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("SELECT balance FROM accounts WHERE account_number=%s FOR UPDATE", (account_number,))
        row = cursor.fetchone()
        if not row:
            conn.rollback(); print("Account not found."); return
        old_balance = Decimal(str(row[0]))
        new_balance = old_balance + amount
        cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s", (new_balance, account_number))
        cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s,'DEPOSIT',%s)", (account_number, amount))
        conn.commit()
        print(f"Old Balance: ₹{old_balance:.2f}\nDeposit: ₹{amount:.2f}\nNew Balance: ₹{new_balance:.2f}")
    except Error as exc:
        conn.rollback(); print(f"Deposit failed: {exc}")
    finally:
        cursor.close(); conn.close()

def withdraw_money():
    account_number = input("Account number: ").strip()
    amount = read_money("Withdrawal amount: ₹")
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("SELECT balance FROM accounts WHERE account_number=%s FOR UPDATE", (account_number,))
        row = cursor.fetchone()
        if not row:
            conn.rollback(); print("Account not found."); return
        old_balance = Decimal(str(row[0]))
        if amount > old_balance:
            conn.rollback()
            print(f"Insufficient balance. Available balance: ₹{old_balance:.2f}")
            return
        new_balance = old_balance - amount
        cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s", (new_balance, account_number))
        cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s,'WITHDRAWAL',%s)", (account_number, amount))
        conn.commit()
        print(f"Available Balance: ₹{old_balance:.2f}\nWithdrawal: ₹{amount:.2f}\nRemaining Balance: ₹{new_balance:.2f}")
    except Error as exc:
        conn.rollback(); print(f"Withdrawal failed: {exc}")
    finally:
        cursor.close(); conn.close()

def transaction_history():
    account_number = input("Account number: ").strip()
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT transaction_id, transaction_type, amount, transaction_date FROM transactions WHERE account_number=%s ORDER BY transaction_date, transaction_id", (account_number,))
        rows = cursor.fetchall()
        if not rows:
            print("No transactions found (or account number does not exist).")
            return
        print("\nID | TYPE | AMOUNT | DATE")
        print("-" * 65)
        for row in rows:
            print(f"{row[0]} | {row[1]} | ₹{row[2]} | {row[3]}")
    except Error as exc:
        print(f"Database error: {exc}")
    finally:
        cursor.close(); conn.close()

def search_account():
    print("Search by: 1. Account Number  2. Customer Name")
    choice = input("Choose: ").strip()
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        if choice == "1":
            term = input("Account number: ").strip()
            cursor.execute("SELECT account_number, customer_name, phone, account_type, balance FROM accounts WHERE account_number=%s", (term,))
        elif choice == "2":
            term = input("Customer name (partial names allowed): ").strip()
            cursor.execute("SELECT account_number, customer_name, phone, account_type, balance FROM accounts WHERE customer_name LIKE %s ORDER BY customer_name", (f"%{term}%",))
        else:
            print("Invalid search option."); return
        rows = cursor.fetchall()
        if not rows:
            print("No matching accounts.")
            return
        for r in rows:
            print(f"Account: {r[0]} | Name: {r[1]} | Phone: {r[2]} | Type: {r[3]} | Balance: ₹{r[4]}")
    except Error as exc:
        print(f"Database error: {exc}")
    finally:
        cursor.close(); conn.close()

def update_customer():
    account_number = input("Account number to update: ").strip()
    print("Leave a field blank to keep its current value.")
    name = input("New customer name: ").strip()
    phone = input("New phone (10–15 digits, optional +): ").strip()
    account_type = input("New account type (Savings/Current): ").strip().title()
    if phone:
        digits = phone[1:] if phone.startswith("+") else phone
        if not digits.isdigit() or not 10 <= len(digits) <= 15:
            print("Invalid phone number."); return
    if account_type and account_type not in ("Savings", "Current"):
        print("Account type must be Savings or Current."); return
    changes, values = [], []
    if name: changes.append("customer_name=%s"); values.append(name)
    if phone: changes.append("phone=%s"); values.append(phone)
    if account_type: changes.append("account_type=%s"); values.append(account_type)
    if not changes:
        print("No changes entered."); return
    values.append(account_number)
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE accounts SET {', '.join(changes)} WHERE account_number=%s", tuple(values))
        if cursor.rowcount == 0:
            print("Account not found, or no values changed.")
        else:
            conn.commit()
            print("Customer details updated successfully in MySQL.")
    except Error as exc:
        conn.rollback(); print(f"Update failed: {exc}")
    finally:
        cursor.close(); conn.close()

def close_account():
    account_number = input("Account number to close: ").strip()
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("SELECT balance FROM accounts WHERE account_number=%s FOR UPDATE", (account_number,))
        row = cursor.fetchone()
        if not row:
            conn.rollback(); print("Account not found."); return
        if Decimal(str(row[0])) != 0:
            conn.rollback(); print(f"Cannot close account. Current balance is ₹{row[0]}. Withdraw/transfer the balance first."); return
        cursor.execute("DELETE FROM accounts WHERE account_number=%s", (account_number,))
        conn.commit()
        print("Account closed successfully.")
    except Error as exc:
        conn.rollback(); print(f"Account closure failed: {exc}")
    finally:
        cursor.close(); conn.close()
