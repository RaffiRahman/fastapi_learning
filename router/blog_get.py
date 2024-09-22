from router.blog_post import required_functionality
from typing import Optional
from fastapi import APIRouter, status, Response, Depends, Query
from enum import Enum

router = APIRouter(
    prefix= '/blog',
    tags=['blog']
)

# @router.get('/blog/all')
# def get_all_blog():
#     return {'message':'all blog bla bla'}

@router.get('/all')
def get_allblogs(page: int = Query(..., description="Page number"), page_size: Optional[int] = Query(10, description="Page size"), req_parameter: dict = Depends(required_functionality)):
    return {'message': f'All {page_size} blogs on page {page}', 'req': req_parameter}

@router.get('/{id}/comments/{comment_id}', tags=['comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {'message': f'ID: {id}, comment_id: {comment_id}, validation: {valid}, Username: {username}'}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('/type/{type}')
def get_blog_type(type: BlogType):
    return{'message': f'Blog Type {type}'}


@router.get('/{id}', status_code= status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id>5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{'error':f'blog {id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'message':f'{id} is found'}
    