# app/main.py

import decimal
from fastapi import FastAPI, HTTPException, Depends, Response
from app.db import (
    database,
    AuthCredentials,
    User,
    UserUpdate,
    Post,
    PostUpdate,
    Comment,
    CommentUpdate,
    Unit,
    UnitUpdate,
    Allergen,
    AllergenUpdate,
    ProductCategory,
    ProductCategoryUpdate,
    Product,
    ProductUpdate,
    Entry,
    EntryUpdate,
    Diary,
    DiaryUpdate,
    SetCategory,
    SetCategoryUpdate,
    Set,
    SetUpdate,
)

from app.auth import AuthHandler
import asyncpg
import re
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


app = FastAPI(title="Fitapka")


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


auth_handler = AuthHandler()

# Remove it later
@app.get("/fill_db")
async def fill_db():
    conn = await asyncpg.connect("postgresql://fitapka:fitapka@db:5432/fitapka")
    tran = conn.transaction()
    await tran.start()
    with open("db/Inserts.pgsql", "r") as f:
        for line in f:
            if "INSERT" in line:
                await conn.execute(line)
    await tran.commit()
    await conn.close()
    return {"success": True}


# @app.get("/")
# async def read_root():
#     return await User.objects.all()

# authorization / retrieving Token
@app.post("/login")
async def login(auth_cred: AuthCredentials):
    user = await User.objects.get_or_none(username=auth_cred.username)
    if (user is None) or (
        not auth_handler.verify_password(auth_cred.password, user.password)
    ):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(user)
    return Response(content=json.dumps({"token": token, "user": jsonable_encoder(user)}), media_type="application/json")


# Create User
@app.post("/register", response_model=User)
async def create_user(user: User):
    if await User.objects.get_or_none(username=user.username):
        raise HTTPException(status_code=400, detail="Username is taken")
    if len(user.username) < 8:
        raise HTTPException(
            status_code=400, detail="Username must be at least 8 characters long"
        )
    if not re.fullmatch(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", user.email
    ):
        raise HTTPException(status_code=400, detail="This is not a valid email address")
    if await User.objects.get_or_none(email=user.email):
        raise HTTPException(
            status_code=400, detail=f"User with email:{user.email} already exist"
        )
    if (
        len(user.password) < 8
        or not any(char.isdigit() for char in user.password)
        or not any(char.isupper() for char in user.password)
        or not any(char.islower() for char in user.password)
    ):
        raise HTTPException(
            status_code=400,
            detail="Your password must be at least 8 characters long, contain at least one number and have a mixture of uppercase and lowercase letters.",
        )
    user.password = auth_handler.get_password_hash(user.password)
    # TODO check if role is provided and prevent creating writers and admins!!!!
    return await user.save()


# Read User
@app.get("/users/{user_id}")
async def read_user(user_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user_id != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorize")
    if (await User.objects.get_or_none(id=user_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"User of given ID: {user_id} not found"
        )
    user_data = (
        await User.objects.select_related(["diaries", "posts", "sets"])
        .filter(id=user_id)
        .all()
    )
    return user_data[0].dict(exclude_through_models=True)


# Read Users - Pagination
@app.get("/users/page/{page_number}")
async def read_users(page_number: int, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorize")
    if not (await User.objects.paginate(page_number).all()):
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    users = []
    for user_data in (
        await User.objects.select_related(["diaries", "posts", "sets"])
        .paginate(page_number)
        .all()
    ):
        users.append(user_data.dict(exclude_through_models=True))
    return users


# Update User
@app.put("/users/{user_id}")
async def update_user(
    user_id: int, update_data: UserUpdate, user=Depends(auth_handler.auth_wrapper)
):
    if (user_data := await User.objects.get_or_none(id=user_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"User of given ID: {user_id} not found"
        )
    if user_data.id != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    flags = []
    if update_data.username is not None and update_data.username != user_data.username:
        if await User.objects.get_or_none(username=update_data.username):
            raise HTTPException(status_code=400, detail="Username is taken")
        if len(update_data.username) < 8:
            raise HTTPException(
                status_code=400, detail="Username must be at least 8 characters long"
            )
        if Comment.objects.get_or_none(username=user_data.username) is not None:
            await Comment.objects.filter(username=user_data.username).update(
                each=True, username=update_data.username
            )
        flags.append("username")
    if update_data.password is not None and update_data.password != user_data.password:
        if (
            len(update_data.password) < 8
            or not any(char.isdigit() for char in update_data.password)
            or not any(char.isupper() for char in update_data.password)
            or not any(char.islower() for char in update_data.password)
        ):
            raise HTTPException(
                status_code=400,
                detail="Your password must be at least 8 characters long, contain at least one number and have a mixture of uppercase and lowercase letters.",
            )
        flags.append("password")
    if update_data.email is not None and update_data.email != user_data.email:
        if not re.fullmatch(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", update_data.email
        ):
            raise HTTPException(
                status_code=400, detail="This is not a valid email address"
            )
        if await User.objects.get_or_none(email=update_data.email):
            raise HTTPException(
                status_code=400,
                detail=f"User with email:{update_data.email} already exist",
            )
        flags.append("email")
    if update_data.role is not None and update_data.role != user_data.role  and user["role"] == "admin":
        if update_data.role in ["user", "writer", "admin"]:
            await user_data.update(role=update_data.role)
    if "username" in flags:
        await user_data.update(username=update_data.username)
    if "password" in flags:
        await user_data.update(password=update_data.password)
    if "email" in flags:
        await user_data.update(email=update_data.email)
    return user_data


# Delete User
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin" and user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (user_data := await User.objects.get_or_none(id=user_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"User of given ID: {user_id} not found"
        )

    await user_data.delete()


# Create Post
@app.post("/posts", response_model=Post)
async def create_post(post: Post, user=Depends(auth_handler.auth_wrapper)):
    post.author = user
    if user["role"] == "user":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if await Post.objects.get_or_none(title=post.title) is not None:
        raise HTTPException(
            status_code=400, detail="Post with this title already exists"
        )
    return await post.save()


# Read Post - Only One
@app.get("/posts/{post_id}")
async def read_post(post_id: int):
    if (await Post.objects.get_or_none(id=post_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Post of given ID: {post_id} don't exist"
        )
    post = await Post.objects.select_related(["comments", "author"]).filter(id=post_id).all()
    return post[0].dict(exclude_through_models=True)


# Read Posts - Pagination
@app.get("/posts/page/{page_number}")
async def read_posts(page_number: int):
    if not (await Post.objects.paginate(page_number).all()):
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    posts = []
    for post in (
        await Post.objects.select_related(["comments", "author"]).paginate(page_number).all()
    ):
        posts.append(post.dict(exclude_through_models=True))
    
    return posts


# Update Posts
@app.put("/posts/{post_id}")
async def update_post(
    post_id: int, content: PostUpdate, user=Depends(auth_handler.auth_wrapper)
):
    if user["role"] not in ["writer", "admin"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (post := await Post.objects.get_or_none(id=post_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Post of given ID: {post_id} not found"
        )
    if post.author.id != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You are not the post author")
    if content.title is not None and len(content.title) > 0:
        if post.title != content.title and await Post.objects.get_or_none(title=content.title) is not None:
            raise HTTPException(
                status_code=400, detail="Post with this title already exists"
            )
        await post.update(title=content.title)
    if content.content is not None:
        await post.update(content=content.content)
    if content.date is not None:
        await post.update(date=content.date)
    return post


# Delete Posts
@app.delete("/posts/{post_id}", status_code=204)
async def delete_post(post_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] == "user":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (post := await Post.objects.get_or_none(id=post_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Post of given ID: {post_id} not found"
        )
    if post.author.id != user["id"] and user["role"] == "writer":
        raise HTTPException(status_code=403, detail="Unauthorized")

    await post.delete()


# Create Comments
@app.post("/comments", response_model=Comment)
async def create_comment(comment: Comment, user=Depends(auth_handler.auth_wrapper)):
    if await Post.objects.get_or_none(id=comment.root_post) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Root Post of given ID: {comment.root_post} not found",
        )
    comment.username = user["username"]

    return await comment.save()


# Read Comment
@app.get("/comments/{comment_id}")
async def read_comment(comment_id: int):
    if (comment := await Comment.objects.get_or_none(id=comment_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Comment of given ID: {comment_id} not found"
        )
    return comment


# Read Comments - Pagination (Read All Comments From Post of Given ID)
@app.get("/comments/{post_id}/page/{page_number}")
async def read_comments(post_id: int, page_number: int):
    if await Post.objects.get_or_none(id=post_id) is None:
        raise HTTPException(
            status_code=404, detail=f"Post of given ID: {post_id} not found"
        )
    if not (
        comments := await Comment.objects.filter(root_post=post_id)
        .paginate(page=page_number)
        .all()
    ):
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    return comments


# Update Comment
@app.put("/comments/{comment_id}")
async def update_comment(
    comment_id: int, data: CommentUpdate, user=Depends(auth_handler.auth_wrapper)
):
    if (comment := await Comment.objects.get_or_none(id=comment_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Comment of given ID: {comment_id} not found"
        )
    if user["username"] != comment.username and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if data.username is not None and len(data.username) > 8 and user["role"] == "admin":
        await comment.update(username=data.username)
    if data.content is not None and len(data.content) > 0:
        await comment.update(content=data.content)
    if data.date is not None:
        await comment.update(date=data.date)
    return comment


# Delete Comment
@app.delete("/comments/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, user=Depends(auth_handler.auth_wrapper)):
    if (comment := await Comment.objects.get_or_none(id=comment_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Comment of given ID: {comment_id} not found"
        )
    post = await Post.objects.get_or_none(id=comment.root_post)
    if (user["username"] != comment.username and user["role"] != "admin") and int(post.author.id) != int(user["id"]):
        raise HTTPException(status_code=403, detail="Unauthorized")
    await comment.delete()


# Create Unit
@app.post("/units", response_model=Unit)
async def create_unit(unit: Unit, user=Depends(auth_handler.auth_wrapper)):
    if await Unit.objects.get_or_none(unitname=unit.unitname) is not None:
        raise HTTPException(status_code=400, detail="This unit already exist")
    if len(unit.unitname) == 0:
        raise HTTPException(status_code=400, detail="Unit need at least one character!")
    return await unit.save()


# Read Unit
@app.get("/units/{unit_id}")
async def read_unit(unit_id: int):
    if (await Unit.objects.get_or_none(id=unit_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unit of given ID: {unit_id} not found"
        )
    unit = await Unit.objects.select_related(["products"]).filter(id=unit_id).all()
    return unit[0].dict(exclude_through_models=True)


# Read Units - All
@app.get("/units")
async def read_units():
    units = []
    for unit in await Unit.objects.select_related(["products"]).all():
        units.append(unit.dict(exclude_through_models=True))
    return units


# Update Unit
@app.put("/units/{unit_id}")
async def update_unit(
    unit_id: int, data: UnitUpdate, user=Depends(auth_handler.auth_wrapper)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (unit := await Unit.objects.get_or_none(id=unit_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unit of given ID: {unit_id} not found"
        )
    if len(data.unitname) == 0:
        raise HTTPException(status_code=400, detail="Unit need at least one character!")
    if await Unit.objects.get_or_none(unitname=data.unitname) is not None:
        raise HTTPException(status_code=400, detail="This unit already exist")

    return await unit.update(unitname=data.unitname)


# Delete Unit
@app.delete("/units/{unit_id}", status_code=204)
async def delete_unit(unit_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (unit := await Unit.objects.get_or_none(id=unit_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Unit of given ID: {unit_id} not found"
        )

    await unit.delete()


# Create Allergen
@app.post("/allergens", response_model=Allergen)
async def create_allergen(allergen: Allergen, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if len(allergen.allergen) == 0:
        raise HTTPException(status_code=400, detail="Allergen cannot be empty string")
    if await Allergen.objects.get_or_none(allergen=allergen.allergen) is not None:
        raise HTTPException(
            status_code=400, detail=f"Allergen {allergen.allergen} already exist"
        )
    return await allergen.save()


# Read Allergen
@app.get("/allergens/{allergen_id}")
async def read_allergen(allergen_id: int):
    if (
        allergen := await Allergen.objects.select_related(["products"]).get_or_none(
            id=allergen_id
        )
    ) is None:
        raise HTTPException(
            status_code=404, detail=f"Allergen of given ID: {allergen_id} not found"
        )
    return allergen.dict(exclude_through_models=True)


# Read Allergens - all
@app.get("/allergens")
async def read_allergens_all():
    allergens = []
    for allergen in await Allergen.objects.select_related(["products"]).all():
        allergens.append(allergen.dict(exclude_through_models=True))
    return allergens


# Read Allergens - pagination
@app.get("/allergens/page/{page_number}")
async def read_allergens(page_number: int):
    if not (await Allergen.objects.paginate(page=page_number).all()):
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    allergens = []
    for allergen in (
        await Allergen.objects.select_related(["products"]).paginate(page_number).all()
    ):
        allergens.append(allergen.dict(exclude_through_models=True))
    return allergens


# Update Allergen
@app.put("/allergens/{allergen_id}")
async def update_allergens(
    allergen_id: int, data: AllergenUpdate, user=Depends(auth_handler.auth_wrapper)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (allergen := await Allergen.objects.get_or_none(id=allergen_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Allergen of given ID: {allergen_id} not found"
        )
    if data.allergen is not None:
        if len(data.allergen) == 0:
            raise HTTPException(
                status_code=400, detail="Allergen cannot be empty string"
            )
        if await Allergen.objects.get_or_none(allergen=data.allergen) is not None:
            raise HTTPException(
                status_code=400, detail=f"Allergen {data.allergen} already exist"
            )
        await allergen.update(allergen=data.allergen)
    return allergen


# Delete Allergen
@app.delete("/allergens/{allergen_id}", status_code=204)
async def delete_allergen(allergen_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (allergen := await Allergen.objects.get_or_none(id=allergen_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Allergen of given ID: {allergen_id} not found"
        )
    await allergen.delete()


# Create Product Category
@app.post("/product_categories", response_model=ProductCategory)
async def create_product_category(
    product_category: ProductCategory, user=Depends(auth_handler.auth_wrapper)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if len(product_category.category_name) == 0:
        raise HTTPException(
            status_code=400, detail="Product Category Name cannot be empty string"
        )
    if (
        await ProductCategory.objects.get_or_none(
            category_name=product_category.category_name
        )
        is not None
    ):
        raise HTTPException(
            status_code=400, detail="This Product Category already exist"
        )
    if (
        product_category.root_category is not None
        and (
            root_category := await ProductCategory.objects.get_or_none(
                id=product_category.root_category
            )
        )
        is None
    ):
        raise HTTPException(
            status_code=404,
            detail=f"Root Category: Product Category of given ID: {product_category.root_category} not found",
        )
    product_category.root_category = root_category
    return await product_category.save()


# Read Product Category
@app.get("/product_categories/{category_id}")
async def read_product_category(category_id: int):
    if (
        product_category := await ProductCategory.objects.select_related(
            ["products", "root_categories"]
        ).get_or_none(id=category_id)
    ) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product Category of given ID: {category_id} not found",
        )
    return product_category.dict(exclude_through_models=True)


# Read Product Categories - All
@app.get("/product_categories")
async def read_product_categories_all():
    product_categories = []
    for category in (
        await ProductCategory.objects.select_related(["products", "root_categories"])
        .filter(root_category=None)
        .all()
    ):
        product_categories.append(category.dict(exclude_through_models=True))
    return product_categories


# Read Product Categories - Pagination
@app.get("/product_categories/page/{page_number}")
async def read_product_categories(page_number: int):
    if not (await ProductCategory.objects.paginate(page=page_number).all()):
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    product_categories = []
    for category in await ProductCategory.objects.select_related(
        ["products", "root_categories"]
    ).all():
        product_categories.append(category.dict(exclude_through_models=True))
    return product_categories


# Update Product Category
@app.put("/product_categories/{category_id}")
async def upate_product_category(
    category_id: int,
    data: ProductCategoryUpdate,
    user=Depends(auth_handler.auth_wrapper),
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (
        product_category := await ProductCategory.objects.get_or_none(id=category_id)
    ) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product Category of given ID: {category_id} not found",
        )
    if data.category_name is not None:
        if len(data.category_name) == 0:
            raise HTTPException(
                status_code=400, detail="Product Category Name cannot be empty string"
            )
        if (
            await ProductCategory.objects.get_or_none(category_name=data.category_name)
            is not None
        ):
            raise HTTPException(
                status_code=400, detail="This Product Category already exist"
            )
        await product_category.update(category_name=data.category_name)
    if (
        data.root_category is not None
        and (await ProductCategory.objects.get_or_none(id=data.root_category)) is None
    ):
        raise HTTPException(
            status_code=404,
            detail=f"Root Category: Product Category of given ID: {product_category.root_category} not found",
        )
    if data.root_category is None and product_category.root_category is not None:
        child_categories = (
            await product_category.root_category.root_categories.select_all().all()
        )
        for category in child_categories:
            if category.id == product_category.id:
                await product_category.root_category.root_categories.remove(category)
        return category
    else:
        await product_category.update(root_category=data.root_category)

    return product_category


# Delete Product Category
@app.delete("/product_categories/{category_id}", status_code=204)
async def delete_product_category(
    category_id: int, user=Depends(auth_handler.auth_wrapper)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (
        product_category := await ProductCategory.objects.get_or_none(id=category_id)
    ) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product Category of given ID: {category_id} not found",
        )
    await product_category.delete()


# Create Product
@app.post("/products")
async def create_product(product: Product, user=Depends(auth_handler.auth_wrapper)):
    if len(product.product_name) == 0:
        raise HTTPException(
            status_code=400, detail="Product Name cannot be an empty string."
        )
    if await Product.objects.get_or_none(product_name=product.product_name) is not None:
        raise HTTPException(
            status_code=400, detail="Product with this name already exists"
        )
    if product.fats < 0:
        raise HTTPException(status_code=400, detail="Fats value cannot be negative")
    if product.proteins < 0:
        raise HTTPException(status_code=400, detail="Proteins value cannot be negative")
    if product.carbohydrates < 0:
        raise HTTPException(
            status_code=400, detail="Carbohydrates value cannot be negative"
        )
    if product.calories < 0:
        raise HTTPException(status_code=400, detail="Calories value cannot be negative")
    if product.base_amount < 0:
        raise HTTPException(
            status_code=400, detail="Base Amount value cannot be negative"
        )
    if product.fats + product.proteins + product.carbohydrates > product.base_amount:
        raise HTTPException(
            status_code=400,
            detail="Sum of Fats, Proteins and Carbohydrates cannot be higher than Base Amount",
        )
    if user["role"] == "admin":
        product.verified = "verified"
    else:
        product.verified = "not verified"
    if await Unit.objects.get_or_none(id=product.unit) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product: Unit of given ID: {product.unit} not found",
        )
    if await Unit.objects.get_or_none(id=product.categories) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product: Category of given ID: {product.categories} not found",
        )
    if product.allergens is not None:
        allergens = []
        for allergen_id in product.allergens:
            if (allergen := await Allergen.objects.get_or_none(id=allergen_id)) is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product: Allergen of given ID: {allergen_id} not found",
                )
            allergens.append(allergen)
    product.allergens = []
    product = await product.save()
    if allergens:
        for allergen in allergens:
            await product.allergens.add(allergen)
    return product


# Get Product Proportions
@app.get("/products/{product_id}/proportions/{amount}")
async def get_proportions(product_id: int, amount: decimal.Decimal):
    if (await Product.objects.get_or_none(id=product_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Product of given ID: {product_id} not found"
        )
    conn = await asyncpg.connect("postgresql://fitapka:fitapka@db:5432/fitapka")
    tran = conn.transaction()
    await tran.start()
    stmt = await conn.prepare('''SELECT * FROM getProportions($1::integer, $2::numeric)''')
    product_values = await stmt.fetch(product_id, float(amount))
    await tran.commit()
    await conn.close()

    return product_values[0]


# Read Product
@app.get("/products/{product_id}")
async def read_product(product_id: int):
    if (await Product.objects.get_or_none(id=product_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Product of given ID: {product_id} not found"
        )
    products = (
        await Product.objects.select_related(["allergens", "sets", "unit", "categories"])
        .get_or_none(id=product_id)
    )
    return products.dict(exclude_through_models=True)


# Read Products - Paginate
@app.get("/products/page/{page_number}")
async def read_products(page_number: int):
    if not (products := await Product.objects.paginate(page=page_number).all()):
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    products = []
    for product in (
        await Product.objects.select_related(["allergens", "sets", "unit", "categories"])
        .paginate(page_number)
        .all()
    ):
        products.append(product.dict(exclude_through_models=True))
    return products


# Update Products
@app.put("/products/{product_id}")
async def update_product(
    product_id: int, data: ProductUpdate, user=Depends(auth_handler.auth_wrapper)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (product := await Product.objects.get_or_none(id=product_id)) is None:
        raise HTTPException(
            status_code=400, detail=f"Product with given ID: {product_id} not found"
        )
    flags = []
    if data.product_name is not None:
        if len(data.product_name) == 0:
            raise HTTPException(
                status_code=400, detail="Product Name cannot be an empty string"
            )
        if (
            await Product.objects.get_or_none(product_name=data.product_name)
            is not None
        ):
            raise HTTPException(
                status_code=400, detail="Product with that name already exists"
            )
        flags.append("product_name")
    if data.fats is not None:
        if data.fats < 0:
            raise HTTPException(status_code=400, detail="Fats value cannot be negative")
        flags.append("fats")
    if data.proteins is not None:
        if data.proteins < 0:
            raise HTTPException(
                status_code=400, detail="Proteins value cannot be negative"
            )
        flags.append("proteins")
    if data.carbohydrates is not None:
        if data.carbohydrates < 0:
            raise HTTPException(
                status_code=400, detail="Carbohydrates value cannot be negative"
            )
        flags.append("carbohydrates")
    if data.calories is not None:
        if data.calories < 0:
            raise HTTPException(
                status_code=400, detail="Calories value cannot be negative"
            )
        flags.append("calories")
    sum = 0
    for val in ["fats", "proteins", "carbohydrates"]:
        if val == "fats":
            if val in flags:
                sum += data.fats
            else:
                sum += product.fats
        if val == "proteins":
            if val in flags:
                sum += data.proteins
            else:
                sum += product.proteins
        if val == "carbohydrates":
            if val in flags:
                sum += data.carbohydrates
            else:
                sum += product.carbohydrates
    if data.base_amount is not None:
        if data.base_amount < 0:
            raise HTTPException(
                status_code=400, detail="Base amount value cannot be negative"
            )
        flags.append("base_amount")
        if sum > data.base_amount:
            raise HTTPException(
                status_code=400,
                detail="Sum of Fats, Proteins and Carbohydrates cannot be higher than Base Amount",
            )
    else:
        if sum > product.base_amount:
            raise HTTPException(
                status_code=400,
                detail="Sum of Fats, Proteins and Carbohydrates cannot be higher than Base Amount",
            )
    if data.verified is not None:
        if data.verified not in ["verified", "not verified"]:
            raise HTTPException(
                status_code=400, detail="Product can only be verified or not verified"
            )
        flags.append("verified")
    if data.unit is not None:
        if await Unit.objects.get_or_none(id=data.unit) is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product: Unit of given ID: {data.unit} not found",
            )
        flags.append("unit")
    if data.categories is not None:
        if await ProductCategory.objects.get_or_none(id=data.categories) is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product: Product Category of given ID: {data.categories} not found",
            )
        flags.append("categories")
    if data.allergens is None or len(data.allergens) == 0:
        if allergens := await product.allergens.select_all().all():
            for allergen in allergens:
                await product.allergens.remove(allergen)
    if data.allergens is not None and len(data.allergens) > 0:
        if allergens := await product.allergens.select_all().all():
            for allergen in allergens:
                await product.allergens.remove(allergen)
        for allergen_id in data.allergens:
            if allergen := await Allergen.objects.get_or_none(id=allergen_id):
                await product.allergens.add(allergen)
    if "product_name" in flags:
        await product.update(product_name=data.product_name)
    if "fats" in flags:
        await product.update(fats=data.fats)
    if "proteins" in flags:
        await product.update(proteins=data.proteins)
    if "carbohydrates" in flags:
        await product.update(carbohydrates=data.carbohydrates)
    if "calories" in flags:
        await product.update(calories=data.calories)
    if "base_amount" in flags:
        await product.update(base_amount=data.base_amount)
    if "verified" in flags:
        await product.update(verified=data.verified)
    if "unit" in flags:
        await product.update(unit=data.unit)
    if "categories" in flags:
        await product.update(categories=data.categories)

    return product


# Delete Product
@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (product := await Product.objects.get_or_none(id=product_id)) is None:
        raise HTTPException(
            status_code=404, detail=f"Product with given ID: {product_id} not found"
        )
    await product.delete()


# Create Diary
@app.post("/diaries", response_model=Diary)
async def create_diary(diary: Diary, user=Depends(auth_handler.auth_wrapper)):
    if await Diary.objects.get_or_none(date=diary.date):
        raise HTTPException(status_code=400, detail="You cannot create second diary on the same date")
    if diary.total_calories < 0:
        raise HTTPException(status_code=400, detail="Total Calories cannot be negative number")
    if diary.total_fats < 0:
        raise HTTPException(status_code=400, detail="Total Fats cannot be negative number")
    if diary.total_carbohydrates < 0:
        raise HTTPException(status_code=400, detail="Total Carbohydrates cannot be negative number")
    if diary.total_proteins < 0:
        raise HTTPException(status_code=400, detail="Total Proteins cannot be negative number")
    diary.owner = await User.objects.get(id=user["id"])
    return await diary.save()


# Read Diary
@app.get("/diaries/{diary_id}")
async def read_diary(diary_id: int, user=Depends(auth_handler.auth_wrapper)):
    if (await Diary.objects.get_or_none(id=diary_id)) is None:
        raise HTTPException(status_code=404, detail=f"Diary of given ID: {diary_id} not found")
    diary = await Diary.objects.select_related(["owner"]).filter(id=diary_id).all()
    if diary[0].owner.id != user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return diary[0].dict(exclude_through_models=True)


# Read Diaries - Paginate
@app.get("/diaries/page/{page_number}")
async def read_diary(page_number: int, user=Depends(auth_handler.auth_wrapper)):
    if not (await Diary.objects.paginate(page=page_number).filter(owner__id=user["id"]).all()):
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    diaries = []
    for diary in await Diary.objects.select_related([Diary.owner]).paginate(page_number).filter(owner__id=user["id"]).all():
        diaries.append(diary.dict(exclude_through_models=True))
    return diaries


# Update Diary
@app.put("/diaries/{diary_id}")
async def update_diary(diary_id: int, data: DiaryUpdate, user=Depends(auth_handler.auth_wrapper)):
    if (diary := await Diary.objects.get_or_none(id=diary_id)) is None:
        raise HTTPException(status_code=404, detail=f"Diary of given ID: {diary_id} not found")
    if await Diary.objects.get_or_none(date=data.date):
        raise HTTPException(status_code=404, detail=f"Diary of given Date: {data.date} already exists")
    if data.date is not None:
        await diary.update(date=data.date)
    return diary


# Delete Diary
@app.delete("/diaries/{diary_id}", status_code=204)
async def delete_diary(diary_id: int, user=Depends(auth_handler.auth_wrapper)):
    if (diary := await Diary.objects.get_or_none(id=diary_id)) is None:
        raise HTTPException(status_code=404, detail=f"Diary of given ID: {diary_id} not found")
    if diary.owner.id != user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    await diary.delete()


# Create Entry
@app.post("/entries", response_model=Entry)
async def create_entry(entry: Entry, user=Depends(auth_handler.auth_wrapper)):
    if await Entry.objects.get_or_none(product_id=entry.product_id, diary_id=entry.diary_id):
        raise HTTPException(status_code=400, detail=f"This entry already exists")
    if (diary := await Diary.objects.get_or_none(id=entry.diary_id.id)) is None:
        raise HTTPException(status_code=404, detail=f"Diary of given ID: {entry.diary_id.id} does not exist")
    if (product := await Product.objects.get_or_none(id=entry.product_id.id)) is None:
        raise HTTPException(status_code=404, detail=f"Product of given ID: {entry.product_id.id} does not exist")
    if diary.owner.id != user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if entry.amount < 0:
        raise HTTPException(status_code=400, detail="Entry amount cannot be negative number")
    entry.product_id = product
    entry.diary_id = diary
    
    conn = await asyncpg.connect("postgresql://fitapka:fitapka@db:5432/fitapka")
    await conn.execute(f"CALL updateDiary({int(entry.diary_id.id)}, {int(entry.product_id.id)}, {0})")
    await conn.close()

    return await entry.save()


# Read Entry
@app.get("/entries/{entry_id}")
async def read_entry(entry_id: int, user=Depends(auth_handler.auth_wrapper)):
    if (entry := await Entry.objects.get_or_none(id=entry_id)) is None:
        raise HTTPException(status_code=404, detail=f"Entry of given ID: {entry_id} not found")
    diary = await Diary.objects.get(id=entry.diary_id.id)
    if diary.owner.id != user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return entry


# Read All Entries for certain Diary
@app.get("/entries/diary/{diary_id}")
async def read_entries(diary_id: int, user=Depends(auth_handler.auth_wrapper)):
    if not (entries := await Entry.objects.filter(diary_id=diary_id).all()):
        raise HTTPException(status_code=404, detail=f"There are noe entries for diary of given ID: {diary_id}")
    diary = await Diary.objects.get(id=diary_id)
    if diary.owner.id != user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return entries


# Update Entry
@app.put("/entries/{entry_id}")
async def update_entry(entry_id: int, data:EntryUpdate, user=Depends(auth_handler.auth_wrapper)):
    if not (entry := await Entry.objects.get_or_none(id=entry_id)):
        raise HTTPException(status_code=404, detail=f"Entry of given ID: {entry_id} not found")
    diary = await Diary.objects.get(id=entry.diary_id.id)
    if diary.owner.id != user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if data.amount is not None and data.amount > 0:
        amount = entry.amount
        await entry.update(amount=data.amount)

        # Update Diary
        conn = await asyncpg.connect("postgresql://fitapka:fitapka@db:5432/fitapka")
        await conn.execute(f"CALL updateDiary({int(entry.diary_id.id)}, {int(entry.product_id.id)}, {amount})")
        await conn.close()
    return entry


# Delete Entry
@app.delete("/entries/{entry_id}", status_code=204)
async def delete_entry(entry_id: int, user=Depends(auth_handler.auth_wrapper)):
    if not (entry := await Entry.objects.get_or_none(id=entry_id)):
        raise HTTPException(status_code=404, detail=f"Entry of given ID: {entry_id} not found")
    diary = await Diary.objects.get(id=entry.diary_id.id)
    if diary.owner.id != user["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")

    conn = await asyncpg.connect("postgresql://fitapka:fitapka@db:5432/fitapka")
    await conn.execute(f"CALL updateDiary({int(entry.diary_id.id)}, {int(entry.product_id.id)}, {2 * entry.amount})")
    await conn.close()

    await entry.delete()


# Create Set Category
@app.post("/set_categories", response_model=SetCategory)
async def create_set_category(set_category: SetCategory, user=Depends(auth_handler.auth_wrapper)):
    if user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Unauthorized")
    if set_category.category_name is None or len(set_category.category_name) == 0:
        raise HTTPException(status_code=400, detail='Category Name cannot be empty')
    if await SetCategory.objects.get_or_none(category_name=set_category.category_name):
        raise HTTPException(status_code=400, detail=f"Category {set_category.category_name} already exists")
    return await set_category.save()


# Read Set Category
@app.get("/set_categories/{category_id}")
async def read_set_category(category_id: int):
    if (set_category := await SetCategory.objects.select_related(['sets']).get_or_none(id=category_id)) is None:
        raise HTTPException(status_code=404, detail=f"Set Category of given ID: f{category_id} not found")
    return set_category.dict(exclude_through_models=True)


# Read Set Categories - All
@app.get("/set_categories")
async def read_set_categories():
    set_categories = await SetCategory.objects.select_related(['sets']).all()
    return [set_category.dict(exclude_through_models=True) for set_category in set_categories]


# Update Set Category
@app.put("/set_categories/{category_id}")
async def update_set_category(category_id: int, data:SetCategoryUpdate, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (set_category := await SetCategory.objects.select_related(['sets']).get_or_none(id=category_id)) is None:
        raise HTTPException(status_code=404, detail=f"Set Category of given ID: f{category_id} not found")
    if data.category_name:
        if await SetCategory.objects.get_or_none(category_name=data.category_name):
            raise HTTPException(status_code=400, detail=f"Category {data.category_name} already exists")
        await set_category.update(category_name= data.category_name)
    return set_category


# Delete Set Category
@app.delete("/set_categories/{category_id}", status_code=204)
async def delete_set_category(category_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (set_category := await SetCategory.objects.select_related(['sets']).get_or_none(id=category_id)) is None:
        raise HTTPException(status_code=404, detail=f"Set Category of given ID: f{category_id} not found")
    
    await set_category.delete()


# Create Set
@app.post("/sets", response_model=Set)
async def create_set(set: Set, user=Depends(auth_handler.auth_wrapper)):
    if not set.set_name:
        raise HTTPException(status_code=400, detail="Set name cannot be an empty string")
    if await Set.objects.get_or_none(owner=user["id"], set_name=set.set_name):
        raise HTTPException(status_code=400, detail=f"Set {set.set_name} already exists")
    set.owner = await User.objects.get(id=user["id"])
    return await set.save()


# Read Set
@app.get("/sets/{set_id}")
async def read_set(set_id: int, user=Depends(auth_handler.auth_wrapper)):
    if (set := await Set.objects.select_related(['owner', 'products', 'categories']).get_or_none(id=set_id)) is None:
        raise HTTPException(status_code=404, detail=f"Set of given ID: {set_id} not found")
    if user["id"] != set.owner.id:
        raise HTTPException(status_code=402, detail="Unauthorized")
    return set.dict(exclude_through_models=True)


# Read Sets - Paginate
@app.get("/sets/page/{page_number}")
async def read_sets(page_number: int, user=Depends(auth_handler.auth_wrapper)):
    if not (sets := await Set.objects.select_related(['owner', 'products', 'categories']).paginate(page_number).filter(owner__id=user["id"]).all()):
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    return [set.dict(exclude_through_models=True) for set in sets]


# Update Set
@app.put("/sets/{set_id}")
async def update_set(set_id: int, data: SetUpdate, user=Depends(auth_handler.auth_wrapper)):
    if (set := await Set.objects.select_related(['owner', 'products', 'categories']).get_or_none(id=set_id)) is None:
        raise HTTPException(status_code=404, detail=f"Set of given ID: {set_id} not found")
    if user["id"] != set.owner.id:
        raise HTTPException(status_code=402, detail="Unauthorized")
    if data.set_name and set.set_name != data.set_name:
        if await Set.objects.get_or_none(owner=user["id"], set_name=data.set_name):
            raise HTTPException(status_code=400, detail=f"Set {data.set_name} already exists")
        await set.update(set_name=data.set_name)
    await set.update(description= data.description)

    if data.products is None or len(data.products) == 0:
        temp = await Set.objects.select_related(["products"]).get_or_none(id=set_id)
        if products := temp.products:
            for product in products:
                await set.products.remove(product)
    if data.products is not None and len(data.products) > 0:
        temp = await Set.objects.select_related(["products"]).get_or_none(id=set_id)
        if products := temp.products:
            for product in products:
                await set.products.remove(product)
        for product_id in data.products:
            if product := await Product.objects.get_or_none(id=product_id):
                await set.products.add(product)
    
    if data.categories is None or len(data.categories) == 0:
        if categories := await set.categories.select_all().all():
            for category in categories:
                await set.categories.remove(category)
    if data.categories is not None and len(data.categories) > 0:
        if categories := await set.categories.select_all().all():
            for category in categories:
                await set.categories.remove(category)
        for category_id in data.categories:
            if category := await SetCategory.objects.get_or_none(id=category_id):
                await set.categories.add(category)
    return set


# Delete Set
@app.delete("/sets/{set_id}", status_code=204)
async def delete_set(set_id: int, user=Depends(auth_handler.auth_wrapper)):
    if (set := await Set.objects.get_or_none(id=set_id)) is None:
        raise HTTPException(status_code=404, detail=f"Set of given ID: {set_id} not found")
    if set.owner.id != user["id"]:
        raise HTTPException(status_code=402, detail="Unauthorized")
    await set.delete()


@app.on_event("startup")
async def startup():
    conn = await asyncpg.connect("postgresql://fitapka:fitapka@db:5432/fitapka")
    tran = conn.transaction()
    await tran.start()
    with open("db/AlterTable.pgsql", "r") as f:
        data = f.read()
        await conn.execute(data)
    with open("db/Package.pgsql", "r") as f:
        data = f.read()
        await conn.execute(data)
    await tran.commit()
    await conn.close()
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
