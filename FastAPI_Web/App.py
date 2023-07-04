from fastapi import FastAPI, status, Request 
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
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
    try:
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

    except Exception as e:
        print(f"Can't Connect for {e}")


    return templates.TemplateResponse('home.html', 
                                {'request':request, 
                                'data':None})


@app.get('/login', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
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
    
    # name = request.POST.get('doctor')
    # password = request.POST.get('password')
    # # index 1 show tha name of doctor and index -1 or 3 show password
    # # we must check the password id correct or not
    # sql_query = "SELECT * FROM main_doctor"
    # cur.execute(sql_query)
    # for doctor_row in cur.fetchall():
    #     if doctor_row[1]==name and doctor_row[-1]==password:
    #         request.session['doctro'] = doctor_row[0] # that's ID of doctor
    #         # return RedirectResponse('home.html')

    return templates.TemplateResponse('login.html', 
                            {'request':request, 
                            'data':None})


@app.get('/signup', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
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
    
    # name = request.POST.get('doctor')
    # password = request.POST.get('password')
    # # index 1 show tha name of doctor and index -1 or 3 show password
    # # we must check the password id correct or not
    # sql_query = "SELECT * FROM main_doctor"
    # cur.execute(sql_query)
    # for doctor_row in cur.fetchall():
    #     if doctor_row[1]==name and doctor_row[-1]==password:
    #         request.session['doctro'] = doctor_row[0] # that's ID of doctor
    #         # return RedirectResponse('home.html')

    return templates.TemplateResponse('signup.html', 
                            {'request':request, 
                            'data':None})



if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=2728)
