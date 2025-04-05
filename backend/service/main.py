import os
from flask import Flask, jsonify
from flask_cors import CORS

from models.BlogPost import BlogPost, BlogPostVerificationError

import database
import mysql.connector
import logging


print("Server started")

logging.basicConfig(level=logging.DEBUG)
class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()

        
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,5)])
        self.connection.commit()
    
    def query_blog_posts(self):
        self.cursor.execute('SELECT id, title FROM blog')
        list_of_blog_posts = []
        for c in self.cursor:
            try:
                blog_post = BlogPost(c[0], c[1])
            except BlogPostVerificationError as e:
                logging.debug(f"Error: {e}")

            list_of_blog_posts.append(blog_post.to_dictionary())
        return list_of_blog_posts
    
    def query_blog_post(self, post_id):
        self.cursor.execute('SELECT id, title FROM blog WHERE id = %s', (post_id,))
        result = self.cursor.fetchone()
        list_of_blog_posts = []
        try:
            blog_post = BlogPost(result[0], result[1])
        except BlogPostVerificationError as e:
            logging.debug(f"Error: {e}")
            return

        list_of_blog_posts.append(blog_post.to_dictionary())
        return list_of_blog_posts


server = Flask(__name__)
CORS(server)
conn = None

@server.route('/')
def listBlogs():
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    result = conn.query_blog_posts()

    if result:
        return jsonify(result)
    else:
        return jsonify({'error': "Error querying blogs."}), 404

@server.route('/<int:post_id>')
def listBlog(post_id):
    global conn
    logging.debug(f'Received request for post_id: {post_id}')
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()

    result = conn.query_blog_post(post_id=post_id)

    if result:
        return jsonify(result)
    else:
        return jsonify({'error': "Error querying blog"}), 404


if __name__ == '__main__':
    server.run()

