import datetime
import os
import sqlite3 as sq
from typing import List


class DataBase:
    def __init__(self):
        self.con = sq.connect(os.path.join('db', 'acc.db'))
        self.cur = self.con.cursor()

    def insert_expense(self, cost: int, category_uniqname: str):
        self.cur.execute("SELECT * FROM category WHERE uniqname = ?", (category_uniqname,))
        self.cur.execute("INSERT INTO expenses (cost, date, category_uniqname) VALUES (?, ?, ?)",
                         (cost, datetime.datetime.now(), category_uniqname))
        self.con.commit()

    def get_category_names(self) -> List[str]:
        names = self.cur.execute("SELECT name FROM category")
        return names.fetchall()
