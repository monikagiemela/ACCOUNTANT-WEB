"""
Napisz program (accountant.py), który będzie rejestrował operacje na koncie firmy i stan magazynu.
Program jest wywoływany w następujący sposób:
a) python accountant.py saldo <int wartosc> <str komentarz>
b) python accountant.py sprzedaż <str identyfikator produktu> <int cena> <int liczba sprzedanych>
c) python accountant.py zakup <str identyfikator produktu> <int cena> <int liczba zakupionych>
d) python accountant.py konto
e) python accountant.py magazyn <str identyfikator produktu 1> <str identyfikator produktu 2> <str identyfikator produktu 3> ...
f) python accountant.py przegląd

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
import os.path


AVAILABLE_COMMANDS = ("saldo", "zakup", "sprzedaż", "konto", "magazyn", 
"przegląd")
commands = sys.argv

def main():
    
    # Check if database already exists - otherwise create file konto.txt
    start_database()
    
    # Execute code based on user command
    with open("magazyn.txt", "a"):

        if len(commands) < 2:    
            sys.exit("""\nPodaj nazwę komendy i odpowiednie parametry.

Program jest wywoływany w następujący sposób:
a) python accountant.py saldo <int wartosc> <str komentarz>
b) python accountant.py sprzedaż <str identyfikator produktu> <int cena> <int liczba sprzedanych>
c) python accountant.py zakup <str identyfikator produktu> <int cena> <int liczba zakupionych>
d) python accountant.py konto
e) python accountant.py magazyn <str identyfikator produktu 1> <str identyfikator produktu 2> <str identyfikator produktu 3> ...
f) python accountant.py przegląd""")         

        if commands[1] not in AVAILABLE_COMMANDS:    
            sys.exit("Podaj poprawną komendę")   
        elif commands[1] == "zakup":
            buy() 
            view_account()  
        elif commands[1] == "saldo":
            saldo()
            view_account()                
        elif commands[1] == "sprzedaż":    
            sell()
            view_account()           
        elif commands[1] == "konto":    
            view_account()
        elif commands[1] == "magazyn":
            view_storage()   
        elif commands[1] == "przegląd":     
            # Add current command to log.txt
            view_log()
        save_to_log()       
    
"View current account"
def view_account():
    # Add current command to log.txt
    print(f"Saldo konta: {check_balance()}")
                   
"Buy products"
def buy():
    # Check if user's commands are correct   
    product, price, quantity, total = validate_user_inputs()  
    
    # Check available funds 
    current_account = int(check_balance())    
    if current_account < total:        
        sys.exit("Brak wystarczającej ilości środków na koncie")        
    else:    
        current_account -= total

    #Write current account balance to konto.txt file
    update_konto_file(current_account)
    
    # Write contents of magazyn.txt file to file_dict
    try:
        current_store_quantity, file_dict = check_quantity(product)
    except TypeError:
        file_dict = {}
    
    new_store_quantity = current_store_quantity + quantity
    # Change quantity of the product in the file_dict
    file_dict[product] = new_store_quantity
           
    # Write file_dict contents to magazyn.txt file
    update_magazyn_file(file_dict)
          
    # Write current transaction to tranzakcje.txt file
    update_tranzakcje_file()    
 
"View storage"
def view_storage():    
    if len(commands) < 3:    
        sys.exit("Podaj id produktu")          
    # Read magazyn.txt file and print requested products' data
    with open("magazyn.txt", "r") as store_file:       
        for line in store_file:   
            line = line.strip()
            for command in commands[2:]:    
                if line.startswith(command):    
                    searched_line = line.split()
                    print(": ".join(searched_line))

"Register a new transaction"
def saldo():  
    try:    
        value = int(commands[2])
    except ValueError or IndexError:    
        sys.exit("Podaj kwotę w groszach")
        
    try:    
        comment = str(commands[3])
    except ValueError or IndexError:    
        sys.exit("Podaj komantarz do zmiany salda")

    with open("tranzakcje.txt", "a") as transactions_file:    
        transactions_file.write(f"{commands[1]} {value} {comment}\n")
    
    current_account = 0
    
    with open("konto.txt", "r") as account_file:   
        for line in account_file:    
            if line.startswith("saldo:"):    
                line = line.strip().split()
                current_account += int(line[1])
                
    current_account += value

    #Write current account balance to konto.txt file
    update_konto_file(current_account)
    print(" ".join(commands))

"Save current command to log.txt - helper function"
def save_to_log():  
    with open("log.txt", "a") as log_file:
        commands_str = " ".join(commands)
        log_file.write(commands_str + "\n")

"Sell products"
def sell():
    # Check if user's commands are correct
    product, price, quantity, total = validate_user_inputs()

    # Search for the line in magazyn.txt file where the product is located
    # Write contents of magazyn.txt file to file_dict
    try:
        current_store_quantity, file_dict = check_quantity(product)
    except TypeError:
        sys.exit("Brak produktu w magazynie")

    if current_store_quantity >= quantity:    
        new_store_quantity = current_store_quantity - quantity
        file_dict[product] = new_store_quantity
    else:    
        sys.exit("Brak wystarczającej ilości produktu w magazynie")   

    # Print file_dict contents to file
    update_magazyn_file(file_dict)
       
    # Find current account balance
    current_account = int(check_balance())                 
    
    current_account += total 
    #Write current account balance to konto.txt file
    update_konto_file(current_account)
    
    # Write current transaction to tranzakcje.txt file
    update_tranzakcje_file()       

"View history of commands"
def view_log():    
    with open("log.txt", "r") as log_file:    
        print(log_file.read(), sep="/n")
    sys.exit()

"Helper function - check if database exists"
def start_database():
    # Check if konto.txt file exists
    if os.path.isfile("konto.txt"):
        print()
    # konto.txt file doesn't exist - create a file and initiate account ballance info
    else:
        with open("konto.txt", "w") as account_file:
            account_file.write("saldo: 0")

"Helper function - check if user entered correct commands"
def validate_user_inputs():
    try:    
        product = str(commands[2]) 
    except ValueError or IndexError:    
        print("Podaj indentyfikator produktu")
    
    try:    
        price = int(commands[3]) 
    except ValueError or IndexError:    
        sys.exit("Podaj cenę za sztukę w groszach")
          
    try:    
        quantity = int(commands[4]) 
    except ValueError or IndexError:    
        sys.exit("Podaj ilość produktu")
        
    total = price * quantity

    if price < 1 or quantity < 1:    
        sys.exit("Cena ani ilość nie mogą być mniejsze niż 1") 
    return (product, price, quantity, total)

"Helper function - update tranzakcje.txt file"
def update_tranzakcje_file():
    with open("tranzakcje.txt", "a") as transactions_file:    
        transaction_str = " ". join(commands[1: ])
        transactions_file.write(transaction_str + "\n")
    print(" ".join(commands))

"Helper function - update konto.txt file"
def update_konto_file(current_account):
    with open("konto.txt", "w") as account_file:    
        account_file.write(f"saldo: {current_account}")

"Helper function - update magazyn.txt file"
def update_magazyn_file(file_dict):
    with open("magazyn.txt", "w") as store_file:
        for product, value in file_dict.items():
            store_file.write(f"{product} {value}\n")

"Helper function - check account balance"
def check_balance():
    with open("konto.txt", "r") as account_file:        
        for line in account_file:    
            if line.startswith("saldo:"):    
                line = line.strip().split()
                return line[1]

"Check quantity of product in the store"
def check_quantity(product):
    # Write file contents to the file_dict
    file_dict = {}
    current_store_quantity = 0
    with open("magazyn.txt", "r") as store_file:
        if store_file != "":
            for line in store_file:
                line = line.strip().split()
                file_dict[line[0]] = int(line[1]) 
                if line[0] == product:  
                    current_store_quantity = int(line[1])                  
    return (current_store_quantity, file_dict) 

if __name__ == "__main__":      

    main()