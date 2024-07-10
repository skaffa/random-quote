from flask import Flask, send_file, jsonify, render_template, request, redirect
from flask_cors import CORS
from flask_minify import Minify, decorators as minify_decorators
from flask_compress import Compress
from glob import glob
from random import choice
import asyncio
import threading
import background_seeder as seeder

app = Flask(__name__)
Minify(app, go=False, passive=True)
CORS(app)
Compress(app)

######
# @app.route('/gyallery-like-riri')
# def return_batch():
#     files = glob('static/images/*.webp')
#     return jsonify(files)
######

@app.route('/get-random-quote')
def get_random_quote():
    files = glob('static/images/*.webp')
    return send_file(choice(files))

@app.route('/vote-a-quote')
def vote_a_quote():
    return render_template('vote_a_quote.html')

@app.route('/show-the-quotes')
def show_the_quotes():
    return render_template('show_the_quotes.html')

@app.route('/')
def home():
    return redirect("/show-the-quotes", code=302)

@app.route('/robots.txt')
def robots():
    return send_file('static/robots.txt')

def run_seeder():
    asyncio.run(seeder.seeder())

if __name__ == '__main__':
    seeder_thread = threading.Thread(target=run_seeder)
    seeder_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=8000, use_reloader=False)
