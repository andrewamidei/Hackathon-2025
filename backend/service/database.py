import mysql.connector

class Database:
    def __init__(self, password):
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect_to_db()
    
    def connect_to_db(self):
        

        self.connection = mysql.connector.connect(
            host='db',
            user='root',
            password=self.password,
            database='example',
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def add_user(self, username, password):
        try:
            self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS Users (
                                userID INT AUTO_INCREMENT PRIMARY KEY, 
                                username VARCHAR(255) NOT NULL, 
                                password VARCHAR(255) NOT NULL,
                                UNIQUE (username)
                                )
                        ''')
            
            self.cursor.execute('SELECT COUNT(*) FROM Users WHERE username = %s', (username,))
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('INSERT INTO Users (username, password) VALUES (%s, %s)', (username, password))
                self.connection.commit()
            else:
                print("Username already exists. User not added.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
    
    
    
    def get_users(self):
        try:
            self.cursor.execute('SELECT * FROM Users')
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    
    def truncate_table(self):
        try:
            self.cursor.execute('TRUNCATE TABLE users')
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            
            
            
            
    def add_contact(self, username, contact_username):

        if(username == contact_username):
            print("Cannot add yourself as a contact")
            return
        try:
            self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS Contacts (
                                contactID INT AUTO_INCREMENT PRIMARY KEY,  
                                userID INT NOT NULL,
                                contact_user_id INT NOT NULL,
                                FOREIGN KEY (userID) REFERENCES Users(userID),
                                FOREIGN KEY (contact_user_id) REFERENCES Users(userID),
                                UNIQUE (userID, contact_user_id)
                                )
                        ''')
            
            
            
            self.cursor.execute('INSERT INTO Contacts (userID, contact_user_id) VALUES ((SELECT userID FROM Users WHERE username = %s), (SELECT userID FROM Users WHERE username = %s))', (username, contact_username))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            
    def get_contacts(self):
        try:
            self.cursor.execute('SELECT * FROM Contacts')
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
            
            
    def drop_table(self):
        try:
            self.cursor.execute('DROP TABLE IF EXISTS Users')
            self.cursor.execute('DROP TABLE IF EXISTS Contacts')
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            
            
    def add_chat(self, username, contact_username, message):
        try:
            self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS Chats (
                                chatID INT AUTO_INCREMENT PRIMARY KEY,  
                                senderID INT NOT NULL,
                                receiverID INT NOT NULL,
                                message TEXT NOT NULL,
                                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (senderID) REFERENCES Users(userID),
                                FOREIGN KEY (receiverID) REFERENCES Users(userID)
                                )
                        ''')
            
            self.cursor.execute('INSERT INTO Chats (senderID, receiverID, message) VALUES ((SELECT userID FROM Users WHERE username = %s), (SELECT userID FROM Users WHERE username = %s), %s)', (username, contact_username, message))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()

            
    