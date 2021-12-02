# app/main.py

from datetime import datetime
from os import stat
from asyncpg.connection import connect
from fastapi import FastAPI, HTTPException, Depends

from app.db import CommentUpdate, database, AuthCredentials, User, UserUpdate, Post, PostUpdate, Comment, Unit, Allergen, ProductCategory, Product, Entry, Diary, SetCategory, Set

from app.auth import AuthHandler
import asyncpg

app = FastAPI(title="Fitapka")


auth_handler = AuthHandler()

# Remove it later
@app.get("/fill_db")
async def fill_db():
    conn = await asyncpg.connect('postgresql://fitapka:fitapka@db:5432/fitapka')
    tran = conn.transaction()
    await tran.start()
    with open('db/Inserts.pgsql', 'r') as f:
        for line in f:
            if 'INSERT' in line:
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
    if (user is None) or (not auth_handler.verify_password(auth_cred.password, user.password)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user)
    return {'token': token}

# Create User
@app.post("/register", response_model=User)
async def create_user(user: User):
    if await User.objects.get_or_none(username=user.username):
        raise HTTPException(status_code=400, detail='Username is taken')
    if await User.objects.get_or_none(email=user.email):
        raise HTTPException(status_code=400, detail=f'User with email:{user.email} already exist')
    if len(user.password) < 8 or\
            not any(char.isdigit() for char in user.password) or\
            not any(char.isupper() for char in user.password) or\
            not any(char.islower() for char in user.password):
        raise HTTPException(status_code=400, detail='Your password must be at least 8 characters long, contain at least one number and have a mixture of uppercase and lowercase letters.')
    user.password = auth_handler.get_password_hash(user.password)
    # TODO check if role is provided and prevent creating writers and admins!!!!
    return await user.save()


# Read User
@app.get("/user/{user_id}")
async def read_user(user_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user_id != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorize")
    if (user_data := await User.objects.get_or_none(id=user_id)) is None:
        raise HTTPException(status_code=404, detail=f"User of given ID: {user_id} not found")
    return user_data


# Read Users - Pagination
@app.get("/users/{page_number}")
async def read_users(page_number: int, user=Depends(auth_handler.auth_wrapper)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Unauthorize")
    if not (users := await User.objects.paginate(page_number).all()):
        raise HTTPException(status_code=404, detail=f'Page {page_number} not found')
    return users


# Update User
@app.put("/update_user/{user_id}")
async def update_user(user_id: int, update_data: UserUpdate, user=Depends(auth_handler.auth_wrapper)):
    if (user_data := await User.objects.get_or_none(id=user_id)) is None:
        raise HTTPException(status_code=404, detail=f"User of given ID: {user_id} not found")
    if user_data.id != user['id'] and user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Unauthorized")
    if update_data.username is not None:
        if await User.objects.get_or_none(username=update_data.username):
            raise HTTPException(status_code=400, detail='Username is taken')
        if Comment.objects.get_or_none(username=user_data.username) is not None:
            await Comment.objects.filter(username=user_data.username).update(each=True, username=update_data.username)
        await user_data.update(username=update_data.username)
    if update_data.password is not None:
        if len(update_data.password) < 8 or\
            not any(char.isdigit() for char in update_data.password) or\
            not any(char.isupper() for char in update_data.password) or\
            not any(char.islower() for char in update_data.password):
            raise HTTPException(status_code=400, detail='Your password must be at least 8 characters long, contain at least one number and have a mixture of uppercase and lowercase letters.')
        await user_data.update(password=update_data.password)
    if update_data.email is not None:
        if await User.objects.get_or_none(email=update_data.email):
            raise HTTPException(status_code=400, detail=f'User with email:{update_data.email} already exist')
        await user_data.update(email=update_data.email)
    if update_data.role is not None and user['role'] == 'admin':
        if update_data.role in ['user', 'writer', 'admin']:
            await user_data.update(role=update_data.role)
    return user_data


# Delete User
@app.delete("/delete_user/{user_id}", status_code=204)
async def delete_user(user_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user['role'] != 'admin' and user['id'] != user_id:
        raise HTTPException(status_code=403, detail='Unauthorized')
    if (user_data := await User.objects.get_or_none(id=user_id)) is None:
        raise HTTPException(status_code=404, detail=f"User of given ID: {user_id} not found")

    await user_data.delete()


# Create Post
@app.post("/create_post", response_model=Post)
async def create_post(post: Post, user=Depends(auth_handler.auth_wrapper)):
    post.author = user
    if user['role'] == "user":
        raise HTTPException(status_code=403, detail='Unauthorized')
    return await post.save()

# Read Post - Only One
@app.get("/read_post/{post_id}")
async def read_post(post_id: int):
    if (post := await Post.objects.get_or_none(id=post_id)) is None:
        raise HTTPException(status_code=404, detail=f'Post of given ID: {post_id} don\'t exist')
    return post


# Read Posts - Pagination
@app.get("/read_posts/{page_number}")
async def read_posts(page_number: int):
    if not (posts := await Post.objects.paginate(page_number).all()):
        raise HTTPException(status_code=404, detail=f'Page {page_number} not found')
    return posts


# Update Posts
@app.put("/update_post/{post_id}")
async def update_post(post_id: int, content: PostUpdate, user=Depends(auth_handler.auth_wrapper)):
    if user['role'] not in ['writer', 'admin']:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (post := await Post.objects.get_or_none(id=post_id)) is None:
        raise HTTPException(status_code=404, detail=f"Post of given ID: {post_id} not found")
    if post.author.id != user['id'] and user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="You are not the post author")
    if content.title is not None:
        await post.update(title=content.title)
    if content.content is not None:
        await post.update(content=content.content)
    if content.date is not None:
        await post.update(date=content.date)
    return post


# Delete Posts
@app.delete("/delete_post/{post_id}", status_code=204)
async def delete_post(post_id: int, user=Depends(auth_handler.auth_wrapper)):
    if user['role'] == 'user':
        raise HTTPException(status_code=403, detail="Unauthorized")
    if (post := await Post.objects.get_or_none(id=post_id)) is None:
        raise HTTPException(status_code=404, detail=f"Post of given ID: {post_id} not found")
    if (post.author.id != user['id'] and user['role'] == "writer"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    await post.delete()

# Create Comments
@app.post("/create_comment", response_model=Comment)
async def create_comment(comment: Comment, user=Depends(auth_handler.auth_wrapper)):
    if await Post.objects.get_or_none(id=comment.root_post) is None:
        raise HTTPException(status_code=404, detail=f"Root Post of given ID: {comment.root_post} not found")
    comment.username = user['username']
    
    return await comment.save()


# Read Comment
@app.get("/read_comment/{comment_id}")
async def read_comment(comment_id: int):
    if (comment := await Comment.objects.get_or_none(id=comment_id)) is None:
        raise HTTPException(status_code=404, detail=f"Comment of given ID: {comment_id} not found")
    return comment


# Read Comments - Pagination (Read All Comments From Post of Given ID) 
@app.get("/read_comments/{post_id}/{page_number}")
async def read_comments(post_id: int, page_number: int):
    if await Post.objects.get_or_none(id=post_id) is None:
        raise HTTPException(status_code=404, detail=f"Post of given ID: {post_id} not found")
    if not (comments := await Comment.objects.filter(root_post=post_id).paginate(page=page_number).all()):
        raise HTTPException(status_code=404, detail=f'Page {page_number} not found')
    return comments


# Update Comment
@app.put("/update_comment/{comment_id}")
async def update_comment(comment_id: int, data: CommentUpdate, user=Depends(auth_handler.auth_wrapper)):
    if (comment := await Comment.objects.get_or_none(id=comment_id)) is None:
        raise HTTPException(status_code=404, detail=f"Comment of given ID: {comment_id} not found")
    if user["username"] != comment.username and user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Unauthorized")
    if data.username is not None and len(data.username) > 8 and user['role'] == 'admin':
        await comment.update(username = data.username)
    if data.content is not None and len(data.content) > 0:
        await comment.update(content = data.content)
    if data.date is not None:
        await comment.update(date = data.date)
    return comment


# Delete Comment
@app.delete("/delete_comment/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, user=Depends(auth_handler.auth_wrapper)):
    if (comment := await Comment.objects.get_or_none(id=comment_id)) is None:
        raise HTTPException(status_code=404, detail=f"Comment of given ID: {comment_id} not found")
    if user["username"] != comment.username and user["role"] != 'admin':
        raise HTTPException(status_code=403, detail="Unauthorized")
    await comment.delete()


@app.post("/create_unit", response_model=Unit)
async def create_unit(unit: Unit):
    return await unit.save()


@app.post("/create_allergen", response_model=Allergen)
async def create_allergen(allergen: Allergen):
    return await allergen.save()


@app.post("/create_product_categorie", response_model=ProductCategory)
async def create_product_category(product_category: ProductCategory):
    return await product_category.save()


@app.post("/create_product", response_model=Product)
async def create_product(product: Product):
    return await product.save()


@app.post("/create_entry", response_model=Entry)
async def create_entry(entry: Entry):
    return await entry.save()


@app.post("/create_diary", response_model=Diary)
async def create_diary(diary: Diary):
    return await diary.save()


@app.post("/create_set_category", response_model=SetCategory)
async def create_set_category(set_category: SetCategory):
    return await set_category.save()


@app.post("/create_set", response_model=Set)
async def create_set(set: Set):
    return await set.save()


@app.on_event("startup")
async def startup():
    conn = await asyncpg.connect('postgresql://fitapka:fitapka@db:5432/fitapka')
    tran = conn.transaction()
    await tran.start()
    with open('db/AlterTable.pgsql', 'r') as f:
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
