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


@app.post('/profile', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
async def homepage(request:Request):
    validation = "name"
    forms = await request.form()
    forms = dict(forms)
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
    if validation in forms.keys():
        try:
            sql_query_patient_lenght = "SELECT * FROM main_patientprofile" 

            sql_query_many_to_many_relation = '''INSERT INTO main_doctor_patient(
                                    id,
                                    doctor_id,
                                    patientprofile_id)
                                    VALUES (%s, %s, %s)    
                                '''

            sql_query_patient = '''INSERT INTO main_patientprofile(
                        ID,
                        name, 
                        last_name,
                        age,
                        description,
                        email)
                        VALUES (%s, %s, %s, %s, %s, %s)    
                    '''
            
            name, lastname, age = forms['name'], forms['lastname'], forms['age']
            description, email = forms['description'], forms['email']
            ID = 16
            values_patient = tuple([ID, name, lastname, age, description, email])
            cur.execute(sql_query_patient, values_patient)

            doctor_id = request.session['doctor']
            values_many_to_many = tuple([ID+1, doctor_id, ID])
            cur.execute(sql_query_many_to_many_relation, values_many_to_many)

        except Exception as e:
            pass

    return templates.TemplateResponse('home.html', 
                                    {'request':request,
                                    'data':1})



@app.get('/login', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def Login(request:Request):
    return templates.TemplateResponse('login.html', 
                            {'request':request, 
                            'data':None})


@app.post('/login', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
async def Logined(request:Request):
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
    print(f"this is a form's of data {form}")
    name = form["doctor"]
    password = form['password']
    # index 1 show tha name of doctor and index -1 or 3 show password
    # we must check the password id correct or not
    sql_query = "SELECT * FROM main_doctor"
    cur.execute(sql_query)
    for doctor_row in cur.fetchall():
        print(doctor_row)
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
