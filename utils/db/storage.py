from sqlite3 import connect

class DatabaseManager:
    def __init__(self, path):
        self.conn = connect(path)
        self.conn.execute('pragma foreign_keys=ON')
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.query(
            'CREATE TABLE IF NOT EXISTS questions (cid int, question text)')

    def query(self, arg, values=None):
        if values is None:
            self.cursor.execute(arg)
        else:
            self.cursor.execute(arg, values)
        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values is None:
            self.cursor.execute(arg)
        else:
            self.cursor.execute(arg, values)
        return self.cursor.fetchone()

    def fetchall(self, arg, values=None):
        if values is None:
            self.cursor.execute(arg)
        else:
            self.cursor.execute(arg, values)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()