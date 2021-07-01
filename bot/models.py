from pydantic import BaseModel


class Article(BaseModel):
    title: str
    description: str
    url: str
