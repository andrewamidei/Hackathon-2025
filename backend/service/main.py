import os
import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS

from database import Database
from models.BlogPost import BlogPost, BlogPostVerificationError
from controller import LLmanager
from message_queue import MessageQueue, ChatMessage
from contextlib import contextmanager
from datetime import datetime
import threading
import time
import logging


logging.basicConfig(level=logging.DEBUG)


    

server = Flask(__name__)
CORS(server)
conn = None

@contextmanager
def get_db():
    db = Database('db-78n9n')
    try:
        db.connect_to_db()
        yield db
    finally:
        db.close_connection()

message_queue = MessageQueue()
llm_manager = LLmanager()

def process_messages():
    while True:
        try:
            message = message_queue.get_next_raw_message()
            if message:
                logging.info(f"Processing message: {message.sender}")
                with get_db() as db:
                    processed_content = llm_manager.llmQuery(
                        message=message.content,
                        sender=message.sender
                    )
                    logging.info(f"Processed content: {processed_content}")
                    
                    processed_message = ChatMessage(
                        sender=message.sender,
                        receiver=message.receiver,
                        content=processed_content,
                        timestamp=datetime.now(),
                        processed=True
                    )
                    
                    db.add_chat(message.sender, message.receiver, processed_content)
                    message_queue.add_processed_message(processed_message)
                    logging.info(f"Message processed and queued for {message.receiver}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
        time.sleep(0.1)

# Start message processing thread
processing_thread = threading.Thread(target=process_messages, daemon=True)
processing_thread.start()


@server.route('/health', methods=['GET'])
def health_check():
    try:
        with get_db() as db:
            db.get_users()  # Test database connection
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

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



@server.route('/api/chat/send', methods=['POST'])
def send_message():
    data = request.get_json()
    if not all(k in data for k in ['sender', 'receiver', 'content']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    message = ChatMessage(
        sender=data['sender'],
        receiver=data['receiver'],
        content=data['content'],
        timestamp=datetime.now()
    )
    
    message_queue.add_raw_message(message)
    return jsonify({'status': 'message queued'}), 200

@server.route('/api/chat/receive/<username>', methods=['GET'])
def receive_messages(username):
    messages = message_queue.get_processed_messages(username)
    return jsonify({
        'messages': [
            {
                'sender': m.sender,
                'content': m.content,
                'timestamp': m.timestamp.isoformat()
            } for m in messages
        ]
    }), 200


if __name__ == '__main__':
    server.run()
