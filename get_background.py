import numpy as np
from PIL import Image
import random
import time

def _random_pastel_color():
    base = 255
    return (random.randint(base//2, base), random.randint(base//2, base), random.randint(base//2, base))

def _create_gradient_image(width, height):
    # Generate two random pastel colors
    color1 = np.array(_random_pastel_color())
    color2 = np.array(_random_pastel_color())

    # Create a gradient array
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    
    for i in range(height):
        ratio = i / height
        color = (1 - ratio) * color1 + ratio * color2
        gradient[i, :, :] = color

    return gradient

# Define image dimensions
def get_background():
    width, height = 1024, 1024
    gradient_image = _create_gradient_image(width, height)
    path = f'temp/{time.time()}-{random.randint(1111, 9999)}.png'
    Image.fromarray(gradient_image).save(path)
    return path