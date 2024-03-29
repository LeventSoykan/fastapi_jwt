import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import JWTBearer
import app.db_manager as db

# posts = [
#     {
#         'id': 1,
#         'title': 'penguins',
#         'content': 'text for penguins'
#     },
# {
#         'id': 2,
#         'title': 'tigers',
#         'content': 'text for tigers'
#     },
# {
#         'id': 3,
#         'title': 'koalas',
#         'content': 'text for koalas'
#     }
# ]
#
# users = []

app = FastAPI()

#Get  - for testin
@app.get('/', tags=['test'])
def greet():
    return {'Hello': 'World'}

#Get posts
@app.get('/posts', tags=['posts'])
def get_posts():
    return {'data': db.get_posts()}


#Get single post {id}
@app.get('/posts/{id}', tags=['posts'])
def get_one_post(id : int):
    posts = db.get_posts()
    if id > len(posts):
        return {
            'error': 'Post with this ID does not exist!'
        }
    for post in posts:
        if post['id'] == id:
            return {
                'data': post
            }

#Creating a post
@app.post('/posts', dependencies=[Depends(JWTBearer())], tags=['posts'])
def add_post(post: PostSchema):
    db.add_post(post)
    return {
        'info': 'post_added'
    }

#Signup new user
@app.post('/user/signup', tags=['user'])
def user_signup(user: UserSchema = Body(default=None)):
    db.add_user(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    return db.check_user(data)

@app.post('/user/login', tags=['user'])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            'error': 'Incorrect login details!'
        }
