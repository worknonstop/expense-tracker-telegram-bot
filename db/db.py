import os
import sqlite3 as sq


class DataBase:
    def __init__(self):
        self.con = sq.connect(os.path.join('db', 'acc.db'))
        self.cur = self.con.cursor()

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS category(uniqname PRIMARY KEY, name)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY,
        cost INTEGER,
        date DATETIME,
        category_uniqname INTEGER,
        FOREIGN KEY(category_uniqname) REFERENCES category(uniqname)""")
