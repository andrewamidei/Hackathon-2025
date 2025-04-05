import mysql.connector

class DB_unit_test:

    def __init__(self, db):
        self.db = db
        self.db.connect_to_db()
    

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
                
                
                
    def add_contact_test(self, username, contact_username):
            print("Testing for adding contacts with same usernames")
            for i in range(5):
                try:
                    self.db.add_contact(username, contact_username)
                    print("Contact added successfully")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    print("Contact already exists")
            print("Testing for adding contacts with same usernames")

            print("Testing for adding contacts with different usernames")
            for i in range(5):
                try:
                    self.db.add_contact(username + str(i), contact_username + str(i))
                    print("Contact added successfully")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    print("Contact already exists")