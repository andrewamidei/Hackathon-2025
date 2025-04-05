import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from database import Database
from models.BlogPost import BlogPost, BlogPostVerificationError
from controller import LLmanager
from controller import msg_handler
import mysql.connector
import asyncio
import logging


logging.basicConfig(level=logging.DEBUG)


def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

server = Flask(__name__)
CORS(server)
conn = None

@server.route('/api/debug/database', methods=['GET'])
def debugDB():
    pass

@server.route('/api/queryllm', methods=['POST'])
def PostQuery():
    try:
        # Parse the incoming JSON data
        request_data = request.get_json()
        if not request_data or 'prompt' not in request_data:
            return jsonify({'error': 'Invalid request, "prompt" is required'}), 400

        # Extract the prompt from the request
        prompt = request_data['prompt']
        rate_prompt = request_data['rate_prompt']
    #MODEL = 'mistral'
    #URL = 'http://192.168.8.137:11434/api/generate'

        llm_manager_gpu = LLmanager(model="mistral", url='http://192.168.8.137:11434/api/generate')
        llm_manager_cpu = LLmanager(model="gemma:2b", url='http://192.168.8.137:11435/api/generate')
        llm_feeder = msg_handler(LLM_gpu=llm_manager_gpu, LLM_cpu=llm_manager_cpu)
        llm_feeder.feed("1", prompt)
        llm_feeder.rate("1", rate_prompt)
        response =  llm_feeder.consume()

        #response = llm_manager.llmQuery(message=prompt)
        # Return the response as JSON
        return jsonify({'response': response}), 200
    except Exception as e:
        logging.error(f"Error in PostQuery: {str(e)}")
        return jsonify({'error': str(e)}), 500

    # return response


@server.route('/api/login', methods=['POST'])
def PostLogin():

    # Parse the incoming JSON data
    request_data = request.get_json()
    if not request_data or 'username' not in request_data or 'password' not in request_data:
        return jsonify({'error': 'Invalid request, "username" and "password" are required'}), 400

    # Extract the username and password from the request
    print("Connecting to DB")
    logging.warning("Connecting to DB")
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
    server.run()
