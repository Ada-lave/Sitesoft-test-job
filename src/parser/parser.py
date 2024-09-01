
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from models.article import ArticleInfo


WEBSITE_URL = "https://habr.com"

class HabrParser:
    def __init__(self, URL) -> None:
        self.URL = URL

    async def get_info_from_article(self, link: str, session) -> ArticleInfo:  
        html = await self.fetch_html(link, session)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("h1", class_="tm-title").text
        author_link = soup.find('a', class_="tm-user-info__username")
        time = soup.find('span', class_="tm-article-datetime-published").find("time").attrs['datetime']
        
        return ArticleInfo(
            heading=title, 
            publish_date=time, 
            link=link, 
            author_name=author_link.text, 
            link_to_author=f"{WEBSITE_URL}{author_link.attrs['href']}"
            )


    async def get_info_from_habr(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(self.URL, session)
            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("article", class_="tm-articles-list__item")
            for article in articles:
                link_to_article = article.find("a", "tm-title__link")
                tasks.append(self.get_info_from_article(f"{WEBSITE_URL}{link_to_article.attrs["href"]}", session))

            return await asyncio.gather(*tasks)
        
    async def fetch_html(self, url: str, session: aiohttp.ClientSession) -> str:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Error fetching {url}: {response.status}")
                return ""
            return await response.text()
