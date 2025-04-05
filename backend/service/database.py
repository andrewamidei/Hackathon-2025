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
    
    def add_user(self, username, password) -> int:
        """
        Adds a new user to the Users table in the database.
        This method creates the Users table if it does not already exist. It then checks 
        if the provided username is unique. If the username does not exist, it inserts 
        the new user with the given username and password into the table. If the username 
        already exists, the user is not added.
        Args:
            username (str): The username of the user to be added. Must be unique.
            password (str): The password of the user to be added.
        Returns:
            int: A status code indicating the result of the operation:
                - 0: User successfully added.
                - 1: Username already exists, user not added.
                - -1: An error occurred during the operation.
        Raises:
            mysql.connector.Error: If a database error occurs during the operation.
        Notes:
            - The password is stored as plain text in the database. For production use, 
              consider hashing the password before storing it.
            - The method uses a rollback mechanism to revert changes in case of an error.
        """
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
                return 0
            else:
                print("Username already exists. User not added.")
                return 1
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            return -1
        
    def check_username_password(self, username, password, status) -> int:
        """
        This function checks if the username and password are correct.
        If the username does not exist, it adds the user to the database.

        Parameters:
            username (string): The username to check.
            password (string): The password to check.
            status (int): The status of the user. 0 - If the user does not exist and needs to be added. Else check the login credentials.
        Returns:
            - 0 - If the username and password are correct.
            - 1 - If the username and password are incorrect.
            - 2 - If the username does not exist and is added to the database.
            - -1 - If there is an error in the database connection or query.
        Raises:
            mysql.connector.Error: If there is an issue executing the database queries.
        """

        try:

            ## SIGNUP CHECK
            self.cursor.execute('SELECT COUNT(*) FROM Users WHERE username = %s', (username,))
            user_count = self.cursor.fetchone()[0]
            if user_count == 0 and status == 0:
                self.add_user(username, password)
                return 0
            elif user_count > 0 and status == 0:
                print("Username already exists.")
                return 1
            
            ## LOGIN CHECK
            self.cursor.execute('SELECT COUNT(*) FROM Users WHERE username = %s AND password = %s', (username, password))
            if self.cursor.fetchone()[0] == 1:
                print("Valid Credentials.")
                return 0
            else:
                print("Invalid username or password.")
                return 1
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return -1
    
    
    
    def get_users(self):
        """
        Retrieves all users from the Users table in the database.

        This method executes a SQL query to fetch all records from the Users table
        and returns the results. If an error occurs during the database operation,
        it logs the error and returns None.

        Returns:
            list: A list of tuples representing the rows in the Users table, where
                  each tuple contains the column values for a user.
            None: If an error occurs during the database operation.

        Raises:
            mysql.connector.Error: If there is an issue with the database connection
                                   or the SQL query execution.

        API Documentation:
            Endpoint: N/A (This is a database service method, not an API endpoint)
            Method: N/A
            Description: Internal method to fetch user data from the database.
        """
        try:
            self.cursor.execute('SELECT * FROM Users')
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    
    def truncate_table(self):
        """
        Truncates all data from the 'Users' table in the database.

        This method executes a SQL TRUNCATE command to remove all rows from the 
        'Users' table. It commits the transaction if successful, or rolls back 
        the transaction in case of an error.

        API Documentation:
        - SQL Command: TRUNCATE TABLE Users
        - Commit: Ensures changes are saved to the database.
        - Rollback: Reverts changes if an error occurs.

        Raises:
            mysql.connector.Error: If there is an issue executing the SQL command.

        Note:
            Use this method with caution as it permanently deletes all data 
            from the 'Users' table and cannot be undone.
        """
        try:
            self.cursor.execute('TRUNCATE TABLE Users')
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            
            
    
            
    def add_contact(self, username:str, contact_username:str) -> int:
        """
    This function adds a contact to the username.

    Parameters:
        username (string): Username of the user's contact where the contact_username is being added.
        contact_username (string): The contact's user name which is being added to the Username's contact.

    Returns:
        - -1 - If the username and contact_username are the same.
        - 0 - If the contact is added successfully.
        - 1 - If the contact already exists.
        - -2 - If the contact does not exist.
    """

        if(username == contact_username):
            print("Cannot add yourself as a contact")
            return -1 
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
            
            self.cursor.execute('SELECT COUNT(*) FROM Users WHERE username = %s', (contact_username,))
            if self.cursor.fetchone()[0] == 0:
                print("Contact does not exist.")
                return -2
            
            self.cursor.execute('SELECT COUNT(*) FROM Users WHERE username = %s', (username,))
            if self.cursor.fetchone()[0] == 0:
                print("User does not exist.")
                return -2
            
            
            
            self.cursor.execute('INSERT INTO Contacts (userID, contact_user_id) VALUES ((SELECT userID FROM Users WHERE username = %s), (SELECT userID FROM Users WHERE username = %s))', (username, contact_username))
            self.cursor.execute('INSERT INTO Contacts (userID, contact_user_id) VALUES ((SELECT userID FROM Users WHERE username = %s), (SELECT userID FROM Users WHERE username = %s))', (contact_username, username))

            self.connection.commit()
            return 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            return 1
            
    def get_contacts(self, username) -> list:
        """
        Retrieves a list of contact usernames for a given user.
        Args:
            username (str): The username of the user whose contacts are to be retrieved.
        Returns:
            list: A list of usernames representing the contacts of the specified user.
                  Returns an empty list if no contacts are found.
                  Returns None if a database error occurs.
        Raises:
            mysql.connector.Error: If there is an issue executing the database queries.
        Notes:
            - This function assumes the existence of two database tables:
              1. `Users` table with columns `userID` and `username`.
              2. `Contacts` table with columns `userID` and `contact_user_id`.
            - If a contact's userID is found in the `Contacts` table but their username
              cannot be retrieved from the `Users` table, a message is printed to the console.
        """
        try:
            self.cursor.execute('SELECT contact_user_id FROM Contacts WHERE userID = (SELECT userID FROM Users WHERE username = %s)', (username,))
            contact_user_ids = self.cursor.fetchall()

            contacts = []
            for user_id in contact_user_ids:
                self.cursor.execute('SELECT username FROM Users WHERE userID = %s', (user_id[0],))
                contact_username = self.cursor.fetchone()
                if contact_username:
                    contacts.append(contact_username[0])
                else:
                    print(f"Contact with userID {user_id[0]} not found.")
            return contacts
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
        """
        Adds a chat message between two users to the database.
        This method creates the `Chats` table if it does not already exist, 
        inserts a new chat message into the table, and retrieves the ID of the newly added chat.
        Args:
            username (str): The username of the sender.
            contact_username (str): The username of the receiver.
            message (str): The chat message to be added.
        Returns:
            int: The ID of the newly added chat message if successful, or -1 if an error occurs.
        Raises:
            mysql.connector.Error: If there is an issue with the database operation.
        Database Schema:
            - Table: Chats
                - chatID (INT, AUTO_INCREMENT, PRIMARY KEY): Unique identifier for the chat.
                - senderID (INT, NOT NULL): Foreign key referencing the `userID` of the sender in the `Users` table.
                - receiverID (INT, NOT NULL): Foreign key referencing the `userID` of the receiver in the `Users` table.
                - message (TEXT, NOT NULL): The chat message content.
                - sent_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): The timestamp when the message was sent.
        Example:
            chat_id = add_chat("alice", "bob", "Hello, Bob!")
            if chat_id != -1:
                print(f"Chat added successfully with ID: {chat_id}")
            else:
                print("Failed to add chat.")
        """
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
            self.cursor.execute('SELECT MAX(chatID) FROM Chats WHERE senderID = (SELECT userID FROM Users WHERE username = %s) AND receiverID = (SELECT userID FROM Users WHERE username = %s) AND message = %s'  , (username, contact_username, message))
            chat_id = self.cursor.fetchone()[0]
            print('Chat Id: %s is added successfully', (chat_id))
            self.connection.commit()
            return chat_id
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            return -1
    
    def get_chats(self, username, contact_username, last_seen_id = 0):
        """
        Retrieves chat messages between two users from the database.

        Args:
            username (str): The username of the first user (sender or receiver).
            contact_username (str): The username of the second user (receiver or sender).
            last_seen_id (int, optional): The ID of the last seen chat message. Defaults to 0.

        Returns:
            list[tuple]: A list of tuples, where each tuple contains:
                - chatID (int): The unique ID of the chat message.
                - message (str): The content of the chat message.
                - sent_at (datetime): The timestamp when the message was sent.
            None: If an error occurs during the database query.

        Raises:
            mysql.connector.Error: If there is an error executing the SQL query.

        API Documentation:
            This method fetches chat messages between two users from the `Chats` table in the database.
            It uses the `Users` table to resolve user IDs based on the provided usernames.
            The query filters messages based on the `last_seen_id` to retrieve only new messages.
            The result is a list of chat messages sorted by their `chatID` in ascending order.
        """
        try:
            self.cursor.execute('SELECT chatID, message, sent_at FROM Chats WHERE ((senderID = (SELECT userID FROM Users WHERE username = %s) AND receiverID = (SELECT userID FROM Users WHERE username = %s)) OR (senderID = (SELECT userID FROM Users WHERE username = %s) AND receiverID = (SELECT userID FROM Users WHERE username = %s))) AND chatID > %s', (username, contact_username, contact_username, username, last_seen_id))
            chats = self.cursor.fetchall()
            return chats
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

            
    