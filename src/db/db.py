import aiosqlite
from models.article import ArticleInfo
from models.hab import HabrHab


class HabrDB:
    def __init__(self, db_name) -> None:
        self.db_name = db_name

    async def seed_tables(self):
        async with aiosqlite.connect(self.db_name) as db:

            await db.execute(
                """
            CREATE TABLE IF NOT EXISTS habs (
                id INTEGER PRIMARY KEY,
                name STRING,
                link STRING,
                interval INTEGER
            )     
            """
            )

            await db.execute(
                """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                heading STRING,
                link STRING,
                author_name STRING,
                author_link STRING,
                published_at DATE,
                hab_id INTEGER, 
                FOREIGN KEY (hab_id)  REFERENCES habs (id)
            )     
            """
            )

    async def get_habs(self) -> list[HabrHab]:
        habs: list[HabrHab] = []
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM habs") as cur:
                data = await cur.fetchall()
                for hab in data:
                    habs.append(HabrHab(hab[0], hab[1], hab[2], hab[3]))
        return habs

    async def seed_habs(self):
        habs = [
            ("programming", "https://habr.com/ru/hubs/programming/articles/", 2),
            ("bussines laws", "https://habr.com/ru/hubs/business-laws/articles/", 2),
        ]

        async with aiosqlite.connect(self.db_name) as db:
            for hab in habs:
                async with db.execute(
                    "SELECT link FROM habs WHERE link = ?", (hab[1],)
                ) as cur:
                    if await cur.fetchone() is None:
                        await db.execute(
                            "INSERT INTO habs (name, link, interval) VALUES (?, ?, ?)",
                            hab,
                        )
            await db.commit()

    async def insert_article(self, article: ArticleInfo, hab_id):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(
                "SELECT link FROM articles WHERE link = ?", (article.link,)
            ) as cur:
                if await cur.fetchone() is None:
                    await db.execute(
                        """
                                INSERT INTO articles (heading, link, author_name, author_link, published_at, hab_id) VALUES (?, ?, ?, ?, ?, ?);
                                """,
                        (
                            article.heading,
                            article.link,
                            article.author_name,
                            article.link_to_author,
                            article.publish_date,
                            hab_id
                        ),
                    )
                    await db.commit()
