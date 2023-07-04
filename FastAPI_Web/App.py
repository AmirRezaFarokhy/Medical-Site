from fastapi import FastAPI, status, Request 
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn 
import psycopg2 as pg 

from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), 
          name='static')
templates = Jinja2Templates(directory='templates')

# add request.session
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    session = request.cookies.get('session')
    if session:
        response.set_cookie(key='session', value=request.cookies.get('session'), httponly=True)
    return response


@app.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def homepage(request:Request):
    message = {'warning':'You are becomming a web developer.'}
    return templates.TemplateResponse('home.html', {'request':request, 'data':message})



if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=2728)
