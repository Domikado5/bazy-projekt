from typing import ForwardRef
import databases
import ormar
import sqlalchemy
import datetime
import decimal

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=32, unique=True, nullable=False)
    password: str = ormar.String(max_length=512, nullable=False)
    email: str = ormar.String(max_length=320, unique=True, nullable=False)
    role: str = ormar.String(
        max_length=7,
        nullable=False,
        choices=["user", "admin", "writer"],
        default="user",
    )


class Post(ormar.Model):
    class Meta(BaseMeta):
        tablename = "posts"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=128, nullable=False)
    content: str = ormar.Text(nullable=False)
    date: datetime.datetime = ormar.DateTime(
        nullable=False, default=datetime.datetime.now()
    )
    author: User = ormar.ForeignKey(User)


class Comment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "comments"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=32, nullable=False)
    content: str = ormar.Text(nullabl=False)
    date: datetime.datetime = ormar.DateTime(
        nullable=False, default=datetime.datetime.now()
    )
    root_post: Post = ormar.ForeignKey(Post)


class Unit(ormar.Model):
    class Meta(BaseMeta):
        tablename = "units"

    id: int = ormar.Integer(primary_key=True)
    unitname: str = ormar.String(max_length=32, nullable=False, unique=True)


class Product(ormar.Model):
    class Meta(BaseMeta):
        tablename = "products"

    id: int = ormar.Integer(primary_key=True)
    product_name: str = ormar.String(max_length=128, nullable=False)
    fats: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    proteins: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    carbohydrates: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    calories: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    base_amount: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    verified: str = ormar.String(
        max_length=12,
        nullable=False,
        choices=["verified", "not verified"],
        default="not verified",
    )
    unit: Unit = ormar.ForeignKey(Unit)


ProductCategoryRef = ForwardRef("ProductCategory")


class ProductCategory(ormar.Model):
    class Meta(BaseMeta):
        tablename = "product_categories"

    id: int = ormar.Integer(primary_key=True)
    category_name: str = ormar.String(max_length=128, nullable=False)
    root_category: ProductCategoryRef = ormar.ForeignKey(
        ProductCategoryRef, related_name="root_categories"
    )


ProductCategory.update_forward_refs()

engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
