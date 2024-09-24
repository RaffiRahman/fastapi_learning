from fastapi import FastAPI, Request 
from exceptions import StoryException
from router import blog_get, blog_post, user, article, product, file
from auth import authentication
from templates import templates
from db import models
from db.database import engine
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.get('/hello')
def index():
    return {'message':'Hello World!'}

# @app.exception_handler(StoryException)
# def story_exception_handler(request: Request, exc: StoryException):
#     return JSONResponse(
#         status_code= 418,
#         content= {'detail': exc.name}
#     )

models.Base.metadata.create_all(engine)

app.mount('/files', StaticFiles(directory= "files"), name='files')
app.mount('/static', 
        StaticFiles(directory="templates/static"),
        name="static"
    )