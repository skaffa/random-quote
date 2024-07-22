import get_background as bg
import get_quote as qt
import get_author as at
import get_watermark as wm
import get_webp as wp
import get_database as db
import asyncio
import os
import time
import random
from glob import glob
import hashlib

async def seeder():
    while True:
        print("Seeding...")
        
        for i in range(25):
            background = bg.get_background()
            quote = qt.get_quote(background)
            author = at.get_author(quote)
            watermark = wm.get_watermark(author, url='http://beanium.net:8000')
            webp = wp.get_webp(watermark)
            name = hashlib.sha1(quote.encode()).hexdigest()
            os.rename(webp, f'all_quote_images/{name}.webp')
            db.add_quote(name, quote, author)
            print(i)


        t = glob('temp/*')
        if t:
            for f in t:
                try:
                    os.remove(f)
                except FileNotFoundError as e:
                    continue


        print("Seeded!")
        print('Waiting 30 minutes...')
        await asyncio.sleep((60*60) * .5)