import get_background as bg
import get_quote as qt
import get_author as at
import get_watermark as wm
import get_webp as wp
import asyncio
import os
import time
import random
from glob import glob

async def seeder():
    while True:
        print("Seeding...")
        iters = 0
        history = glob('static/images/*.webp')
        
        while True:
            background = bg.get_background()
            quote = qt.get_quote(background)
            author = at.get_author(quote)
            watermark = wm.get_watermark(author, url='http://beanium.net:8000')
            webp = wp.get_webp(watermark)
            os.rename(webp, f'static/images/{time.time()}-{random.randint(1111, 9999)}.webp')

            iters += 1
            if iters >= 2500:
                for histor in history:
                    new_path = os.path.join('all_quote_images', os.path.basename(histor))
                    os.rename(histor, new_path)

                    for f in glob('temp/*'):
                        os.remove(f)
                    break

        print("Seeded!")
        print('Waiting 4 hours...')
        await asyncio.sleep((60*60) * 12)