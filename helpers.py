import os
import sys
import csv 


"Check account balance"
def check_balance():
    with open("current_balance.txt", "r") as balance_file:        
        for line in balance_file:    
            if line.startswith("balance:"):    
                line = line.strip().split()
                return line[1]

"Ccheck quantity of product in the store - return quantity and file_list"
def check_quantity(product):
    # Write file contents to the file_list
    file_list = []
    current_store_quantity = 0
    with open("store.csv", "r", newline="") as store_file:
        reader = csv.DictReader(store_file)
        if reader != "":
            for row in reader:
                file_list.append(row) 
                if row["product"] == product:  
                    current_store_quantity = int(row["quantity"])            
    return (current_store_quantity, file_list)
    
"Update store.csv file"
def update_store_file(file_list):
    with open("store.csv", "w", newline="") as store_file:
        fieldnames = ["product", "quantity"]
        writer = csv.DictWriter(store_file, fieldnames=fieldnames)
        writer.writeheader() 
        for product in file_list:        
            writer.writerow(product)

"Update current_balance.txt file"
def update_balance_file(current_balance):
    with open("current_balance.txt", "w") as balance_file:
        balance_file.write(f"balance: {current_balance}")

"Update transactions.txt file"
def update_transactions_file():
    commands = read_commands()
    with open("transactions.txt", "a") as transactions_file:    
        transaction_str = " ". join(commands[1: ])
        transactions_file.write(transaction_str + "\n")
    print(" ".join(commands))

"Save current command to log.txt"
def save_to_log():
    commands = read_commands() 
    with open("log.txt", "a") as log_file:
        commands_str = " ".join(commands)
        log_file.write(commands_str + "\n")

"Check if user entered correct commands"
def validate_user_inputs():
    commands = read_commands()
    try:    
        product = str(commands[2]) 
    except ValueError or IndexError:    
        print("Enter product id")
    
    try:    
        price = int(commands[3]) 
    except ValueError or IndexError:    
        sys.exit("Enter price per item")
          
    try:    
        quantity = int(commands[4]) 
    except ValueError or IndexError:    
        sys.exit("Enter quantity")
        
    total = price * quantity

    if price < 1 or quantity < 1:    
        sys.exit("Price and quantity cannot be less than 1") 
    return (product, price, quantity, total)

"Check if database exists"
def start_database():
    # Check if current_balance.txt file exists
    if os.path.isfile("current_balance.txt"):
        print()
    # current_balance.txt file doesn't exist - create a file and initiate account balance info
    else:
        with open("current_balance.txt", "w") as account_file:
            account_file.write("balance: 0")

"Read args"
def read_commands():
    return sys.argv