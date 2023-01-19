import sqlite3


class CheckUser(object):
    # Init connection
    def __init__(self, db_path):
        self.__con = sqlite3.connect(db_path)

    # Check for user and password
    def check(self, username: str, password: str):
        cur = self.__con.cursor()
        res = cur.execute(f"SELECT * FROM Connections where Username='{username}' and Password='{password}'")
        if res.fetchone() is None:
            return False
        return True

    # Stop connection
    def __del__(self):
        self.__con.close()