
from datetime import date


# Models
class User:
    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name


class Address:
    def __init__(self, street: str, city: str, country: str, zip_code: str) -> None:
        self.street = street
        self.city = city
        self.country = country
        self.zip_code = zip_code


class UserProfile:
    def __init__(self, user_id: int, address: Address, phone_number: str, email: str, age: int, sex: bool) -> None:
        self.user_id = user_id
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.age = age
        self.sex = sex

    def is_male(self) -> bool:
        return self.sex


class UploadedImage:
    def __init__(self, image_id: int, file_name: str, width: int, height: int) -> None:
        self.image_id = image_id
        self.file_name = file_name
        self.width = width
        self.height = height


class Article:
    def __init__(self, article_id: int, author_id: int, title: str, content: str, publication_date: date) -> None:
        self.article_id = article_id
        self.author_id = author_id
        self.title = title
        self.content = content
        self.publication_date = publication_date


class Like:
    def __init__(self, article_id: int, user_id: int) -> None:
        self.article_id = article_id
        self.user_id = user_id


class ArticleImage:
    def __init__(self, article_id: int, image_id: int, image_index: int) -> None:
        self.article_id = article_id
        self.image_id = image_id
        self.image_index = image_index
