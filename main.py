from account import (
    create_account, display_account, deposit_money, withdraw_money,
    check_balance, transaction_history, search_account, update_customer, close_account
)

MENU = """
========================================
    BANK ACCOUNT MANAGEMENT SYSTEM
========================================
1. Create Account
2. Display Account Details
3. Deposit Money
4. Withdraw Money
5. Check Balance
6. Transaction History
7. Search Account
8. Update Customer Details
9. Close Account
10. Exit
"""

def main():
    actions = {
        "1": create_account,
        "2": display_account,
        "3": deposit_money,
        "4": withdraw_money,
        "5": check_balance,
        "6": transaction_history,
        "7": search_account,
        "8": update_customer,
        "9": close_account,
    }
    while True:
        print(MENU)
        choice = input("Enter your choice (1-10): ").strip()
        if choice == "10":
            print("Thank you for using Bank Account Management System.")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except (KeyboardInterrupt, EOFError):
                print("\nOperation cancelled.")
            except Exception as exc:
                print(f"Unexpected error: {exc}")
        else:
            print("Invalid menu option. Please enter a number from 1 to 10.")
        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    main()
