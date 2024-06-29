import json
import markovify
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
import random
import math
from discord.ext import commands, tasks
import discord

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

def generate_random_gradient_instagram_post():
    # Set the size of an Instagram post
    width, height = 1080, 1080

    # Create a new image with RGB mode
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    # Randomly choose between radial and linear gradient
    is_radial = random.choice([True, False])

    # Generate random start and end colors
    start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Randomly choose the rotation angle
    rotation_angle = random.uniform(0, 360)

    # Randomly choose the center point
    center_x = random.uniform(0.2, 0.8) * width
    center_y = random.uniform(0.2, 0.8) * height

    # Random chance for radial gradient
    if is_radial:
        # Draw the radial gradient
        for x in range(width):
            for y in range(height):
                t = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) / (width / 2)
                t = max(0, min(1, t))  # Clamp between 0 and 1
                current_color = (
                    int((1 - t) * start_color[0] + t * end_color[0]),
                    int((1 - t) * start_color[1] + t * end_color[1]),
                    int((1 - t) * start_color[2] + t * end_color[2]),
                )
                draw.point((x, y), fill=current_color)
    else:
        # Draw the linear gradient
        for step in range(width):
            t = step / (width - 1)  # Interpolation parameter between 0 and 1
            current_color = (
                int((1 - t) * start_color[0] + t * end_color[0]),
                int((1 - t) * start_color[1] + t * end_color[1]),
                int((1 - t) * start_color[2] + t * end_color[2]),
            )

            # Calculate the position based on the rotation and center point
            x = center_x + math.cos(math.radians(rotation_angle)) * (step - center_x)
            y = center_y + math.sin(math.radians(rotation_angle)) * (step - center_y)

            # Draw a vertical line with the current color
            draw.line([(step, 0), (step, height)], fill=current_color)

    return image



def get_quote():
    with open("quotes.json", "r") as file:
        data = json.load(file)

    text = ". ".join([quote["text"] for quote in data])
    model = markovify.Text(text)
    new_quote = model.make_sentence()
    return new_quote

def generate_random_gradient_with_quote():
    # Set the size of an Instagram post
    width, height = 1080, 1080

    # Generate random gradient
    gradient_image = generate_random_gradient_instagram_post()

    # Get a quote
    quote = get_quote()

    # Create a new image with the same size as the gradient
    image = Image.new("RGB", (width, height))
    image.paste(gradient_image, (0, 0))

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Specify the path to the font file
    font_path = os.path.join(os.getcwd(), "raleway.ttf")

    # Specify the font size
    font_size = 48

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the maximum width for text wrapping
    max_text_width = width * 0.8

    # Wrap the text to fit within the specified width
    wrapped_text = textwrap.fill(quote, width=29)  # Adjust width as needed

    # Calculate the wrapped text size
    wrapped_text_width, wrapped_text_height = draw.textsize(wrapped_text, font=font)

    # Calculate the position to center the wrapped text
    text_x = (width - wrapped_text_width) // 2
    text_y = (height - wrapped_text_height) // 2

    # Draw the wrapped text
    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill="white", align="center")

    filename = str(random.randint(1111111,99999999))
    image.save(image, filename)

    return image

# Example usage: Generate an image with a random gradient and a centered, wrapped quote with a specified font and size
# image_with_quote = generate_random_gradient_with_quote()
# image_with_quote.show()







@bot.command()
async def hello(ctx):
    await ctx.send(file=discord.File(generate_random_gradient_with_quote(), 'quote.png'))


async def send_image(ctx):
    # Replace 'your_image_url' with the actual URL of the image you want to send
    image_url = 'your_image_url'

    # Send the image
    await ctx.send(file=discord.File(image_url, 'image.png'))


bot.run('MTE0NTEzMDM4Nzg2NjE0MDc0Mw.Gd6PBy.9osQPknnyvkFkhcdWmoH705OiTONNVD66s-Vm0')