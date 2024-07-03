import os
import msgpack
import pandas as pd
import markovify
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import time

csv_file = 'quotes.csv'
quotes_df = pd.read_csv(csv_file)
quotes = [str(quote) for quote in quotes_df['quote'].tolist()]
model = markovify.Text(' '.join(quotes), state_size=2)

def _get_quote():
    return model.make_sentence()

import textwrap

def _put_quote_in_image(quote):
    width, height = 1080, 1080
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    font_path = os.path.join(os.getcwd(), "raleway.ttf")
    font = ImageFont.truetype(font_path, 48)
    
    # Wrap the quote text into multiple lines
    wrapped_text = textwrap.wrap(quote, width=32, initial_indent='', subsequent_indent='', expand_tabs=True)
    
    # Calculate the total height of the wrapped text
    total_height = 0
    for line in wrapped_text:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        total_height += text_height
    
    y = (height - total_height) / 2

    for line in wrapped_text:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        x = (width - text_width) / 2
        draw.text((x, y), line, font=font, fill="white")
        y += text_height
    
    return image

def _save_image(image):
    file_path = f'temp/{time.time()}-{random.randint(1111, 9999)}.png'
    image.save(file_path)
    return file_path

def get_quote():
    quote = _get_quote()
    image = _put_quote_in_image(quote)
    path = _save_image(image)
    return path


if __name__ == '__main__':
    img = get_quote()
    Image.open(img).show()

