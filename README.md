# Bank Account Management System using Python & MySQL

## Objective
A menu-driven console application that stores account data and transaction history in MySQL. Account balances are not kept only in Python memory.

## Technologies
- Python 3.10 or newer
- MySQL Server 8.x
- `mysql-connector-python`

## Project files
- `main.py` — menu and program entry point
- `database.py` — shared MySQL connection settings
- `account.py` — account CRUD, deposits, withdrawals, balance and history
- `transaction.py` — notes about transaction handling
- `schema.sql` — database and table creation
- `requirements.txt` — Python dependency

## Step-by-step setup (Windows + VS Code)

### 1. Install the required software
1. Install Python from https://www.python.org/downloads/ and select **Add Python to PATH** during installation.
2. Install MySQL Server and MySQL Workbench from https://dev.mysql.com/downloads/installer/.
3. Remember the MySQL `root` password you set during installation.
4. Open MySQL Workbench and connect to your local MySQL Server.

### 2. Create the database and tables
1. In MySQL Workbench, open a SQL tab.
2. Open `schema.sql` from this project and copy all its SQL into the SQL tab.
3. Click the lightning-bolt **Execute** button.
4. Refresh the Schemas panel. You should see `bank_management_db`, with `accounts` and `transactions` tables.

### 3. Configure the database password
1. Open `database.py` in VS Code.
2. Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL password.
3. Keep `host` as `localhost`, `user` as `root`, `database` as `bank_management_db`, and port as `3306` unless your MySQL setup uses different values.
4. Save the file. Do not share this file publicly while it contains your password.

### 4. Install the Python package
1. Open the project folder in VS Code.
2. Choose **Terminal → New Terminal**.
3. Run:
   ```bash
   python -m pip install -r requirements.txt
   ```
   If `python` is not recognized, try `py -m pip install -r requirements.txt`.

### 5. Run the application
In the VS Code terminal, run:
```bash
python main.py
```
If needed on Windows, use:
```bash
py main.py
```

### 6. Test each feature
1. Choose `1` to create an account. Use a unique account number, e.g. `1001001`, and an initial deposit such as `10000`.
2. Choose `2` to display account details.
3. Choose `3` to deposit, e.g. `5000`.
4. Choose `4` to withdraw, e.g. `3000`.
5. Choose `5` to check balance. Expected balance after these examples: ₹12000.
6. Choose `6` to display transaction history.
7. Choose `7` to search by account number or customer name.
8. Choose `8` to update customer details.
9. Verify the update in MySQL Workbench:
   ```sql
   USE bank_management_db;
   SELECT * FROM accounts;
   SELECT * FROM transactions ORDER BY transaction_id;
   ```
10. Choose `9` to close an account. The account must have a zero balance. For this test account, withdraw the full balance first.
11. Choose `10` to exit.

## Common errors
- **MySQL connection failed / Access denied:** Confirm MySQL Server is running and the password in `database.py` is correct.
- **Unknown database:** Run `schema.sql` in Workbench first.
- **Can't connect to MySQL server:** Start the MySQL80 service from Windows Services and confirm the configured port.
- **`python` is not recognized:** Try `py main.py`; if that works, use `py -m pip install -r requirements.txt`.
- **Duplicate account number:** Enter a different account number.

## Screenshots for submission
Capture screenshots of:
1. Successful account creation in the terminal.
2. Account details.
3. Deposit and withdrawal output.
4. Balance and transaction history.
5. Updated customer details in the terminal.
6. MySQL Workbench showing:
   ```sql
   SELECT * FROM accounts;
   SELECT * FROM transactions;
   ```
Take screenshots on your own computer after running the project; this ZIP does not include fabricated screenshots.

## Important notes
- Use this as a learning/demo project, not for real banking or real customer data.
- Passwords for MySQL are local configuration only; never upload them to a public repository.
- Deposit/withdrawal balance changes and transaction inserts are committed together.
- Account closure is allowed only when the balance is zero. The foreign key deletes associated transaction history when an account is closed, as configured in the schema.
