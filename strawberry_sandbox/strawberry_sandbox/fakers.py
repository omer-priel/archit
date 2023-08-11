
from typing import Optional

from faker import Faker
from factory import Factory, Faker as FactoryFaker, LazyAttribute, SubFactory

from strawberry_sandbox.models import Article, Like, User, Address, UserProfile, UploadedImage, ArticleImage


fake = Faker()
id_fakes = {}


PHONE_PREFIXS = ['052', '053', '054', '055', '058']


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


class AddressFactory(Factory):
    class Meta:
        model = Address

    street = FactoryFaker('street_address')
    city = FactoryFaker('city')
    country = FactoryFaker('country')
    zip_code = FactoryFaker('postcode')


class UserProfileFactory(Factory):
    class Meta:
        model = UserProfile

    user_id = null_id_factory_field()
    address = SubFactory(AddressFactory)
    phone_number = LazyAttribute(lambda x: fake.random_element(PHONE_PREFIXS) + fake.numerify('-#######'))
    email = FactoryFaker('email')
    age = FactoryFaker('pyint', min_value=18, max_value=100)
    sex = FactoryFaker('pybool')


class UploadedImageFactory(Factory):
    class Meta:
        model = UploadedImage

    image_id = id_factory_field('uploaded_image')
    file_name = LazyAttribute(lambda el: fake.file_name(category='image'))
    width = FactoryFaker('pyint', min_value=100, max_value=1000)
    height = FactoryFaker('pyint', min_value=100, max_value=1000)


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


class ArticleImageFactory(Factory):
    class Meta:
        model = ArticleImage

    article_id = null_id_factory_field()
    image_id = null_id_factory_field()
    image_index = LazyAttribute(lambda el: 0)


class Pool:
    def __init__(self, users: dict[int, User], users_profile: dict[int, UserProfile],
                 uploaded_images: dict[int, UploadedImage], articles: dict[int, Article],
                 likes: list[Like], articles_images: list[ArticleImage]) -> None:
        self.users = users
        self.users_profile = users_profile
        self.uploaded_images = uploaded_images
        self.articles = articles
        self.likes = likes
        self.articles_images = articles_images


pool: Optional[Pool] = None


def generate_pool(n_users: int = 50, n_authors: int = 5, n_articles: int = 15, n_likes: int = 150,
                  n_articles_images: int = 10) -> Pool:
    global pool

    if pool is not None:
        return pool

    authors = list(UserFactory.create_batch(n_authors))
    authors_profile = list(UserProfileFactory.create_batch(n_authors))
    for author_profile, author in zip(authors_profile, authors):
        author_profile.user_id = author.user_id

    users = list(UserFactory.create_batch(n_users))
    users_profile = list(UserProfileFactory.create_batch(n_users))
    for user_profile, user in zip(users_profile, users):
        user_profile.user_id = user.user_id

    users = authors + users
    users_profile = authors_profile + users_profile

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

    uploaded_images = list(UploadedImageFactory.create_batch(n_articles_images))
    articles_images = []

    not_in_article = set(uploaded_images)
    images_indexs = {}
    while len(not_in_article) > 0:
        image_id = not_in_article.pop().image_id
        article_image = ArticleImageFactory.build(image_id=image_id)
        article_image.article_id = fake.random_element(articles).article_id
        if article_image.article_id not in images_indexs:
            images_indexs[article_image.article_id] = 0
        else:
            images_indexs[article_image.article_id] += 1
        article_image.image_index = images_indexs[article_image.article_id]
        articles_images.append(article_image)

    pool = Pool(
        users={user.user_id: user for user in users},
        users_profile={profile.user_id: profile for profile in users_profile},
        uploaded_images={image.image_id: image for image in uploaded_images},
        articles={article.article_id: article for article in articles},
        likes=likes,
        articles_images=articles_images
    )

    return pool
