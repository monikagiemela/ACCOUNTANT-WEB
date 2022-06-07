import sys
import csv
from app.UTILS.Exception import userError
from accountant import Accountant

class Manager:

    def __init__(self):
        self.username = input("Username: ")
        self.password = input("Password: ")
    
    def __str__(self):
        f"{self.username}"

    def is_manager(self) -> bool:
        """Check if the user is registered"""
        with open("managers.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == self.username and row[1] == self.password:
                    return True 
            return False         

    def create_new_manager(self) -> str:
        """Create a new manager - only a registered user can create a new manager account"""
        new_user_username = input("New user username: ")
        new_user_password = input("New user password: ")
        with open("managers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([new_user_username, new_user_password])
            return f"Created new user: {new_user_username}"
    
    def login_required(func):
        """Make access to Accountant object available only to registered users"""
        def decorated_function(self, commands):
            if not self.is_manager():
                print("#" * 65)
                print(userError("You are not registered. A registered manager can give you access to the service"))
                print("#" * 65)
                sys.exit()
            return func(commands)
        return decorated_function
    
    @login_required
    def start_accountant(commands):
        """Create Accountant objet"""
        accountant = Accountant(commands)
        return accountant