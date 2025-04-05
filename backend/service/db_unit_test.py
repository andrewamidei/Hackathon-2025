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
        for i in range(10):
            try:
                self.db.add_user(username + str(i), password + str(i))
                print("User added successfully")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("User already exists")
                
                
                
    def add_contact_test(self, username, contact_username):
            print("Testing for adding contacts with same usernames")
            for i in range(10):
                try:
                    self.db.add_contact(username, contact_username + str(i))
                    print("Contact added successfully")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    print("Contact already exists")

            print("Testing for adding contacts with different usernames")
            for i in range(5):
                try:
                    self.db.add_contact(username + str(i), contact_username + str())
                    print("Contact added successfully")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    print("Contact already exists")

    def add_chats(self, username, contact_username):
        print("Testing for adding chats with same usernames")
        for i in range(10):
            try:
                self.db.add_chat(username, contact_username, "hello" + str(i))
                print("Chat added successfully")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("Chat already exists")

        # print("Testing for adding chats with different usernames")
        # for i in range(5):
        #     try:
        #         self.db.add_chat(username + str(i), contact_username + str())
        #         print("Chat added successfully")
        #     except mysql.connector.Error as err:
        #         print(f"Error: {err}")
        #         print("Chat already exists")
    def user_login_signup_test(self):
        print("Testing for login and signup")
        for i in range(5):
            try:
                self.db.check_username_password('bob' + str(i), 'password', 0)
                self.db.check_username_password('bob' + str(i), 'password', 0)
                print("User added successfully")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("User already exists")


        try:
            self.db.check_username_password('bob' , 'password', 1)
            self.db.check_username_password('bob1' , 'password', 1)
            self.db.check_username_password('bob2' , 'password1', 1)
            self.db.check_username_password('bob3' , 'password1', 1)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print("User already exists")