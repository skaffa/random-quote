from PIL import Image, ImageDraw, ImageFont
import os
import time
import random

def get_watermark(author_path, url):
    url = 'http://beanium.net:8000'
    watermark = Image.open(author_path)
    draw = ImageDraw.Draw(watermark)
    font_path = os.path.join(os.getcwd(), "raleway.ttf")
    font = ImageFont.truetype(font_path, 20)
    draw.text((0, watermark.height - 20), url, font=font, fill="#FF5F1F")
    path = f'temp/{time.time()}-{random.randint(1111, 9999)}.png'
    watermark.save(path)
    return path