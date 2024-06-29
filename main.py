# import json
# import markovify
# from PIL import Image, ImageDraw, ImageFont
# import os
# import textwrap
# import random
# import math
# from flask import Flask, send_file
# import msgpack

# app = Flask(__name__)

# def generate_random_gradient_instagram_post():
#     # Set the size of an Instagram post
#     width, height = 1080, 1080

#     # Create a new image with RGB mode
#     image = Image.new("RGB", (width, height))
#     draw = ImageDraw.Draw(image)

#     # Generate random start and end colors
#     start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

#     # Randomly choose the rotation angle
#     rotation_angle = random.uniform(0, 360)

#     # Randomly choose the center point
#     center_x = random.uniform(0.2, 0.8) * width
#     center_y = random.uniform(0.2, 0.8) * height

#     # Draw the linear gradient
#     for step in range(width):
#         t = step / (width - 1)  # Interpolation parameter between 0 and 1
#         current_color = (
#             int((1 - t) * start_color[0] + t * end_color[0]),
#             int((1 - t) * start_color[1] + t * end_color[1]),
#             int((1 - t) * start_color[2] + t * end_color[2]),
#         )

#         # Calculate the position based on the rotation and center point
#         x = center_x + math.cos(math.radians(rotation_angle)) * (step - center_x)
#         y = center_y + math.sin(math.radians(rotation_angle)) * (step - center_y)

#         # Draw a vertical line with the current color
#         draw.line([(step, 0), (step, height)], fill=current_color)

#     return image

# def load_data_msgpack(file_path):
#     with open(file_path, "rb") as data_file:
#         packed_data = data_file.read()
#         data = msgpack.unpackb(packed_data, raw=False, use_list=False)
#     return data

# def get_quote():
#     # Load quotes data
#     quotes_data = load_data_msgpack("quotes.msgpack")

#     # Combine all quotes into a single text
#     text = ". ".join([quote['quote'] for quote in quotes_data])

#     # Create a text model
#     model = markovify.NewlineText(text, state_size=2)

#     # Try generating a sentence multiple times
#     for _ in range(5):
#         new_quote = model.make_sentence()
#         if new_quote:
#             return new_quote
    
#     # Return a default quote if all attempts fail
#     return "Your default quote goes here."

# def generate_random_gradient_with_quote():
#     # Set the size of an Instagram post
#     width, height = 1080, 1080

#     # Generate random gradient
#     gradient_image = generate_random_gradient_instagram_post()

#     # Get a quote
#     quote = get_quote()

#     # Create a new image with the same size as the gradient
#     image = Image.new("RGB", (width, height))
#     image.paste(gradient_image, (0, 0))

#     # Create a draw object
#     draw = ImageDraw.Draw(image)

#     # Specify the path to the font file
#     font_path = os.path.join(os.getcwd(), "raleway.ttf")

#     # Specify the font size
#     font_size = 48

#     # Load the font
#     font = ImageFont.truetype(font_path, font_size)

#     # Calculate the maximum width for text wrapping
#     max_text_width = width * 0.8

#     # Wrap the text to fit within the specified width
#     wrapped_text = textwrap.fill(quote, width=29)  # Adjust width as needed

#     # Calculate the wrapped text size
#     wrapped_text_width, wrapped_text_height = draw.textsize(wrapped_text, font=font)

#     # Calculate the position to center the wrapped text
#     text_x = (width - wrapped_text_width) // 2
#     text_y = (height - wrapped_text_height) // 2

#     # Draw the wrapped text
#     draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill="white", align="center")

#     filename = str(random.randint(1111111, 99999999))
#     file_path = f'images/{filename}.png'
#     image.save(file_path)

#     return file_path

# @app.route('/generate_quote_image', methods=['GET'])
# def generate_quote_image():
#     file_path = generate_random_gradient_with_quote()
#     return send_file(file_path, mimetype='image/png', as_attachment=True, attachment_filename='quote.png')

# if __name__ == '__main__':
#     os.makedirs('images', exist_ok=True)
#     app.run(debug=True, host='0.0.0.0', port=5000)


import json
import markovify
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
import random
import math
import msgpack

# Generate a random gradient Instagram post and serialize the image
def generate_random_gradient_instagram_post():
    width, height = 1080, 1080
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    # Your gradient drawing logic here
    return image

# Serialize and save the generated gradient image
def serialize_gradient_image(image, file_path):
    image.save(file_path)

# Load data from msgpack file
def load_data_msgpack(file_path):
    with open(file_path, "rb") as data_file:
        packed_data = data_file.read()
        data = msgpack.unpackb(packed_data, raw=False, use_list=False)
    return data

# Get a random quote and author
def get_random_quote_and_author(quotes_data):
    random_entry = random.choice(quotes_data)
    return random_entry['quote'], random_entry['author']

# Serialize and save a quote using JSON
def serialize_quote(quote, file_path):
    with open(file_path, 'w') as f:
        json.dump({"quote": quote}, f)

# Generate a combined image with gradient, quote, and author, and serialize it
def generate_random_gradient_with_quote():
    width, height = 1080, 1080
    gradient_image = generate_random_gradient_instagram_post()
    quotes_data = load_data_msgpack("quotes.msgpack")
    quote, author = get_random_quote_and_author(quotes_data)

    image = Image.new("RGB", (width, height))
    image.paste(gradient_image, (0, 0))
    draw = ImageDraw.Draw(image)

    font_path = os.path.join(os.getcwd(), "raleway.ttf")
    font_size = 48
    font = ImageFont.truetype(font_path, font_size)

    max_text_width = width * 0.8
    wrapped_text = textwrap.fill(quote, width=29)
    wrapped_text_width, wrapped_text_height = draw.textsize(wrapped_text, font=font)

    text_x = (width - wrapped_text_width) // 2
    text_y = (height - wrapped_text_height) // 2

    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill="white", align="center")

    author_text = f"- {author}"
    author_text_width, author_text_height = draw.textsize(author_text, font=font)
    author_text_x = (width - author_text_width) // 2
    author_text_y = text_y + wrapped_text_height + 20

    draw.text((author_text_x, author_text_y), author_text, font=font, fill="white", align="center")

    filename = str(random.randint(1111111, 99999999))
    file_path = f'images/{filename}.png'
    image.save(file_path)

    return file_path

# Main function to generate and serialize the combined image with quote
def main():
    os.makedirs('images', exist_ok=True)

    # Generate and serialize the combined image with quote
    file_path = generate_random_gradient_with_quote()
    print(f"Generated image saved at: {file_path}")

if __name__ == '__main__':
    main()
