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


AVAILABLE_COMMANDS = ("saldo", "zakup", "sprzedaż", "konto", "magazyn", "przegląd")
commands = sys.argv

def main():
    
    # Check if konto.txt file exists
    if os.path.isfile("konto.txt"):
    
        print()
        account()
 
    # The doesn't exist - create a file and initiate account ballance info
    else:

        with open("konto.txt", "w") as account_file:

            account_file.write("saldo: 0")
    
    # Execute code based on user command
    with open("magazyn.txt", "a"):

        if len(commands) < 2:
            
            print("Podaj nazwę komendy i odpowiednie parametry")
            quit()

        if commands[1] not in AVAILABLE_COMMANDS:
            
            print("Podaj poprawną komendę")
            quit()

        if commands[1] == "zakup":

            buy()
            # Add current command to log.txt
            save_to_log()
            account()
          
        if commands[1] == "saldo":

            saldo()
            # Add current command to log.txt
            save_to_log()
            account()
                         
        if commands[1] == "sprzedaż":
            
            sell()
            # Add current command to log.txt
            save_to_log()
            account()
                    
        if commands[1] == "konto":
            
            account()
            # Add current command to log.txt
            save_to_log()
        
        if commands[1] == "magazyn":

            view_storage()
            # Add current command to log.txt
            save_to_log()
            account()
            
        if commands[1] == "przegląd":
            
            # Add current command to log.txt
            save_to_log()
            view_log()
               
    
"View current account"
def account():

    # Add current command to log.txt
    save_to_log()

    with open("konto.txt", "r") as account_file:
            
        for line in account_file:
            
            if line.startswith("saldo:"):
                
                line = line.strip().split()
                print(f"Saldo konta: {line[1]}")
       
            
"Buy products"
def buy():

    try:
        
        product = str(commands[2])
    
    except ValueError or IndexError:
        
        print("Podaj indentyfikator produktu")
    
    try:
        
        price = int(commands[3])
    
    except ValueError or IndexError:
        
        print("Podaj cenę za sztukę w groszach")
        quit()
    
    try:
        
        purchase_quantity = int(commands[4])
    
    except ValueError or IndexError:
        
        print("Podaj ilość zakupionego produktu")
          
    
    if price < 1 or purchase_quantity < 1:
        
        print("Cena ani ilość nie mogą być mniejsze niż 1") 
        quit()
    
    # Total purchase value
    total = price * purchase_quantity
  
    # Check available funds 
    current_account = 0

    
    with open("konto.txt", "r") as account_file:
        
        for line in account_file:
            
            if line.startswith("saldo:"):
                
                line = line.strip().split()
                current_account = int(line[1])
                
                if current_account < total:
                    
                    print("Brak wystarczającej ilości środków na koncie")
                    quit()
                
                else:
                    
                    current_account -= total

    with open("konto.txt", "w") as account_file:
        account_file.write(f"saldo: {current_account}")
    
    # Print magazyn.txt file contents to a string temp_file replacing the changed line with new_line
    temp_file = ""
    product_in_file = False
    
    with open("magazyn.txt", "r") as store_file:
        
        # Check if product is already in the store and fetch its quantity
        for line in store_file:

            if line.startswith(product):
                
                split_line = line.strip().split()
                store_quantity = int(split_line[1])
                new_store_quantity = store_quantity + purchase_quantity
                new_line = f"{product} {new_store_quantity}\n"
                temp_file += new_line
                product_in_file = True
            
            else:
                temp_file += f"{line}\n"
        
        if not product_in_file:
            
            temp_file += f"{product} {purchase_quantity}\n"
           
    # Print temp_file contents to file
    with open("magazyn.txt", "w") as store_file:
        
        store_file.write(temp_file)
       
    with open("tranzakcje.txt", "a") as transactions_file:
        
        transaction_str = " ". join(commands[1: ])
        transactions_file.write(transaction_str + "\n")
    
    print(" ".join(commands))
 

"View storage"
def view_storage():
    
    if len(commands) < 3:
        
        print("Podaj id produktu")
        quit()
    
    # Read magazyn.txt file and print requested products' data
    with open("magazyn.txt", "r") as store_file:
        #print(store_file.read())
            
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
        
        print("Podaj kwotę w groszach")
        
    try:
        
        comment = str(commands[3])
    
    except ValueError or IndexError:
        
        print("Podaj komantarz do zmiany salda")

    with open("tranzakcje.txt", "a") as transactions_file:
        
        transactions_file.write(f"{commands[1]} {value} {comment}\n")
    
    current_account = 0
    
    with open("konto.txt", "r") as account_file:
        
        for line in account_file:
            
            if line.startswith("saldo:"):
                
                line = line.strip().split()
                current_account += int(line[1])
                
    current_account += value

    with open("konto.txt", "w") as account_file:

        account_file.write(f"saldo: {current_account}")
   
    print(" ".join(commands))


"Save current command to log.txt - helper function"
def save_to_log():
    
    with open("log.txt", "a") as log_file:

        commands_str = " ".join(commands)
        log_file.write(commands_str + "\n")


"Sell products"
def sell():

    try:
        
        product = str(commands[2])
    
    except ValueError or IndexError:
        
        print("Podaj indentyfikator produktu")
    
    try:
        
        price = int(commands[3])
    
    except ValueError or IndexError:
        
        print("Podaj cenę za sztukę w groszach")
        quit()
    
    try:
        
        sell_quantity = int(commands[4])
    
    except ValueError or IndexError:
        
        print("Podaj ilość sprzedanego produktu")
        

    total = price * sell_quantity

    if price < 1 or sell_quantity < 1:
        
        print("Cena ani ilość nie mogą być mniejsze niż 1") 
        quit()

    # Check availability of the product
    new_store_quantity = 0

    # Print file contents to string and replace the changed line with new_line
    new_line = f"{product} {new_store_quantity}\n"
    temp_file = ""
    
    with open("magazyn.txt", "r") as store_file:
        
        for line in store_file:    
            
            if line.startswith(product):
                
                line = line.strip().split()
                current_store_quantity = int(line[1])
                
                if current_store_quantity >= sell_quantity:
                    
                    new_store_quantity = current_store_quantity - sell_quantity
                    temp_file += new_line
                
                else:
                    
                    print("Brak wystarczającej ilości produktu w magazynie")
              
            else:
                temp_file += f"{line}\n"


    # Print temp_file contents to file
    with open("magazyn.txt", "w") as store_file:
        
        store_file.write(temp_file)
       
    # Find current account balance
    current_account = 0
    
    with open("konto.txt", "r") as account_file:
        
        for line in account_file:
            
            if line.startswith("saldo:"):
                
                line = line.strip().split()
                current_account = int(line[1])
                
    current_account += total

    # Write current account balance to konto.txt file
    with open("konto.txt", "w") as account_file:
        
        account_file.write(f"saldo: {current_account}")
   
    # Write current transaction to tranzakcje.txt file
    with open("tranzakcje.txt", "a") as transactions_file:
        
        transaction_str = " ". join(commands[1: ])
        transactions_file.write(transaction_str + "\n")
    
    print(" ".join(commands))


"View history of commands"
def view_log():
    
    # Print all historical commands
    with open("log.txt", "r") as log_file:
        
        print(log_file.read(), sep="/n")
    
    quit()


if __name__ == "__main__":      
    main()