"""
created: 2023/02/22 13:21:42 
@author: seraph★vega
contact: admin@pythonspecialops.com
project: Bank Management System (BMS)
metadoc: BMS that connects to a sqlite3 database
license: MIT
"""

import sqlite3
import datetime


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
