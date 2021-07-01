import json
import os

import aiohttp
from bs4 import BeautifulSoup

from bot import models


class HabraService:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    async def get_new_articles(self) -> list[models.Article]:
        async with self._session.get("https://habr.com/ru/page1/") as res:
            html = await res.text()

        soup = BeautifulSoup(html, "lxml")

        new_articles = {}

        if not os.path.exists("articles.json"):
            with open("articles.json", "x") as f:
                f.write("{}")

        with open("articles.json") as f:
            articles = json.load(f)

        for p in soup.find_all(class_="post"):
            title = p.find(class_="post__title").text.strip()
            description = p.find(class_="post__text").text.strip()
            url = p.find(class_="post__title_link").get("href")

            article_id = url.split("/")[-2]

            if article_id in articles:
                continue

            result = {
                "title": title,
                "description": description,
                "url": url
            }

            articles[article_id] = result
            new_articles[article_id] = result

        with open("articles.json", "w") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)

        return [
            models.Article.parse_obj(a)
            for a in new_articles.values()
        ]
