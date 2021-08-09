import random
import sqlite3


class Database:
    database_name = 'card.s3db'

    def __init__(self):
        self.connection = sqlite3.connect(Database.database_name)
        self.connection.row_factory = sqlite3.Row
        self.create_table()

    # noinspection PyMethodMayBeStatic
    def create_table(self):
        table_ddl = """CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    pin TEXT NOT NULL,
    balance INTEGER DEFAULT 0
)"""
        self.connection.execute(table_ddl)

    def next_customer_account_number(self):
        sql = """SELECT 
    IFNULL(
        MAX(
            CAST(SUBSTR(number, 7, 9) AS INTEGER)
        ), 
        1248
    ) + 1 AS customer_account_number 
FROM card"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        return row['customer_account_number']

    def insert_new_card(self, card):
        insert_ddl = 'INSERT INTO card (number, pin) VALUES (?,?)'
        cursor = self.connection.cursor()
        cursor.execute(insert_ddl, (card.card_number(), card.pin))
        card_id = cursor.lastrowid
        self.connection.commit()
        return card_id

    def update_card(self, card):
        update_ddl = 'UPDATE card SET balance = ? WHERE id = ?'
        cursor = self.connection.cursor()
        cursor.execute(update_ddl, (card.balance, card.card_id))
        self.connection.commit()

    def delete_card(self, card):
        update_ddl = 'DELETE FROM card  WHERE id = ?'
        cursor = self.connection.cursor()
        cursor.execute(update_ddl, [card.card_id])
        self.connection.commit()

    def get_card(self, card_number, pin=None):
        if pin is None:
            sql = "SELECT id, number, pin, balance FROM card WHERE number = ?"
            parameters = [card_number]
        else:
            sql = "SELECT id, number, pin, balance FROM card WHERE number = ? and pin = ?"
            parameters = [card_number, pin]
        cursor = self.connection.cursor()
        cursor.execute(sql, parameters)
        row = cursor.fetchone()

        if row is None:
            return None
        return Card(row)


class Card:
    issuer_identification_number = "400000"

    def __init__(self, database_row=None):
        if database_row is None:
            customer_account_number = format(database.next_customer_account_number(), '09')
            self.account_identifier = f"{Card.issuer_identification_number}{customer_account_number}"
            self.checksum_digit = generate_luhn_digit(self.account_identifier)
            self.pin = format(random.randint(0, 9999), '04')
            self.balance = 0
            self.card_id = database.insert_new_card(self)
        else:
            self.account_identifier = get_account_identifier(database_row['number'])
            self.checksum_digit = get_luhn_digit(database_row['number'])
            self.pin = database_row['pin']
            self.balance = database_row['balance']
            self.card_id = database_row['id']

    def check_pin(self, entered_pin):
        return int(self.pin) == entered_pin

    def card_number(self):
        return f"{self.account_identifier}{self.checksum_digit}"

    # noinspection PyMethodMayBeStatic
    def get_balance(self):
        return self.balance

    def income(self, income):
        self.balance += income
        database.update_card(self)


def bye():
    print("Bye!")
    database.connection.close()
    exit(0)


def get_account_identifier(card_number):
    return card_number[0:len(card_number)-1]


def get_luhn_digit(card_number):
    return int(card_number[-1])


def generate_luhn_digit(account_identifier):
    account_digits = [int(digit) for digit in account_identifier]
    for position in range(0, len(account_digits), 2):
        account_digits[position] *= 2
        if account_digits[position] > 9:
            account_digits[position] -= 9
    module = sum(account_digits) % 10
    if module > 0:
        return 10 - module
    return 0


def check_luhn_digit(card_number):
    return generate_luhn_digit(get_account_identifier(card_number)) == get_luhn_digit(card_number)


# Initialize database
database = Database()

while True:
    print("""1. Create an account
2. Log into account
0. Exit""")

    main_option = int(input(">"))

    if main_option == 0:
        bye()
    elif main_option == 1:
        new_card = Card()
        print("Your card has been created")
        print("Your card number:")
        print(new_card.card_number())
        print("Your card PIN:")
        print(new_card.pin)
        print()
    elif main_option == 2:
        print("Enter your card number:")
        user_card_number = input(">")
        print("Enter your PIN:")
        user_pin = input(">")
        print()
        my_card = database.get_card(user_card_number, user_pin)
        if isinstance(my_card, Card):
            print("You have successfully logged in!")
            while True:
                print()
                print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
                login_option = int(input(">"))
                print()
                if login_option == 1:
                    print(f"Balance: {my_card.get_balance()}")
                elif login_option == 2:
                    print("Enter income:")
                    my_card.income(int(input(">")))
                elif login_option == 3:
                    print("Transfer")
                    print("Enter card number:")
                    destination_card_number = input(">")
                    if not check_luhn_digit(destination_card_number):
                        print("Probably you made a mistake in the card number. Please try again!")
                    else:
                        destination_card = database.get_card(destination_card_number)
                        if not isinstance(destination_card, Card):
                            print("Such a card does not exist.")
                        elif destination_card.card_number() == my_card.card_number():
                            print("Probably you made a mistake in the card number. Please try again!")
                        else:
                            print("Enter how much money you want to transfer:")
                            money_to_transfer = int(input(">"))
                            if money_to_transfer > my_card.get_balance():
                                print("Not enough money!")
                            else:
                                my_card.income(-money_to_transfer)
                                destination_card.income(money_to_transfer)
                elif login_option == 4:
                    database.delete_card(my_card)
                    del my_card
                    print("The account has been closed!")
                    break
                elif login_option == 5:
                    print("You have successfully logged out!")
                    break
                elif login_option == 0:
                    bye()
        else:
            print("Wrong card number or PIN!")
        print()
