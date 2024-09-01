
import asyncio
import datetime

from db.db import HabrDB
from models.article import ArticleInfo
from models.hab import HabrHab
from parser.parser import HabrParser
from datetime import timedelta

async def parse_hab(habr_db: HabrDB, parser: HabrParser, hab: HabrHab):    
   try:
        articles: list[ArticleInfo] = await parser.get_info_from_habr()
        print(f"HAB: {hab.name}")
        for article in articles:
            await habr_db.insert_article(article, hab.id)
            print(article.heading)
        print("\n\n")
   except Exception as e:
       print(f"Error parsing {hab.name}: {e}")

async def start_up():
    habr_db = HabrDB('db.sqlite3')
    await habr_db.seed_tables()
    await habr_db.seed_habs()
    await parse_habs(habr_db)
        

async def parse_habs(habr_db: HabrDB):
    habs = await habr_db.get_habs()
    tasks = []
    for hab in habs:    
        parser = HabrParser(hab.link)
        tasks.append(asyncio.create_task(schedule_task(parse_hab, habr_db, parser, hab, hab.interval)))
    await asyncio.gather(*tasks)
        
async def schedule_task(func, habr_db, parser, hab, interval):
    next_run = datetime.datetime.now()
    while True:
        now = datetime.datetime.now()
        if now >= next_run:
            await func(habr_db, parser, hab)
            next_run = now + timedelta(seconds=interval)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(start_up())