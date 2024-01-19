from decouple import config
from sqlalchemy import create_engine, text
from .model import PostSchema, UserSchema, UserLoginSchema

PG_CON_STRING = config('postgres')
engine = create_engine(f'{PG_CON_STRING}fastapi')

def add_post(post: PostSchema):
    query = '''
    INSERT INTO posts (title, content)
    VALUES (:title, :content)
    '''
    with engine.connect() as con:
        con.execute(text(query).bindparams(title=post.title, content=post.content))
        con.commit()

def get_posts():
    query = '''
        SELECT * FROM posts
        '''
    with engine.connect() as con:
        result = con.execute(text(query))
    posts = []
    for res in result.fetchall():
        posts.append({'id': res[0], 'title': res[1], 'content': res[2]})
    return posts

def get_post(id: int):
    query = '''
        SELECT * FROM posts WHERE id=:id
        '''
    with engine.connect() as con:
        result = con.execute(text(query).bindparams(id=id))
    res = result.fetchone()
    return {'id':res[0], 'title':res[1], 'content':res[2]}

def add_user(user: UserSchema):
    query = '''
    INSERT INTO users (fullname, email, password)
    VALUES (:fullname, :email, :password)
    '''
    with engine.connect() as con:
        con.execute(text(query).bindparams(fullname=user.fullname, email=user.email, password=user.password))
        con.commit()

def check_user(data: UserLoginSchema):
    query = '''
    SELECT * FROM users WHERE email=:email AND password=:password 
    '''
    with engine.connect() as con:
        result = con.execute(text(query).bindparams(email=data.email, password=data.password))
    if result.fetchone():
        return True
    return False

