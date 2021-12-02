from typing import ForwardRef, Optional
import databases
import ormar
import sqlalchemy
import datetime
import decimal
from pydantic import BaseModel

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class AuthCredentials(BaseModel):
    username: str
    password: str


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


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


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


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    date: Optional[datetime.datetime] = None


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


class Allergen(ormar.Model):
    class Meta(BaseMeta):
        tablename = "allergens"

    id: int = ormar.Integer(primary_key=True)
    allergen: str = ormar.String(max_length=128, nullable=False)


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
    categories: ProductCategory = ormar.ForeignKey(ProductCategory)
    allegens: Allergen = ormar.ManyToMany(
        Allergen,
        through_relation_name="product_id",
        through_reverse_relation_name="allergen_id",
    )


class Entry(ormar.Model):
    class Meta(BaseMeta):
        tablename = "entries"

    id: int = ormar.Integer(primary_key=True)
    amount: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )


class Diary(ormar.Model):
    class Meta(BaseMeta):
        tablename = "diaries"

    id: int = ormar.Integer(primary_key=True)
    date: datetime.date = ormar.Date(nullable=False, default=datetime.date.today())
    total_calories: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    total_fats: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    total_proteins: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    total_carbohydrates: decimal.Decimal = ormar.Decimal(
        max_digits=10, decimal_places=3, nullable=False
    )
    products: Product = ormar.ManyToMany(
        Product,
        through=Entry,
        through_relation_name="diary_id",
        through_reverse_relation_name="product_id",
    )
    owner: User = ormar.ForeignKey(User)


class SetCategory(ormar.Model):
    class Meta(BaseMeta):
        tablename = "set_categories"

    id: int = ormar.Integer(primary_key=True)
    category_name: str = ormar.String(max_length=128, nullable=False)


class Set(ormar.Model):
    class Meta(BaseMeta):
        tablename = "sets"

    id: int = ormar.Integer(primary_key=True)
    set_name: str = ormar.String(max_length=128, nullable=False)
    description: str = ormar.Text(nullable=True)
    owner: User = ormar.ForeignKey(User, nullable=False)
    products: Product = ormar.ManyToMany(
        Product,
        through_relation_name="set_id",
        through_reverse_relation_name="product_id",
    )
    categories: SetCategory = ormar.ManyToMany(
        SetCategory,
        through_relation_name="set_id",
        through_reverse_relation_name="category_id",
    )


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
