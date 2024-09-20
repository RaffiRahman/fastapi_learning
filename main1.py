from typing import Optional
from fastapi import FastAPI , status, Response
from enum import Enum

app = FastAPI()

@app.get('/hello')
def index():
    return {'message':'Hello World!'}

# @app.get('/blog/all')
# def get_all_blog():
#     return {'message':'all blog bla bla'}


@app.get('/blog/all', tags=['blog'])
def get_allblogs(page, page_size: Optional[int] = None):
    return {'message': f'All {page_size} blogs on page {page}'}

@app.get('/blog/{id}/comments/{comment_id}', tags=['blog', 'comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {'message': f'ID: {id}, comment_id: {comment_id}, validation: {valid}, Username: {username}'}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get('/blog/type/{type}', tags=['blog'])
def get_blog_type(type: BlogType):
    return{'message': f'Blog Type {type}'}


@app.get('/blog/{id}', status_code= status.HTTP_200_OK, tags=['blog'])
def get_blog(id: int, response: Response):
    if id>5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{'error':f'blog {id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'message':f'{id} is found'}
    