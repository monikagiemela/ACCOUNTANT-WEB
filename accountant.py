import sys
import csv

from UTILS.helpers import check_balance, check_quantity, update_balance_file 
from UTILS.helpers import update_store_file
from UTILS.helpers import validate_user_inputs


class Accountant:

    AVAILABLE_COMMANDS = ("transaction", "buy", "sell", "balance", "store", "log", "create_new_manager")

    def __init__(self, commands: list):
        self.commands: list = commands

    def __setattr__(self, name: str, value: str) -> None:
        self.__dict__[name] = value

    def view_account(self) -> str:
        """View current account"""
        return f"Current balance: {check_balance()}"
                   
    def buy(self) -> str:
        """Buy products"""
        # Check if user's commands are correct   
        product, _, quantity, total = validate_user_inputs(self.commands)  
        
        # Check available funds 
        current_balance = int(check_balance())    
        if current_balance < total:        
            sys.exit("Insufficient funds in the account")        
        else:    
            current_balance -= total

        #Write current account balance to current_balance.txt file
        update_balance_file(current_balance)
        
        # Write contents of store.csv file to file_list
        current_store_quantity, file_list = check_quantity(product)
        new_store_quantity = current_store_quantity + quantity
        # Change quantity of the product in the file_list
        if file_list == []:
            file_list.append({"product": product, 
                            "quantity": new_store_quantity})
        else:
            for i in range(len(file_list)):
                if file_list[i]["product"] == product:
                    file_list[i] = {"product": product, "quantity": new_store_quantity}
            file_list.append({"product": product, "quantity": new_store_quantity})
    
        # Write file_list contents to store.csv file
        update_store_file(file_list)
        return f"Bought {product}: {quantity} units"

    def view_storage(self) -> str:
        """View storage"""    
        if len(self.commands) < 3:    
            sys.exit("Please enter product id")          
        # Read store.csv file and print requested products' data
        for command in self.commands[2:]:
            (current_store_quantity, _) = check_quantity(command)
            return f"{command}: {current_store_quantity}"

    def make_transaction(self) -> str:
        """Register a new transaction"""
        try:    
            value = int(self.commands[2])
        except ValueError or IndexError:    
            sys.exit("Please enter value of transaction")
            
        try:    
            comment = str(self.commands[3])
        except ValueError or IndexError:    
            sys.exit("Please enter a comment")

        with open("transactions.csv", "a", newline="") as transactions_file:
            fieldnames = ["transaction", "quantity", "comment"]
            writer = csv.DictWriter(transactions_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({"transaction": self.commands[1], "quantity": value, 
                            "comment": comment})
        
        current_balance = 0
        
        with open("current_balance.txt", "r") as balance_file:
            for line in balance_file:
                if line.startswith("balance:"):
                    line = line.strip().split()
                    current_balance = int(line[1])
                    
        current_balance += value

        #Write current account balance to current_balance.txt file
        update_balance_file(current_balance)
        return " ".join(self.commands)

    def sell(self) -> str:
        """Sell products"""
        # Check if user's commands are correct
        product, price, quantity, total = validate_user_inputs(self.commands)

        # Search for the line in store.txt file where the product is located
        # Write contents of store.txt file to file_list
        try:
            current_store_quantity, file_list = check_quantity(product)
        except TypeError:
            sys.exit("Product not available")

        if current_store_quantity >= quantity:    
            new_store_quantity = current_store_quantity - quantity
            for i in range(len(file_list)):
                if file_list[i]["product"] == product:
                    file_list[i] = {"product": product, "quantity": new_store_quantity}
        else:    
            sys.exit("Insuficiant availability of the requested prodcut")   

        # Write changed file_list to file
        update_store_file(file_list)       
        # Find current account balance
        current_balance = int(check_balance())                    
        current_balance += total 
        #Write current account balance to current_balance.txt file
        update_balance_file(current_balance)
        return f"Sold {product}: {quantity} units"
            
    def view_log(self) -> str:
        """View history of commands"""    
        with open("log.txt", "r") as log_file:    
            return f"{log_file.read()}"