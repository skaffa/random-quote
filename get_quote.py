import os
import pandas as pd
import markovify
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import time

csv_file = 'quotes.csv'
quotes_df = pd.read_csv(csv_file)
quotes = [str(quote) for quote in quotes_df['quote'].tolist()]
# specify max sentence length
model = markovify.Text(' '.join(quotes), state_size=3)

def _get_quote():
    while True:
        quote = model.make_short_sentence(96)
        if quote:
            quote = f'“{quote}”'
            return quote

def _save_image(image):
    file_path = f'temp/{time.time()}-{random.randint(1111, 9999)}.png'
    image.save(file_path)
    return file_path

def _put_quote_on_background(quote, background_path):
    image = Image.open(background_path)
    draw = ImageDraw.Draw(image)
    font_path = os.path.join(os.getcwd(), "raleway.ttf")
    font = ImageFont.truetype(font_path, 48)
    wrapped_text = textwrap.wrap(quote, width=32, initial_indent='', subsequent_indent='', expand_tabs=True)
    total_height = 0
    for line in wrapped_text:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        total_height += text_height
    y = (image.height - total_height) / 2
    for line in wrapped_text:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        x = (image.width - text_width) / 2
        draw.text((x, y), line, font=font, fill="#454545")
        y += text_height
    return image

def get_quote(background_path):
    quote = _get_quote()
    image = _put_quote_on_background(quote, background_path)
    temp_path = _save_image(image)
    return temp_path