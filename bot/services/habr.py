import aiohttp
from bs4 import BeautifulSoup
import clickhouse_driver as ch

from bot import models


class HabraService:
    def __init__(self,
                 session: aiohttp.ClientSession,
                 clickhouse_driver: ch.Client):
        self._session = session
        self._clickhouse = clickhouse_driver

    async def get_last_articles(self) -> list[models.Article]:
        return self._get_articles(5)

    async def scheduler_task(self):
        async with self._session.get("https://habr.com/ru/page1") as res:
            html = await res.text()

        articles = _parse_articles(html)
        self._add_articles(articles)

    def _add_articles(self, articles: list[models.Article]):
        self._clickhouse.execute(
            "INSERT INTO article (title, description, url) VALUES",
            [a.dict() for a in articles]
        )

    def _get_articles(self, count: int) -> list[models.Article]:
        rows = self._clickhouse.execute(
            "SELECT (title, description, url) "
            "FROM article "
            f"ORDER BY date_added DESC LIMIT {count}"
        )

        return list(
            models.Article(
                title=row[0][0],
                description=row[0][1],
                url=row[0][2]
            )
            for row in rows
        )


def _parse_articles(html: str) -> list[models.Article]:
    soup = BeautifulSoup(html, "lxml")

    result = []

    posts = soup.find_all(class_="post")
    for post in posts:
        title = post.find(class_="post__title").text.strip()
        description = post.find(class_="post__text").text.strip()
        url = post.find(class_="post__title_link").get("href")

        result.append(models.Article(
            title=title,
            description=description,
            url=url
        ))

    return result
