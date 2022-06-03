"""
Napisz program (accountant.py), który będzie rejestrował operacje na koncie firmy i stan magazynu.
Program jest wywoływany w następujący sposób:
a) python run.py transaction <int value> <str comment>
b) python run.py buy <str product id> <int price> <int quantity>
c) python run.py sell <str product id> <int price> <int quantity>
d) python run.py balance
e) python run.py store <str prodcut id 1> <str prodcut id 2> <str prodcut id 3> ...
f) python run.py log
g) python run.py create_new_manager

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

import os
import sys

from accountant import Accountant
from UTILS.helpers import save_to_log, start_database, read_commands

from UTILS.Manager import Manager


def main():
    # Validate args
    commands = read_commands()
    if len(commands) < 2:    
            sys.exit("""\nInvalid command.

Usage:
a) python run.py transaction <int value> <str comment>
b) python run.py buy <str product id> <int price> <int quantity>
c) python run.py sell <str product id> <int price> <int quantity>
d) python run.py balance
e) python run.py store <str prodcut id 1> <str prodcut id 2> <str prodcut id 3> ...
f) python run.py log
g) python run.py create_new_manager

""") 
    
    # Initiate a Manager object
    manager = Manager() 
    
    # If managers.csv file exists check if current user is registered
    if os.path.isfile("managers.csv"):
        # Initiate Accountant obeject if user is registered
        accountant = manager.start_accountant(commands)
    # Create file and register the first user
    else:
        new_username = manager.create_new_manager()
        accountant = Accountant(commands)
        print(new_username)     

    if commands[1] not in accountant.AVAILABLE_COMMANDS:    
            sys.exit("Enter a valid command")
    
    # Check if database already exists - otherwise create file current_balance.txt
    start_database()
    
    # Run the code based on user command
    with open("store.csv", "a", newline='') as store_file:           
        if commands[1] == "buy":
            print(accountant.buy()) 
            print(accountant.view_account())
        elif commands[1] == "transaction":
            print(accountant.make_transaction())
            print(accountant.view_account())                
        elif commands[1] == "sell":    
            print(accountant.sell())
            print(accountant.view_account())           
        elif commands[1] == "balance":    
            print(accountant.view_account())
        elif commands[1] == "store":
            print(accountant.view_storage())   
        elif commands[1] == "log":     
            print(accountant.view_log())
        elif commands[1] == "create_new_manager":
            print(manager.create_new_manager())
        # Add current command to log.txt
        save_to_log(commands)       


if __name__ == "__main__":      
    main()