from PIL import Image, ImageDraw, ImageFont
import os
import hashlib

def get_watermark(author_path, url):
    url = 'http://beanium.net:8000'
    watermark = Image.open(author_path)
    draw = ImageDraw.Draw(watermark)
    font_path = os.path.join(os.getcwd(), "raleway.ttf")
    font = ImageFont.truetype(font_path, 20)
    draw.text((0, watermark.height - 20), url, font=font, fill="#FF5F1F")
    name = hashlib.sha512(watermark.tobytes()).hexdigest()
    watermark.save("static/images/" + name + ".png")
    return name