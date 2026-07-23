import random
import json

class BankAccount:
    def __init__(self, acc_no, name, balance=0):
        self.acc_no = acc_no
        self.name = name
        self.balance = balance
        self.transactions = []

        if balance > 0:
            self.transactions.append(f"Initial Deposit: +₹{balance}")

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount!")
            return
        
        self.balance += amount
        self.transactions.append(f"Deposit: +₹{amount}")
        print("Deposit successful!")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdraw: -₹{amount}")
            print("Withdrawal successful!")
        else:
            print("Insufficient balance!")

    def transfer(self, receiver, amount):
        if amount <= self.balance:
            self.balance -= amount
            receiver.balance += amount

            self.transactions.append(
                f"Transfer to {receiver.acc_no}: -₹{amount}"
            )

            receiver.transactions.append(
                f"Transfer from {self.acc_no}: +₹{amount}"
            )

            print("Transfer successful!")
        else:
            print("Insufficient balance!")

    def transaction_history(self):
        print("\n---------- Transaction History ----------")

        if not self.transactions:
            print("No transactions found.")
        else:
            for transaction in self.transactions:
                print(transaction)

    def show_details(self):
        print("\n--------------------------------------")
        print(f"Account Number : {self.acc_no}")
        print(f"Name           : {self.name}")
        print(f"Balance        : ₹{self.balance}")
        print("--------------------------------------")

    def update_account(self, new_name):
        self.name = new_name
        print("Account updated successfully!")

def save_accounts(accounts):
    data = {}

    for acc_no, account in accounts.items():
        data[acc_no] = {
            "name": account.name,
            "balance": account.balance,
            "transactions": account.transactions
        }

    with open("accounts.json", "w") as file:
        json.dump(data, file, indent=4)


def load_accounts():
    accounts = {}

    try:
        with open("accounts.json", "r") as file:
            data = json.load(file)

            for acc_no, info in data.items():
                account = BankAccount(
                    acc_no,
                    info["name"],
                    info["balance"]
                )

                account.transactions = info["transactions"]

                accounts[acc_no] = account

    except FileNotFoundError:
        pass

    return accounts

def generate_account_number(accounts):
    while True:
        acc_no = str(random.randint(100000000000, 999999999999))

        if acc_no not in accounts:
            return acc_no

accounts = load_accounts()

while True:
    print("\n=========== MARVEL BANK ===========")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. View All Accounts")
    print("6. Update Account")
    print("7. Delete Account")
    print("8. Transfer Money")
    print("9. Transaction History")
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter Name: ")
        balance = float(input("Enter Initial Balance: "))

        acc_no = generate_account_number(accounts)

        accounts[acc_no] = BankAccount(acc_no, name, balance)

        save_accounts(accounts)

        print("Account created successfully!")
        print(f"Your Account Number is: {acc_no}")

    elif choice == "2":
        acc_no = input("Enter Account Number: ")
        if acc_no in accounts:
            amount = float(input("Enter Deposit Amount: "))
            accounts[acc_no].deposit(amount)
            save_accounts(accounts)
        else:
            print("Account not found!")

    elif choice == "3":
        acc_no = input("Enter Account Number: ")
        if acc_no in accounts:
            amount = float(input("Enter Withdrawal Amount: "))
            accounts[acc_no].withdraw(amount)
            save_accounts(accounts)
        else:
            print("Account not found!")

    elif choice == "4":
        acc_no = input("Enter Account Number: ")
        if acc_no in accounts:
            accounts[acc_no].show_details()
        else:
            print("Account not found!")

    elif choice == "5":
        if not accounts:
            print("No accounts available.")
        else:
            for account in accounts.values():
                account.show_details()

    elif choice == "6":
        acc_no = input("Enter Account Number: ")

        if acc_no in accounts:
            new_name = input("Enter New Name: ")

            accounts[acc_no].update_account(new_name)
            save_accounts(accounts)
        else:
            print("Account not found!")

    elif choice == "7":
        acc_no = input("Enter Account Number: ")

        if acc_no in accounts:
            accounts[acc_no].show_details()

            confirm = input("\nDelete this account? (y/n): ").lower()

            if confirm == "y":
                del accounts[acc_no]
                save_accounts(accounts)
                print("Account deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print("Account not found!")

    elif choice == "8":
        sender = input("Enter Sender Account Number: ")
        receiver = input("Enter Receiver Account Number: ")

        if sender not in accounts:
            print("Sender account not found!")

        elif receiver not in accounts:
            print("Receiver account not found!")

        elif sender == receiver:
            print("Cannot transfer to the same account!")

        else:
            amount = float(input("Enter Amount: "))

            accounts[sender].transfer(accounts[receiver], amount)

            save_accounts(accounts)
    
    elif choice == "9":
        acc_no = input("Enter Account Number: ")

        if acc_no in accounts:
            accounts[acc_no].transaction_history()
        else:
            print("Account not found!")

    elif choice == "10":
        save_accounts(accounts)
        print("Thank you!")
        break

    else:
        print("Invalid Choice!")
        print("Please choose from 1-10")

        