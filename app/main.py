"""
created: 2023/02/22 13:14:55 
@author: seraph★vega
contact: admin@pythonspecialops.com
project: Bank Management System (BMS)
metadoc: BMS that connects to sqlite3 database, and tracks client transactions/
license: MIT
"""


import sqlite3
import random
import datetime
import sys


class BMSConnection:
    def __init__(self):
        self.conn = sqlite3.connect('transactions.db')
        self.curr = self.conn.cursor()
        self.create_customer_table()
        self.create_transaction_table()

    def create_customer_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Customer_tb (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT  
            );"""
        self.curr.execute(sql)

    def create_transaction_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Transaction_tb (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            account_number TEXT,
            username TEXT ,
            pin TEXT,
            transaction_date TEXT,
            ledger TEXT,
            balance REAL,
            UNIQUE(username)
            FOREIGN KEY(customer_id) REFERENCES customer_tb(id));
            
            """
        self.curr.execute(sql)

    def save_to_customer_tb(self, data):
        sql = """
        INSERT INTO Customer_tb (first_name, last_name) VALUES (?,?)
        """
        record = (data['first_name'], data['last_name'])
        try:
            self.curr.execute(sql, record)
            self.conn.commit()
        except sqlite3.Error as e:
            SystemExit(e)

    def save_to_transaction_tb(self, data):
        sql = """
        INSERT INTO Transaction_tb (customer_id,account_number,username,pin, transaction_date, ledger, balance)
         VALUES (?,?,?,?,?,?, ?)
        """
        customer_id = self.curr.lastrowid
        username = f"{data['first_name'][0]} {data['last_name']}"
        transaction_date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        record = (customer_id,
                  data['account_number'],
                  username,
                  data['pin'],
                  transaction_date,
                  data['transaction'],
                  data['balance']
                  )
        try:
            self.curr.execute(sql, record)
            self.conn.commit()
        except sqlite3.Error as e:
            SystemExit(e)


class BMSApplication:
    def __init__(self, connection):
        self.connection = connection

    def open_account(self):
        unique_user = False
        while not unique_user:
            first_name = input('Enter your first name:\n> ')
            last_name = input('Enter your last name:\n> ')
            username = input('Enter a unique username:\n> ')
            while True:
                initial_deposit = input('How much would you like to initially deposit?:\n> ')
                if not initial_deposit.isdigit() and float(initial_deposit) <= 0:
                    print('Invalid amount!')
                    continue
                else:
                    break
            sql = """
            INSERT INTO Customer_tb (first_name, last_name) VALUES (?,?)
            """
            try:
                self.connection.curr.execute(sql, (first_name, last_name))
            except sqlite3.Error as e:
                SystemExit(e)
            while True:
                pin = input('Enter a 4-digit PIN:\n> ')
                if not pin.isdigit() or len(pin) != 4:
                    print('Invalid PIN, try again!')
                else:
                    break
            account_number = f'00000{random.randint(100000, 999999)}'
            customer_id = self.connection.curr.lastrowid

            transaction_date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            ledger = f'+{float(initial_deposit)}'
            record = (customer_id, account_number, username, pin, transaction_date, ledger, initial_deposit)
            sql = """
            INSERT INTO Transaction_tb (customer_id,account_number,username,pin,transaction_date, ledger, balance)
            VALUES (?,?,?,?,?,?, ?)
            """
            try:
                self.connection.curr.execute(sql, record)
            except sqlite3.IntegrityError as e:
                print('Someone with that username already exists, please try again!')
                continue

            self.connection.conn.commit()
            print('New account successfully created!')
            unique_user = True

    def deposit_funds(self):
        while True:
            pin = input('Please enter your PIN:\n> ')
            sql = """
            SELECT * FROM Transaction_tb WHERE pin = ?;                
            """
            record = self.connection.curr.execute(sql, (pin,)).fetchone()

            #  balance = self.connection.curr.execute(sql, (pin,)).fetchone()
            if record is None:
                print('Your account could not be located, please try again!')
                continue
            else:
                break
        new_record = tuple(record)
        current_balance = new_record[-1]
        deposit = float(input('How much would you like to deposit:\n> '))
        updated_balance = current_balance + deposit
        sql = """
        INSERT INTO Transaction_tb (customer_id,account_number,username,pin,transaction_date, ledger, balance)
        VALUES (?,?,?,?,?,?, ?)
        """
        customer_id = record[1]
        account_number = record[2]
        username = record[3]
        pin = record[4]
        transaction_date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        ledger = f'+{deposit}'
        new_record = (customer_id, account_number, username, pin, transaction_date, ledger, updated_balance)
        self.connection.curr.execute(sql, new_record)
        self.connection.conn.commit()
        print(f'Transaction completed, new balance: ${updated_balance}')

    def withdraw_funds(self):
        while True:
            pin = input('Please enter your PIN:\n> ')
            sql = """
            SELECT * FROM Transaction_tb WHERE pin = ?;            
            """
            record = self.connection.curr.execute(sql, (pin,)).fetchone()
            if record is None:
                print('Your account could not be located, please try again!')
                continue
            else:
                break
        new_record = tuple(record)
        current_balance = new_record[-1]
        while True:
            withdraw = float(input('How much would you like to withdraw:\n> '))
            if withdraw > current_balance:
                print(f'Insufficient funds!\nAvailable balance: ${current_balance}')
                continue
            else:
                updated_balance = current_balance - withdraw
                sql = """
                INSERT INTO Transaction_tb (customer_id,account_number,username,pin,transaction_date, ledger, balance)
                VALUES (?,?,?,?,?,?, ?)
                """
                customer_id = record[1]
                account_number = record[2]
                username = record[3]
                pin = record[4]
                transaction_date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                ledger = f'-{withdraw}'
                new_record = (customer_id, account_number, username, pin, transaction_date, ledger, updated_balance)
                self.connection.curr.execute(sql, new_record)
                self.connection.conn.commit()
                print(f'Transaction completed, new balance: ${updated_balance}')
            break

    def check_balance(self):
        while True:
            pin = input('Please enter your PIN:\n> ')
            sql = """
            SELECT balance FROM Transaction_tb WHERE pin = ?;
            """
            balance = self.connection.curr.execute(sql, (pin,)).fetchone()
            if balance is None:
                print('Your account could not be located, please try again!')
                continue
            else:
                break
        balance = float(balance[0])
        sql = "SELECT username from Transaction_tb WHERE pin = ?"
        username = self.connection.curr.execute(sql, (pin,)).fetchone()[0]
        print(f'Customer: {username}')
        print(f'Balance: ${balance}')

    def delete_account(self):
        while True:
            pin = input('Please enter your PIN:\n> ')
            sql = """
            SELECT id FROM Transaction_tb WHERE pin = ?;
            """
            customer_id = self.connection.curr.execute(sql, (pin,)).fetchone()[0]

            if customer_id is None:
                print('Your account could not be located, please try again!')
                continue
            else:
                break

        sql1 = """
        DELETE FROM Transaction_tb WHERE id = ?;
        """
        sql2 = """
          DELETE FROM Customer_tb WHERE id = ?;
        """
        self.connection.curr.execute(sql1, (customer_id,))
        self.connection.curr.execute(sql2, (customer_id,))
        self.connection.conn.commit()
        print("Account has been deleted!")

    def display_menu(self):
        while True:
            print("""BANK MANAGEMENT SYSTEM:
                    
   1. OPEN NEW ACCOUNT
   2. CHECK BALANCE 
   3. DEPOSIT FUNDS
   4. WITHDRAW FUNDS
   5. DELETE ACCOUNT
   6. EXIT
                    """)
            user_choice = input('Make a selection:\n> ')
            if not user_choice.isdigit() or user_choice not in '123456':
                print('Invalid input, please try again!', file=sys.stderr)
                continue
            else:
                break
        user_choice = int(user_choice)
        if user_choice == 1:
            self.open_account()
        elif user_choice == 2:
            self.check_balance()
        elif user_choice == 3:
            self.deposit_funds()
        elif user_choice == 4:
            self.withdraw_funds()
        elif user_choice == 5:
            self.delete_account()
        elif user_choice == 6:
            print('Goodbye!')
            sys.exit()


def main():
    conn = BMSConnection()
    app = BMSApplication(conn)
    while True:
        app.display_menu()


if __name__ == '__main__':
    main()
