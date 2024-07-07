import sqlite3
import time


class RelapseDB:
    def __init__(self, db_name="relapse.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS relapses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp INTEGER NOT NULL
                )
            """
            )

    def add_relapse(self):
        with self.conn:
            self.conn.execute(
                "INSERT INTO relapses (timestamp) VALUES (?)", (int(time.time()),)
            )

    def get_last_relapse(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp FROM relapses ORDER BY timestamp DESC LIMIT 1")
        return cursor.fetchone()

    def get_relapses_in_period(self, start, end):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT timestamp FROM relapses WHERE timestamp BETWEEN ? AND ?",
            (start, end),
        )
        return cursor.fetchall()

    def get_all_relapses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp FROM relapses")
        return cursor.fetchall()
