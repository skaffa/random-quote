# TODO: (workflow)

from flask import Flask, send_file, jsonify

import get_background as bg
import get_quote as qt
# import serialize_quotes
# from get_author import AuthorGenerator

# author_generator = AuthorGenerator('authors_markov_chain.msgpack', 2)



# pre-load data


app = Flask(__name__)

@app.route('/')
def index():
    background = bg.get_background() # path to background image (gradient)
    # get random quote
    quote = qt.get_quote(background) # path to bg + quote
    # get random author-
    # author = author_generator.get_author()
    # combine quote and gradient
    # add author
    # save image
    # return image

    return send_file(quote, mimetype='image/png')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)