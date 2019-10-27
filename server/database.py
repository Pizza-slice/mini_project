import sqlite3
import random
import threading

MAX_READ = 100


class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.connection.row_factory = lambda cursor, row: row[0]  # make the return list and not tuple
        self.cursor = self.connection.cursor()

    def create_database(self):
        command = """CREATE TABLE IF NOT EXISTS account
        (id INTEGER PRIMARY KEY, username Text unique, password TEXT)"""
        self.cursor.execute(command)
        self.connection.commit()

    def create_user(self, info):
        if not self.check_info(info):
            return "missing info"
        else:
            if self.username_available(info["username"]):
                command = """INSERT INTO account VALUES
        (?,?,?)"""
                self.cursor.execute(command, (self.get_new_id(), info["username"], info["password"]))
                self.connection.commit()
                return "success"
            else:
                return "user taken"

    def get_new_id(self):
        command = "SELECT id FROM account"
        new_id = random.randint(1000000, 9999999)
        self.cursor.execute(command)
        id_list = self.cursor.fetchall()
        while new_id in id_list:
            new_id = random.randint(1000000, 9999999)
        return new_id

    def username_available(self, username):
        command = "SELECT username FROM account"
        self.cursor.execute(command)
        usernames = self.cursor.fetchall()
        if username in usernames:
            return False
        else:
            return True

    @staticmethod
    def check_info(info):
        required_information_list = ["username", "password"]
        keys = list(info.keys())
        for required_information in required_information_list:
            if required_information not in keys:
                return False
        return True


class AsycDatabase:
    def __init__(self, file_name):
        self.database = Database(file_name)
        self.lock = threading.Lock()
        self.semaphone_lock = threading.Semaphore(MAX_READ)

    def create_database(self):
        self.database.create_database()

    def create_user(self, info):
        self.lock.acquire()
        for i in range(MAX_READ):
            self.semaphone_lock.acquire()
        self.database.create_user(info)
        for i in range(MAX_READ):
            self.semaphone_lock.release()
        self.lock.release()


def main():
    d = Database("test.db")
    d.create_database()
    print(d.create_user({"username": "2lon is so cool", "password": "12345"}))


if __name__ == '__main__':
    main()
