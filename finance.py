import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import datetime
import os

class Database:
    def __init__(self , db):
        self.__db_name__ = db
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS [transactions](
                            [id] INT PRIMARY KEY NOT NULL UNIQUE, 
                            [amount] REAL NOT NULL, 
                            [type] TEXT, 
                            [date] TEXT, 
                            [description] TEXT);
                            """
                            )
        
        self.connection.commit()
        self.connection.close()

    def add_transaction(self ,id ,  amount , typeT , description):
        self.connection = sqlite3.connect(self.__db_name__)
        self.cursor = self.connection.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO transactions VALUES(?,?,?,?,?)", (id , amount , typeT , date , description))
        self.connection.commit()
        self.connection.close()

    def get_all_transactions(self):
        self.connection = sqlite3.connect(self.__db_name__)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM transactions")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

db = None

if not os.path.isfile('finance.db'):
    db = Database('finance.db')
    db.add_transaction(1 , 200.5 , "income" , "salary")
else: 
    db = Database('finance.db')

print(db.get_all_transactions())
