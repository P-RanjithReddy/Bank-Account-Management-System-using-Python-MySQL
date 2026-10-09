CREATE DATABASE IF NOT EXISTS bank_management_db;
USE bank_management_db;

CREATE TABLE IF NOT EXISTS accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    account_type VARCHAR(20) NOT NULL,
    balance DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL,
    transaction_type ENUM('DEPOSIT', 'WITHDRAWAL') NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transactions_account
        FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Optional sample data is intentionally omitted. Create accounts through the Python menu.
