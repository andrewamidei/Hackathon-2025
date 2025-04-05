import os

from flask import Flask, jsonify, request
from flask_cors import CORS


from models.BlogPost import BlogPost, BlogPostVerificationError
from controller import LLmanager
import mysql.connector
import logging


logging.basicConfig(level=logging.DEBUG)

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

    model = 'deepseek-r1:8b'  # local model
    url = 'http://192.168.8.137:11434/api/generate'

    llm_manager = LLmanager(model=model, url=url)

    response = llm_manager.llmQuery(prompt=prompt)

    # Return the response as JSON
    return jsonify({'response': response}), 200

    # return response


if __name__ == '__main__':
    server.run()
