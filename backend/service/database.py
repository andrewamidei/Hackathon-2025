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
                                CREATE TABLE IF NOT EXISTS users (
                                userID INT AUTO_INCREMENT PRIMARY KEY, 
                                username VARCHAR(255), 
                                password VARCHAR(255),
                                CONSTRAINT unique_id UNIQUE (userID),
                                CONSTRAINT unique_username UNIQUE (username)
                                )
                        ''')
            
            self.cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
    
    
    
    def get_users(self):
        try:
            self.cursor.execute('SELECT * FROM users')
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
            
            
            
            
    def add_Contact(self, username):
        try:
            self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS contacts (
                                contactID INT AUTO_INCREMENT PRIMARY KEY, 
                                name VARCHAR(255), 
                                userID INT,
                                CONSTRAINT FOREIGN KEY (userID) REFERENCES users(userID),
                                CONSTRAINT unique_id UNIQUE (contactID),
                                CONSTRAINT unique_name UNIQUE (username)
                                )
                        ''')
            
            self.cursor.execute('INSERT INTO contacts (name) VALUES (%s)', (username,))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()

            
    