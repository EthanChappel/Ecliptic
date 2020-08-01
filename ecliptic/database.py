import sqlite3


class Database:
    def __init__(self, name: str):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS schedule
            (rowid INTEGER PRIMARY KEY , start DATETIME UNIQUE, target TEXT, parameters TEXT)'''
        )

    def insert_schedule(self, rowid: int, start: str, target: str, parameters: str):
        self.cursor.execute(
            'INSERT INTO schedule VALUES (?, ?, ?, ?)',
            (rowid, start, target, parameters),
        )
        self.connection.commit()

    def update_schedule(self, rowid: int, start: str, target: str, parameters: str):
        self.cursor.execute(
            'UPDATE schedule SET start=?, target=?, parameters=? WHERE rowid=?',
            (start, target, parameters, rowid),
        )
        self.connection.commit()

    def insert_or_update_schedule(self, rowid: int, start: str, target: str, parameters: str):
        try:
            self.insert_schedule(rowid, start, target, parameters)
        except sqlite3.IntegrityError:
            self.update_schedule(rowid, start, target, parameters)

    def remove_schedule(self, rowid: int):
        self.cursor.execute(
            'DELETE FROM schedule WHERE rowid=?',
            (rowid,),
        )
        self.connection.commit()

    def schedule_max_id(self):
        self.cursor.execute('SELECT MAX(rowid) FROM schedule')
        r = self.cursor.fetchone()[0]
        if not r:
            r = 0
        return r
