import os
import pandas as pd
from markov_generator import MarkovWordGenerator
import random
import string
from PIL import Image, ImageDraw, ImageFont
import time

csv_file = 'quotes.csv'
authors_df = pd.read_csv(csv_file, usecols=['author'], converters={'author': str})
authors = [str(author) for author in authors_df['author'].tolist()]

generator = MarkovWordGenerator(markov_length=2, word_list=authors)

def _get_author():
    while True:
        generated_word = str(generator.generate_word())
        if generated_word is not None and len(generated_word) > 5:
            if generated_word[0].isupper():
                if generated_word[1].islower():
                    if all(c.isalpha() for c in generated_word):
                        return generated_word

def get_author(quote_path):
    author = _get_author()
    mid_letter = f' {random.choice(string.ascii_uppercase)}.' if random.uniform(0, 1) < .3 else ''
    surname = f' {_get_author()}' if random.uniform(0, 1) < .55 else ''
    full_name = '~ ' + author + mid_letter + surname

    # Add author to image, italic and bold text
    img = Image.open(quote_path)
    draw = ImageDraw.Draw(img)
    font_path = os.path.join(os.getcwd(), "sfproitaliclight.otf")
    font = ImageFont.truetype(font_path, 35) # Adjust the font to include italic and bold if needed
    
    # Calculate text position using textbox
    image_width, image_height = img.size
    bbox = draw.textbbox((0, 0), full_name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (image_width - text_width) / 2
    text_y = image_height * 0.80  # 75% from the top

    # Add text to image
    # italic text
    draw.text((text_x, text_y), full_name, font=font, fill="#454545")
    
    # Save image to temp folder
    temp_folder = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_folder, exist_ok=True)
    temp_path = f'temp/{time.time()}-{random.randint(1111, 9999)}.png'
    img.save(temp_path)

    # Return image path
    return temp_path
