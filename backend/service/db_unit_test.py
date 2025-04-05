import mysql.connector

class DB_unit_test:

    def __init__(self, db):
        self.db = db
        self.db.connect_to_db()
        #self.db.truncate_table()
    

    def add_user_test(self, username, password):
        print("Testing for adding users with same usernames")
        for i in range(5):
            try:
                self.db.add_user(username, password)
                print("User added successfully")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("User already exists")
        print("Testing for adding users with same usernames")

        print("Testing for adding users with different usernames")
        for i in range(5):
            try:
                self.db.add_user(username + str(i), password + str(i))
                print("User added successfully")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("User already exists")