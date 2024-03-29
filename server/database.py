import random
import sqlite3
import string
import threading

MAX_READ = 100


class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.connection.row_factory = lambda cursor, row: row[0]  # make the return list and not tuple
        self.cursor = self.connection.cursor()

    def create_database(self):
        command = """CREATE TABLE IF NOT EXISTS account
        (id INTEGER PRIMARY KEY,auth_code TEXT unique, username Text unique, password TEXT)"""
        self.cursor.execute(command)
        self.connection.commit()

    def get_auth_code(self, username):
        command = "SELECT auth_code FROM account WHERE username=?"
        self.cursor.execute(command, (username,))
        return self.cursor.fetchall()[0]

    def check_user(self, username, password):
        command = "SELECT username FROM account"
        self.cursor.execute(command)
        user_list = self.cursor.fetchall()
        if username not in user_list:
            return False, "username or password does not match"
        else:
            command = "SELECT password FROM account WHERE username=?"
            self.cursor.execute(command, (username,))
            database_password = self.cursor.fetchall()[0]
            if database_password == password:
                return True, "OK"
            else:
                return False, "username or password does not match"

    def create_user(self, username, passwrod):
        if self.username_available(username):
            command = """INSERT INTO account VALUES
    (?,?,?,?)"""
            self.cursor.execute(command,
                                (self.get_new_id(), self.get_new_auth_code(), username, passwrod))
            self.connection.commit()
            return True, "user created successfully"
        else:
            return False, "username taken"

    def get_new_id(self):
        command = "SELECT id FROM account"
        new_id = random.randint(1000000, 9999999)
        self.cursor.execute(command)
        id_list = self.cursor.fetchall()
        while new_id in id_list:
            new_id = random.randint(1000000, 9999999)
        return new_id

    def get_new_auth_code(self):
        command = "SELECT auth_code FROM account"
        new_auth_code = self.random_string()
        self.cursor.execute(command)
        code_list = self.cursor.fetchall()
        while new_auth_code in code_list:
            new_auth_code = self.random_string()
        return new_auth_code

    def username_available(self, username):
        command = "SELECT username FROM account"
        self.cursor.execute(command)
        usernames = self.cursor.fetchall()
        if username in usernames:
            return False
        else:
            return True

    def authentication_user(self, auth_code):
        command = "SELECT auth_code FROM account"
        self.cursor.execute(command)
        auth_code_list = self.cursor.fetchall()
        if auth_code in auth_code_list:
            command = "SELECT id FROM account WHERE auth_code=?"
            self.cursor.execute(command, (auth_code,))
            user_id = self.cursor.fetchall()[0]
            return True, user_id
        else:
            return False, None

    def get_id_list(self, user_id):
        command = "SELECT id FROM account"
        self.cursor.execute(command)
        id_list = self.cursor.fetchall()
        id_list.remove(user_id)
        return id_list

    def get_username_from_id(self, user_id):
        command = "SELECT username FROM account WHERE id=?"
        self.cursor.execute(command, (user_id,))
        username = self.cursor.fetchall()[0]
        return username

    @staticmethod
    def check_info(info):
        required_information_list = ["username", "password"]
        keys = list(info.keys())
        for required_information in required_information_list:
            if required_information not in keys:
                return False
        return True

    @staticmethod
    def random_string(string_length=10):
        """Generate a random string of fixed length """
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(string_length))


class AsycDatabase:
    def __init__(self, file_name):
        self.database = Database(file_name)
        self.lock = threading.Lock()
        self.semaphone_lock = threading.Semaphore(MAX_READ)

    def create_database(self):
        self.database.create_database()

    def create_user(self, username, passwrod):
        self.lock.acquire()
        for i in range(MAX_READ):
            self.semaphone_lock.acquire()
        success, massage = self.database.create_user(username, passwrod)
        for i in range(MAX_READ):
            self.semaphone_lock.release()
        self.lock.release()
        return success, massage

    def check_user(self, username, password):
        self.semaphone_lock.acquire()
        success, massage = self.database.check_user(username, password)
        self.semaphone_lock.release()
        return success, massage

    def get_auth_code(self, username):
        self.semaphone_lock.acquire()
        auth_code = self.database.get_auth_code(username)
        self.semaphone_lock.release()
        return auth_code

    def get_id_list(self, user_id):
        self.semaphone_lock.acquire()
        id_list = self.database.get_id_list(user_id)
        self.semaphone_lock.release()
        return id_list

    def authentication_user(self, auth_code):
        self.semaphone_lock.acquire()
        authenticated, user_id = self.database.authentication_user(auth_code)
        self.semaphone_lock.release()
        return authenticated, user_id

    def get_username_from_id(self, user_id):
        self.semaphone_lock.acquire()
        username = self.database.get_username_from_id(user_id)
        self.semaphone_lock.release()
        return username


def main():
    d = AsycDatabase("database.db")
    d.create_database()


if __name__ == '__main__':
    main()
