import asyncpg
from models.article import ArticleInfo
from models.hab import HabrHab
import datetime

class HabrDB:
    def __init__(self, db_url) -> None:
        # db_url должен быть строкой подключения к PostgreSQL
        self.db_url = db_url

    async def seed_tables(self):
        conn = await asyncpg.connect(self.db_url)
        try:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS habs (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR,
                    link VARCHAR,
                    interval INTEGER
                )
                """
            )
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS articles (
                    id SERIAL PRIMARY KEY,
                    heading VARCHAR,
                    link VARCHAR,
                    author_name VARCHAR,
                    author_link VARCHAR,
                    published_at DATE,
                    hab_id INTEGER,
                    FOREIGN KEY (hab_id) REFERENCES habs (id)
                )
                """
            )
        finally:
            await conn.close()

    async def get_habs(self) -> list[HabrHab]:
        conn = await asyncpg.connect(self.db_url)
        try:
            rows = await conn.fetch("SELECT * FROM habs")
            habs = [HabrHab(row['id'], row['name'], row['link'], row['interval']) for row in rows]
        finally:
            await conn.close()
        return habs

    async def seed_habs(self):
        habs = [
            ("programming", "https://habr.com/ru/hubs/programming/articles/", 10),
            ("business laws", "https://habr.com/ru/hubs/business-laws/articles/", 2),
        ]

        conn = await asyncpg.connect(self.db_url)
        try:
            for hab in habs:
                row = await conn.fetchrow("SELECT link FROM habs WHERE link = $1", hab[1])
                if row is None:
                    await conn.execute(
                        "INSERT INTO habs (name, link, interval) VALUES ($1, $2, $3)",
                        hab[0], hab[1], hab[2]
                    )
        finally:
            await conn.close()

    async def insert_article(self, article: ArticleInfo, hab_id):
        conn = await asyncpg.connect(self.db_url)
        try:
            row = await conn.fetchrow("SELECT link FROM articles WHERE link = $1", article.link)
            if row is None:
                await conn.execute(
                    """
                    INSERT INTO articles (heading, link, author_name, author_link, published_at, hab_id)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    article.heading,
                    article.link,
                    article.author_name,
                    article.link_to_author,
                    datetime.datetime.fromisoformat(article.publish_date),
                    hab_id
                )
        finally:
            await conn.close()
