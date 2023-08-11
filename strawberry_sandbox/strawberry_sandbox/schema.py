
import typing
import strawberry


from strawberry_sandbox.models import User, Article, UserProfile
from strawberry_sandbox.fakers import generate_pool


@strawberry.type
class AddressOutput:
    street: str
    city: str
    country: str
    zip_code: str


@strawberry.type
class UserProfileOutput:
    address: AddressOutput
    phone_number: str
    email: str
    age: int
    sex: str


@strawberry.type
class UserOutput:
    user_id: int
    name: str
    profile: UserProfileOutput


@strawberry.type
class ArticleOutput:
    article_id: int
    author_id: int
    title: str
    content: str
    publication_date: str


@strawberry.type
class UserFullOutput(UserOutput):
    written_articles: list[ArticleOutput]
    liked_articles: list[ArticleOutput]


@strawberry.type
class ArticleFullOutput(ArticleOutput):
    author: UserOutput
    likes: list[UserOutput]


def safe_user(user: User, user_profile: UserProfile) -> UserOutput:
    return UserOutput(
        user_id=user.user_id,
        name=user.name,
        profile=UserProfileOutput(
            address=AddressOutput(
                street=user_profile.address.street,
                city=user_profile.address.city,
                country=user_profile.address.country,
                zip_code=user_profile.address.zip_code
            ),
            phone_number=user_profile.phone_number,
            email=user_profile.email,
            age=user_profile.age,
            sex="Male" if user_profile.sex else "Female"
        )
    )


def safe_full_user(user: User, user_profile: UserProfile,
                   written_articles: list[ArticleOutput],
                   liked_articles: list[ArticleOutput]) -> UserFullOutput:
    return UserFullOutput(
        user_id=user.user_id,
        name=user.name,
        profile=UserProfileOutput(
            address=AddressOutput(
                street=user_profile.address.street,
                city=user_profile.address.city,
                country=user_profile.address.country,
                zip_code=user_profile.address.zip_code
            ),
            phone_number=user_profile.phone_number,
            email=user_profile.email,
            age=user_profile.age,
            sex="Male" if user_profile.sex else "Female"
        ),
        written_articles=written_articles,
        liked_articles=liked_articles
    )


def safe_article(article: Article) -> ArticleOutput:
    return ArticleOutput(
        article_id=article.article_id,
        author_id=article.author_id,
        title=article.title,
        content=article.content,
        publication_date=str(article.publication_date)
    )


def safe_full_article(article: Article, author: UserOutput, likes: list[UserOutput]) -> ArticleFullOutput:
    return ArticleFullOutput(
        article_id=article.article_id,
        author_id=article.author_id,
        title=article.title,
        content=article.content,
        publication_date=str(article.publication_date),
        author=author,
        likes=likes,
    )


def get_articles() -> list[ArticleFullOutput]:
    pool = generate_pool()
    articles_output = []

    for article_id in pool.articles:
        article = pool.articles[article_id]

        article_output = safe_full_article(
            article,
            author=safe_user(pool.users[article.author_id], pool.users_profile[article.author_id]),
            likes=[safe_user(pool.users[like.user_id], pool.users_profile[like.user_id]) for like in pool.likes
                   if like.article_id == article.article_id]
        )

        articles_output.append(article_output)

    return articles_output


def get_users() -> list[UserFullOutput]:
    pool = generate_pool()
    users_output = []
    for user_id in pool.users:
        user = pool.users[user_id]

        user_output = safe_full_user(
            user,
            pool.users_profile[user_id],
            written_articles=[safe_article(pool.articles[article_id]) for article_id in pool.articles
                              if pool.articles[article_id].author_id == user_id],
            liked_articles=[safe_article(pool.articles[like.article_id]) for like in pool.likes if like.user_id == user_id]
        )

        users_output.append(user_output)

    return users_output


@strawberry.type
class Query:
    articles: list[ArticleFullOutput] = strawberry.field(resolver=get_articles)
    users: list[UserFullOutput] = strawberry.field(resolver=get_users)


schema = strawberry.Schema(query=Query)
