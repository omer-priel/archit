
from datetime import date


# Models
class User:
    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name

    def __str__(self) -> str:
        return str(self.user_id)


class Article:
    def __init__(self, article_id: int, author_id: int, title: str, content: str, publication_date: date) -> None:
        self.article_id = article_id
        self.author_id = author_id
        self.title = title
        self.content = content
        self.publication_date = publication_date

    def __str__(self) -> str:
        return str(self.article_id)


class Like:
    def __init__(self, article_id: int, user_id: int) -> None:
        self.article_id = article_id
        self.user_id = user_id

    def __str__(self) -> str:
        return f'{self.user_id} likes {self.article_id}'
