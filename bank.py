def read_data(filename):
    with open(filename, 'r') as f:
        data = {}
        for line in f:
            password, name, balance = line.strip().split(':')
            data[password] = {"name": name, "balance": float(balance)}
        return data

def write_data(filename, data):
    with open(filename, 'w') as f:
        for password, values in data.items():
            f.write(f"{password}:{values['name']}:{values['balance']}\n")

# Functions for bank balance management
def read_bank_balance(filename):
    with open(filename, 'r') as f:
        bank_balance = {}
        for line in f:
            denomination, quantity = line.strip().split(':')
            bank_balance[float(denomination)] = int(quantity)
        return bank_balance

def has_sufficient_bank_balance(amount, bank_balance):
    temp_balance = bank_balance.copy()
    for denom in sorted(temp_balance.keys(), reverse=True):
        while denom <= amount and temp_balance[denom] > 0:
            amount -= denom
            temp_balance[denom] -= 1
    return amount == 0

def update_bank_balance(amount, bank_balance):
    for denom in sorted(bank_balance.keys(), reverse=True):
        while denom <= amount and bank_balance[denom] > 0:
            amount -= denom
            bank_balance[denom] -= 1
    with open('bankbalance.txt', 'w') as f:
        for denomination, quantity in bank_balance.items():
            f.write(f"{denomination}:{quantity}\n")

# Transaction functions
def deposit(data, password):
    amount = float(input("Enter the amount to deposit: "))
    data[password]['balance'] += amount
    print(f"Deposited {amount}. New balance: {data[password]['balance']}")

def withdraw(data, password, bank_balance):
    amount = float(input("Enter the amount to withdraw: "))
    if amount <= data[password]['balance']:
        if has_sufficient_bank_balance(amount, bank_balance):
            data[password]['balance'] -= amount
            update_bank_balance(amount, bank_balance)
            print(f"Withdrew {amount}. New balance: {data[password]['balance']}")
        else:
            print("Bank does not have sufficient denominations for this amount.")
    else:
        print("Insufficient funds!")

def check_balance(data, password):
    print(f"Your balance is: {data[password]['balance']}")

def main():
    data = read_data('customers.txt')
    bank_balance = read_bank_balance('bankbalance.txt')
    password = input("Enter your password: ")

    if password not in data:
        print("Incorrect password!")
        return

    while True:
        print("\nMenu:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Exit")
        choice = int(input("Choose an option (1/2/3/4): "))

        if choice == 1:
            deposit(data, password)
        elif choice == 2:
            withdraw(data, password, bank_balance)
        elif choice == 3:
            check_balance(data, password)
        elif choice == 4:
            write_data('customers.txt', data)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select from the menu.")

if __name__ == "__main__":
    main()