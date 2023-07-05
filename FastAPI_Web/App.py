from fastapi import FastAPI, status, Request, HTTPException 
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn 
import psycopg2 as pg 

from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


# add request.session
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    session = request.cookies.get('session')
    if session:
        response.set_cookie(key='session', 
                            value=request.cookies.get('session'), 
                            httponly=True)
    return response


@app.get('/', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def homepage(request:Request):
    return templates.TemplateResponse('home.html', 
                            {'request':request, 
                            'data':None})


@app.post('/', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
async def homepage(request:Request):
    if request.session['doctor'] is not None:
        conn = pg.connect(
                    host='localhost',
                    port=5432,
                    dbname='postgres',
                    password='postgres',
                    user='postgres'
                )
        print("Connected succesfully...")

        sql_query = '''INSERT INTO main_patientprofile(
                    ID,
                    name, 
                    last_name,
                    age,
                    description,
                    email)
                    VALUES (%s, %s, %s, %s, %s, %s)    
                '''


@app.get('/login', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def Login(request:Request):
    return templates.TemplateResponse('login.html', 
                            {'request':request, 
                            'data':None})


@app.post('/login', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
async def Login(request:Request):
    conn = pg.connect(
        host='localhost',
        port=5432,
        dbname='postgres',
        password='postgres',
        user='postgres'
    )
    print("Connected succesfully...")

    conn.autocommit = True 
    cur = conn.cursor()

    form = await request.form()
    form = dict(form)
    print(form)
    name = form["doctor"]
    password = form['password']
    # index 1 show tha name of doctor and index -1 or 3 show password
    # we must check the password id correct or not
    sql_query = "SELECT * FROM main_doctor"
    cur.execute(sql_query)
    for doctor_row in cur.fetchall():
        if doctor_row[1]==name and doctor_row[-1]==password:
            request.session['doctor'] = doctor_row[0] # that's ID of doctor
            return templates.TemplateResponse('home.html', 
                            {'request':request, 
                            'data':doctor_row[1]})
        else:
            return templates.TemplateResponse('login.html', 
                            {'request':request, 
                            'data':"Invalid Profile!!!"})
    

@app.get('/logout', response_class=HTMLResponse)
async def Logout(request:Request):
    request.session['doctor'] = None 
    return RedirectResponse(url='/')


@app.get('/signup', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
async def Login(request:Request):
    return templates.TemplateResponse('signup.html', 
                            {'request':request, 
                            'data':None})



if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=2728)
