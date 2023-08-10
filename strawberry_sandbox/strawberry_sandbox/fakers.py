
from typing import Optional

from faker import Faker
from factory import Factory, Faker as FactoryFaker, LazyAttribute, post_generation


from strawberry_sandbox.models import Article, Like, User

fake = Faker()
id_fakes = {}


def generate_unique_id(tag: str) -> int:
    global id_fakes
    if tag not in id_fakes:
        id_fakes[tag] = Faker()

    return id_fakes[tag].unique.random_int(min=1, max=10**6)


def id_factory_field(tag: str) -> LazyAttribute:
    return LazyAttribute(lambda el: generate_unique_id(tag))


def null_id_factory_field() -> LazyAttribute:
    return LazyAttribute(lambda el: 0)


class UserFactory(Factory):
    class Meta:
        model = User

    user_id = id_factory_field('user')
    name = FactoryFaker('name')


class ArticleFactory(Factory):
    class Meta:
        model = Article

    article_id = id_factory_field('article')
    author_id = null_id_factory_field()
    title = FactoryFaker('sentence', nb_words=6)
    content = FactoryFaker('paragraph', nb_sentences=5)
    publication_date = FactoryFaker('date_this_decade')


class LikeFactory(Factory):
    class Meta:
        model = Like

    article_id = null_id_factory_field()
    user_id = null_id_factory_field()


class Pool:
    def __init__(self, users: dict[int, User], articles: dict[int, Article], likes: list[Like]) -> None:
        self.users = users
        self.articles = articles
        self.likes = likes


pool: Optional[Pool] = None


def generate_pool(n_users: int = 50, n_authors: int = 5, n_articles: int = 15, n_likes: int = 150) -> Pool:
    global pool

    if pool is not None:
        return pool

    authors = list(UserFactory.create_batch(n_authors))
    users = list(UserFactory.create_batch(n_users))

    users = authors + users

    articles = list(ArticleFactory.create_batch(n_articles))

    for article in articles:
        article.author_id = fake.random_element(authors).user_id

    likes = set()
    while len(likes) < n_likes:
        like = (
            fake.random_element(articles).article_id,
            fake.random_element(users).user_id
        )
        likes.add(like)

    likes = [LikeFactory.build(article_id=like[0], user_id=like[1]) for like in likes]

    pool = Pool(
        users={user.user_id: user for user in users},
        articles={article.article_id: article for article in articles},
        likes=likes
    )

    return pool
