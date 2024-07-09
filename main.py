from flask import Flask, send_file, jsonify, render_template, request, redirect
import get_background as bg
import get_quote as qt
import get_author as at
import get_watermark as wm
from glob import glob
from random import choice

app = Flask(__name__)

files = glob('static/images/*.webp')

# task to generate, delete, and move quotes

# functio to get random quote

@app.route('/get-quote')
def return_url():
    background = bg.get_background()
    quote = qt.get_quote(background)
    author = at.get_author(quote)
    url = request.url
    watermark = wm.get_watermark(author, url)

    return watermark

@app.route('/get-random-quote')
def show_the_quotes():
    return send_file(choice(files))

@app.route('/show-the-quotes')
def show_the_quotes():
    return render_template('show_the_quotes.html')

@app.route('/')
def home():
    return redirect("/show-the-quotes", code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)