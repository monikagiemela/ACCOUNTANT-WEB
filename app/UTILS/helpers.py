import os
import sys
import csv 


def check_balance() -> str:
    """Check account balance"""
    with open("current_balance.txt", "r") as balance_file:        
        for line in balance_file:    
            if line.startswith("balance:"):    
                line = line.strip().split()
                return line[1]

def check_quantity(product) -> tuple:
    """Check quantity of the product in the store - return quantity and file_list"""
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
    
def update_store_file(file_list) -> None:
    """Update store.csv file"""
    with open("store.csv", "w", newline="") as store_file:
        fieldnames = ["product", "quantity"]
        writer = csv.DictWriter(store_file, fieldnames=fieldnames)
        writer.writeheader() 
        for product in file_list:        
            writer.writerow(product)

def update_balance_file(current_balance) -> None:
    """Update current_balance.txt file"""
    with open("current_balance.txt", "w") as balance_file:
        balance_file.write(f"balance: {current_balance}")

def update_transactions_file(commands) -> str:
    """Update transactions.txt file"""
    with open("transactions.txt", "a") as transactions_file:    
        transaction_str = " ". join(commands[1: ])
        transactions_file.write(transaction_str + "\n")
    return " ".join(commands)

def save_to_log(commands) -> None:
    """Save current command to log.txt"""
    with open("log.txt", "a") as log_file:
        commands_str = " ".join(commands)
        log_file.write(commands_str + "\n")

def validate_user_inputs(commands) -> tuple:
    """Check if user entered correct commands"""
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

def start_database() -> None:
    """Check if database exists"""
    # Check if current_balance.txt file exists
    if os.path.isfile("current_balance.txt"):
        print()
    # If current_balance.txt file doesn't exist - create a file and initiate account balance info
    else:
        with open("current_balance.txt", "w") as account_file:
            account_file.write("balance: 0")

def read_commands() -> list:
    """Read args"""
    return sys.argv