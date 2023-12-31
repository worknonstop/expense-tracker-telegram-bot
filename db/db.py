import datetime
import os
import sqlite3 as sq
from typing import List


class DataBase:
    def __init__(self):
        self.con = sq.connect(os.path.join('db', 'acc.db'))
        self.cur = self.con.cursor()

    def insert(self, cost: int, category_name: str):
        """Writes the expense to the database"""
        uniqname_object = self.cur.execute("SELECT uniqname FROM category WHERE name = ?", (category_name,))
        uniqname = uniqname_object.fetchone()[0]
        self.cur.execute("INSERT INTO expense (cost, date, category_uniqname) VALUES (?, ?, ?)",
                         (cost, datetime.datetime.now(), uniqname))
        self.con.commit()

    def get_list_categories(self) -> List[str]:
        names = self.cur.execute("SELECT name FROM category")
        return [name[0] for name in names]

    def get_sql_day_expenses(self):
        return self.cur.execute("""
        SELECT c.name, SUM(e.cost) 
        FROM expense e 
        INNER JOIN category c ON e.category_uniqname = c.uniqname 
        WHERE date(e.date) = date('now') 
        GROUP BY c.name""")

    def get_sql_month_expenses(self):
        return self.cur.execute("""
        SELECT c.name, SUM(e.cost)
        FROM expense e
        JOIN category c ON e.category_uniqname = c.uniqname
        WHERE strftime('%Y-%m', e.date) = strftime('%Y-%m', 'now')
        GROUP BY c.name""")

    def get_sql_week_expenses(self):
        return self.cur.execute("""
        SELECT c.name, SUM(e.cost) as total_cost
        FROM expense e
        JOIN category c ON e.category_uniqname = c.uniqname
        WHERE e.date >= date('now', 'weekday 1', '-7 days')
        AND e.date < date('now', '+1 day')
        GROUP BY c.name""")

    def get_sql_five_last(self):
        return self.cur.execute("""
        SELECT c.name, e.cost, e.id
        FROM expense e
        JOIN category c ON e.category_uniqname = c.uniqname
        ORDER BY e.id DESC
        LIMIT 5
        """)

    def delete_sql_entry(self, entry_id):
        query = self.cur.execute("DELETE FROM expense WHERE id = ?", (entry_id,))
        # self.con.commit()
        return query
