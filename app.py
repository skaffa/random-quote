from flask import Flask, send_file, jsonify, render_template, request, redirect
from flask_limiter import Limiter
from flask_caching import Cache
import utilset as uls
from flask_cors import CORS
from flask_minify import Minify, decorators as minify_decorators
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from flask_talisman import Talisman
import get_database as qdb
import routing as rt
import asyncio
import threading
import background_seeder as seeder
import random
from waitress import serve
import ssl

app = Flask(__name__)
# Minify(app, go=False, passive=True)
CORS(app)
# Compress(app)
# Talisman(app)
cache = Cache(app=app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': 'tmp/flaskcache'})
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["7 per second"],
    storage_uri="memory://",
    strategy="moving-window",
)

@cache.memoize(timeout=uls.get_seconds(minutes=5))
def list_cached_quotes():
    return qdb.fetch_multiple_quotes(count=1000)

rt.domain_based_routing(app)

@app.route('/random-quote-image')
def random_quote_image():
    return send_file(f"all_quote_images/{random.choice(list_cached_quotes()).uid}.webp")

@app.route('/vote-a-quote')
@app.route('/vote')
def vote_a_quote():
    return render_template('vote-a-quote.html')

@app.route('/show-the-quotes')
def show_the_quotes():
    return render_template('show-the-quotes.html')

<<<<<<< Updated upstream:app.py
@app.route('/robots.txt')
def robots():
    return send_file('static/robots.txt')

@app.route('/ads.txt')
def ads_txt():
    return render_template('static/ads.txt')

=======
>>>>>>> Stashed changes:main.py
@app.route('/sitemap')
@app.route('/sitemap.xml')
def sitemap():
    return send_file('static/sitemap.xml')

@app.route('/legal')
def legal():
    return redirect('https://github.com/skaffa/random-quote')

@app.route('/robots.txt')
def robots():
    return send_file('static/robots.txt')

@app.route('/')
@app.errorhandler(404)
def home(e=None):
    print("Index it is")
    return redirect("/show-the-quotes", code=302)

def run_seeder():
    asyncio.run(seeder.seeder())

if __name__ == '__main__':
    seeder_thread = threading.Thread(target=run_seeder)
    seeder_thread.start()
    
    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain(certfile='path/to/your/certfile.pem', keyfile='path/to/your/keyfile.pem')


    # certifytheweb is used for LetsEncrypt certificates
    serve(app, host='0.0.0.0', port=443, ssl_context='adhoc') #, ssl_context=ssl_context
