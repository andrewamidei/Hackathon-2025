import os
import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS

from database import Database
from db_unit_test import DB_unit_test
from models.BlogPost import BlogPost, BlogPostVerificationError
from controller import LLmanager
import mysql.connector
import logging


logging.basicConfig(level=logging.DEBUG)
db = Database('db-78n9n')
db.connect_to_db()  

unit_test = DB_unit_test(db)
#unit_test.add_chats('bob', 'alice')
unit_test.user_login_signup_test()


#print(db.get_chats('bob', 'alice', 20))

    

server = Flask(__name__)
CORS(server)
conn = None

# @server.route('/')
# def listBlogs():
#     global conn
#     if not conn:
#         conn = DBManager(password_file='/run/secrets/db-password')
#         conn.populate_db()
#     result = conn.query_blog_posts()

#     if result:
#         return jsonify(result)
#     else:
#         return jsonify({'error': "Error querying blogs."}), 404

# @server.route('/<int:post_id>')
# def listBlog(post_id):
#     global conn
#     logging.debug(f'Received request for post_id: {post_id}')
#     if not conn:
#         conn = DBManager(password_file='/run/secrets/db-password')
#         conn.populate_db()

#     result = conn.query_blog_post(post_id=post_id)

#     if result:
#         return jsonify(result)
#     else:
#         return jsonify({'error': "Error querying blog"}), 404


@server.route('/api/debug/database', methods=['GET'])
def debugDB():
    pass

@server.route('/api/queryllm', methods=['POST'])
def PostQuery():
    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'prompt' not in request_data:
        return jsonify({'error': 'Invalid request, "prompt" is required'}), 400

    # Extract the prompt from the request
    prompt = request_data['prompt']

    llm_manager = LLmanager()

    response = llm_manager.llmQuery(message=prompt)

    # Return the response as JSON
    return jsonify({'response': response}), 200

    # return response


@server.route('/api/login', methods=['POST'])
def PostLogin():

    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'username' not in request_data or 'password' not in request_data:
        return jsonify({'error': 'Invalid request, "username" and "password" are required'}), 400

    # Extract the username and password from the request
    print("Conneting to DB")
    logging.warning("Conneting to DB")
    username = request_data['username']
    password = request_data['password']

    db = Database('db-78n9n')
    db.connect_to_db()

    if(db.check_username_password(username, password, 1) != 0):
        logging.warning("User already exists")
        return jsonify({'error': 'Username already exists'}), 400
    
    logging.debug(db.get_users())


    response = {
        'message': 'User added successfully',
        'username': username
    }

    # Return the response as JSON
    return jsonify({'response': response}), 200

@server.route('/api/signup', methods=['POST'])
def PostSignup():
    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'username' not in request_data or 'password' not in request_data:
        return jsonify({'error': 'Invalid request, "username" and "password" are required'}), 400

    # Extract the username and password from the request
    username = request_data['username']
    password = request_data['password']

    db = Database('db-78n9n')
    db.connect_to_db()
    if(db.check_username_password(username, password, 0) != 0):
        logging.warning("User already exists")
        return jsonify({'error': 'Username already exists'}), 400

    response = {
        'message': 'User added successfully',
        'username': username
    }

    # Return the response as JSON
    return jsonify({'response': response}), 200

@server.route('/api/contacts', methods=['POST'])
def PostContacts():
    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'username' not in request_data or 'contact_username' not in request_data:
        return jsonify({'error': 'Invalid request, "username" and "contact_username" are required'}), 400

    # Extract the username and password from the request
    username = request_data['username']
    contact_username = request_data['contact_username']

    db = Database('db-78n9n')
    db.connect_to_db()
    if(db.add_contact(username, contact_username) != 0):
        logging.warning("Contact already exists")
        return jsonify({'error': 'Contact already exists'}), 400

    response = {
        'message': 'Contact added successfully',
        'username': username,
        'contact_username': contact_username
    }

    # Return the response as JSON
    return jsonify({'response': response}), 200


@server.route('/api/get/contacts', methods=['POST'])
def GetContacts():
    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'username' not in request_data:
        return jsonify({'error': 'Invalid request, "username" is required'}), 400

    # Extract the username and password from the request
    username = request_data['username']

    db = Database('db-78n9n')
    db.connect_to_db()
    contacts = db.get_contacts(username)

    if contacts is None:
        logging.warning("Error getting contacts")
        return jsonify({'error': 'Error getting contacts'}), 400

    response = {
        'contacts': contacts
    }

    # Return the response as JSON
    return jsonify({'response': response}), 200

@server.route('/api/add/chat', methods=['POST'])
def PostChat():
    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'username' not in request_data or 'contact_username' not in request_data:
        return jsonify({'error': 'Invalid request, "username" and "contact_username" are required'}), 400

    # Extract the username and password from the request
    username = request_data['username']
    contact_username = request_data['contact_username']

    db = Database('db-78n9n')
    db.connect_to_db()
    chat_id = db.add_chat(username, contact_username)
    if(chat_id < 0):
        logging.warning("Adding chat failed")
        return jsonify({'error': 'Adding chat failed'}), 400

    response = {
        'message': 'Chat added successfully',
        'username': username,
        'contact_username': contact_username,
        'chat_id': chat_id
    }

    # Return the response as JSON
    return jsonify({'response': response}), 200

@server.route('/api/get/chat', methods=['POST'])
def GetChat():

    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'username' not in request_data or 'contact_username' not in request_data:
        return jsonify({'error': 'Invalid request, "username" and "contact_username" are required'}), 400

    # Extract the username and password from the request
    username = request_data['username']
    contact_username = request_data['contact_username']
    last_seen_id = request_data['last_seen_id'] if 'last_seen_id' in request_data else 0
    logging.debug(f"Last seen id: {last_seen_id}")

    db = Database('db-78n9n')
    db.connect_to_db()
    chat = db.get_chats(username, contact_username, last_seen_id)

    if chat is None:
        logging.warning("Error getting chat")
        return jsonify({'error': 'Error getting chat'}), 400

    response = {
        'chat': chat
    }

    # Return the response as JSON
    return jsonify({'response': response}), 200

if __name__ == '__main__':
    server.run()
