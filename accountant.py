"""
Napisz program (accountant.py), który będzie rejestrował operacje na koncie firmy i stan magazynu.
Program jest wywoływany w następujący sposób:
a) python saldo.py <plik><int wartosc> <str komentarz>
b) python sprzedaz.py <plik><str identyfikator produktu> <int cena> <int liczba sprzedanych>
c) python zakup.py <plik> <str identyfikator produktu> <int cena> <int liczba zakupionych>
d) python konto.py <plik>
e) python magazyn.py <plik><str identyfikator produktu 1> <str identyfikator produktu 2> <str identyfikator produktu 3> ...
f) python przeglad.py <plik>

Działanie programu będzie zależne od podanych argumentów
Niezależnie od trybu program zawsze będzie działał w następujący sposób
I. Program pobierze rodzaj akcji (ciąg znaków). Dozwolone akcje to "saldo", zakup", "sprzedaż". Jeśli użytkownik wprowadzi inną akcję, program powinien zwrócić błąd i zakończyć działanie.
saldo: program pobiera dwie linie: zmiana na koncie firmy wyrażona w groszach (int) (może być ujemna) oraz komentarz do zmiany (str)
zakup: program pobiera trzy linie: identyfikator produktu (str), cena jednostkowa (int) i liczba sztuk (int). Program odejmuje z salda cenę jednostkową pomnożoną przez liczbę sztuk. Jeśli saldo po zmianie jest ujemne, cena jest ujemna bądź liczba sztuk jest mniejsza od zero program zwraca błąd. Program podnosi stan magazynowy zakupionego towaru
sprzedaż: program pobiera trzy linie: identyfikator produktu (str), cena jednostkowa (int), liczba sztuk (int). Program dodaje do salda cenę jednostkową pomnożoną razy liczbę sztuk. Jeśli na magazynie nie ma wystarczającej liczby sztuk, cena jest ujemna bądź liczba sztuk sprzedanych jest mniejsza od zero program zwraca błąd. Program obniża stan magazynowy zakupionego towaru.
stop: program przechodzi do kroku IV
II. Program zapamiętuje każdą wprowadzoną linię
III. Program wraca do kroku I
IV. W zależności od wywołania:
a) b) c) program dodaje do historii podane argumenty tak, jakby miały być wprowadzone przez standardowe wejście, przechodzi do kroku V
d) program wypisuje na standardowe wyjście stan konta po wszystkich akcjach, kończy działanie
e) program wypisuje stany magazynowe dla podanych produktów, w formacie: <id produktu>: <stan> w nowych liniach i kończy działanie:
f) Program wypisuje wszystkie akcje zapisane pod indeksami w zakresie [od, do] (zakresy włącznie)
V. Program wypisuje wszystkie podane parametry w formie identycznej, w jakiej je pobrał.

"""

import sys
import csv

from helpers import check_balance, check_quantity, update_balance_file 
from helpers import update_store_file, save_to_log
from helpers import validate_user_inputs, start_database, read_commands



AVAILABLE_COMMANDS = ("transaction", "buy", "sell", "balance", "store", "log")

commands = read_commands()

def main():
    
    # Check if database already exists - otherwise create file current_balance.txt
    start_database()
    
    # Run the code based on user command
    with open("store.csv", "a", newline='') as store_file:
        if len(commands) < 2:    
            sys.exit("""\nEnter the right commands.

Run the program as follows:
a) python accountant.py transaction <int value> <str comment>
b) python accountant.py buy <str product id> <int price> <int quantity>
c) python accountant.py sell <str product id> <int price> <int quantity>
d) python accountant.py balance
e) python accountant.py store <str prodcut id 1> <str prodcut id 2> <str prodcut id 3> ...
f) python accountant.py log
""")         

        if commands[1] not in AVAILABLE_COMMANDS:    
            sys.exit("Enter a valid command")   
        elif commands[1] == "buy":
            buy() 
            view_account()  
        elif commands[1] == "transaction":
            make_transaction()
            view_account()                
        elif commands[1] == "sell":    
            sell()
            view_account()           
        elif commands[1] == "balance":    
            view_account()
        elif commands[1] == "store":
            view_storage()   
        elif commands[1] == "log":     
            # Add current command to log.txt
            view_log()
        save_to_log()       

"View current account"
def view_account():
    # Add current command to log.txt
    print(f"Current balance: {check_balance()}")
                   
"Buy products"
def buy():
    # Check if user's commands are correct   
    product, price, quantity, total = validate_user_inputs()  
    
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
        for row in file_list:
            if row["product"] == product:
                row = {"product": product, "quantity": new_store_quantity}
            else:
                file_list.append({"product": product, "quantity": new_store_quantity})     
    # Write file_list contents to store.csv file
    update_store_file(file_list)

"View storage"
def view_storage():    
    if len(commands) < 3:    
        sys.exit("Please enter product id")          
    # Read store.csv file and print requested products' data
    for command in commands[2:]:
        (current_store_quantity, file_list) = check_quantity(command)
        print(f"{command}: {current_store_quantity}")
    #with open("store.csv", "r", newline="") as store_file:
    #    reader = csv.DictReader(store_file)
    #    for row in reader:   
    #        for command in commands[2:]:    
    #            if row["product"] == command:
    #                print(f"{row['product']}: {row['quantity']}")

"Register a new transaction"
def make_transaction():  
    try:    
        value = int(commands[2])
    except ValueError or IndexError:    
        sys.exit("Please enter value of transaction")
        
    try:    
        comment = str(commands[3])
    except ValueError or IndexError:    
        sys.exit("Please enter a comment")

    with open("transactions.csv", "a", newline="") as transactions_file:
        fieldnames = ["transaction", "quantity", "comment"]
        writer = csv.DictWriter(transactions_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"transaction": commands[1], "quantity": value, 
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
    print(" ".join(commands))

"Sell products"
def sell():
    # Check if user's commands are correct
    product, price, quantity, total = validate_user_inputs()

    # Search for the line in magazyn.txt file where the product is located
    # Write contents of magazyn.txt file to file_dict
    try:
        current_store_quantity, file_list = check_quantity(product)
    except TypeError:
        sys.exit("Product not available")

    if current_store_quantity >= quantity:    
        new_store_quantity = current_store_quantity - quantity
        for row in file_list:
            if row["product"] == product:
                row = {"product": product, "quantity": new_store_quantity}
    else:    
        sys.exit("Insuficiant availability of the requested prodcut")   

    # Print file_dict contents to file
    update_store_file(file_list)       
    # Find current account balance
    current_balance = int(check_balance())                    
    current_balance += total 
    #Write current account balance to konto.txt file
    update_balance_file(current_balance)
        
"View history of commands"
def view_log():    
    with open("log.txt", "r") as log_file:    
        print(log_file.read(), sep="/n")
    sys.exit()


if __name__ == "__main__":      
    main()