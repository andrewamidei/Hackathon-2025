import os
import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import json

from database import Database
from models.BlogPost import BlogPost, BlogPostVerificationError
from controller import LLmanager

logging.basicConfig(level=logging.DEBUG)

server = Flask(__name__)
CORS(server)

# Message storage structure: { username: [messages] }
message_queue = {}

@server.route('/api/chat', methods=['POST'])
def handle_chat():
    user_data = request.get_json()
    logging.debug(f"Received chat request: {user_data}")

    # Sending a message
    if 'sendAddress' in user_data and 'message' in user_data:
        address = user_data['sendAddress']
        message = user_data['message']
        
        if address not in message_queue:
            message_queue[address] = []
            
        message_queue[address].append(message)
        logging.debug(f"Message sent to {address}: {message}")
        return jsonify({'status': 'Message sent successfully'}), 200
    
    # Checking for messages
    elif 'username' in user_data:
        username = user_data['username']
        messages = message_queue.get(username, [])
        
        if messages:
            # Get the next message and remove it from the queue
            message = messages.pop(0)
            logging.debug(f"Delivering message to {username}: {message}")
            return jsonify({'message': message}), 200
            
        return jsonify({'message': 'No new messages'}), 200
    
    return jsonify({'error': 'Invalid request'}), 400

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

    if(db.check_username_password(username, password) != 0):
        logging.warning("User already exists")
        return jsonify({'error': 'Username already exists'}), 400
    
    logging.debug(db.get_users())


    response = {
        'message': 'User added successfully',
        'username': username
    }

    # Return the response as JSON
    return jsonify({'response': response}), 200

@server.route('/api/contacts ', methods=['POST'])
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




if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080, debug=True)
