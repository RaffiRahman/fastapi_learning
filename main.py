from os import name
from fastapi import FastAPI, Request 
from exceptions import StoryException
from router import blog_get, blog_post, user, article, product, file, dependencies
from auth import authentication
from templates import templates
from db import models
from db.database import engine
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import time
from client import html
from fastapi.websockets import WebSocket

app = FastAPI()
app.include_router(dependencies.router)
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

@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def websockets_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)

models.Base.metadata.create_all(engine)

@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response

app.mount('/files', StaticFiles(directory= "files"), name='files')
app.mount('/static', 
        StaticFiles(directory="templates/static"),
        name="static"
    )