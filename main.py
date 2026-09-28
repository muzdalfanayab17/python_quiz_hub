from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware  # <-- Session ke liye import kiya
from sqlalchemy import create_engine,Column ,Integer,String,MetaData,Table
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL = "postgresql://postgres:PRINT@localhost:5432/quiz_hub"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
#user table here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    gender = Column(String)
Base.metadata.create_all(bind=engine)
app = FastAPI()

# <-- Session Middleware add kiya (Isse session work karega)
app.add_middleware(SessionMiddleware, secret_key="my_secret_key_for_python_quiz_hub")

users = []
scores=[]
templates = Jinja2Templates(directory="templates")
#static files ky liey
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )
@app.get('/login', response_class=HTMLResponse)
def login(request: Request):
    error = request.query_params.get('error')

    return templates.TemplateResponse(
        name='login.html',
        request=request,
        context={
            'request': request,
            'error': error
        }
    )

@app.get('/register', response_class=HTMLResponse)
def register(request: Request):
    error = request.query_params.get('error')

    return templates.TemplateResponse(
        name='register.html',
        request=request,
        context={
            'request': request,
            'error': error
        }
    )
@app.post('/register')
def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    gender: str = Form(...)
):

    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        db.close()
        return RedirectResponse(
            url='/register?error=Email already registered',
            status_code=303
        )

    new_user = User(
        name=name,
        email=email,
        password=password,
        gender=gender
    )

    db.add(new_user)
    db.commit()
    db.close()

    request.session['user_email'] = email
    request.session['user_name'] = name

    print(new_user)

    return RedirectResponse(url='/dashboard', status_code=303)
@app.post('/login')
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if user and user.password == password:

        request.session['user_email'] = user.email
        request.session['user_name'] = user.name

        db.close()

        return RedirectResponse(
            url='/dashboard',
            status_code=303
        )

    db.close()

    return RedirectResponse(
        url='/login?error=Invalid email or password',
        status_code=303
    )
@app.get('/logout')
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(url='/login', status_code=303)


@app.get('/dashboard', response_class=HTMLResponse)
def dashboard(request: Request):

    user_email = request.session.get('user_email')

    return templates.TemplateResponse(
        name='dashboard.html',
        request=request,
        context={
            'request': request,
            'email': user_email
        }
    )

@app.get('/quiz_category', response_class=HTMLResponse)
def quiz_category(request: Request):
    return templates.TemplateResponse(
        name='quiz_category.html',
        request=request,
        context={'request': request}
    )

@app.get('/view', response_class=HTMLResponse)
def view(request: Request):

    user_email = request.session.get('user_email')

    user_scores = []

    for i in scores:
        if i['email'] == user_email:
            user_scores.append(i)

    return templates.TemplateResponse(
        name='view.html',
        request=request,
        context={
            'request': request,
            'scores': user_scores
        }
        
    )
@app.get('/profile', response_class=HTMLResponse)
def profile(request: Request):
    user_email = request.session.get('user_email')
    user_name = request.session.get('user_name')

    return templates.TemplateResponse(
        name='profile.html',
        request=request,
        context={
            'request': request,
            'email': user_email,
            'name': user_name
        }
    )
@app.post('/profile')
def update_profile(
    request: Request,
    new_name: str = Form(...),
    new_email: str = Form(...)
):
    old_email = request.session.get('user_email')

    for i in users:
        if i['email'] == old_email:
            i['name'] = new_name
            i['email'] = new_email

            request.session['user_name'] = new_name
            request.session['user_email'] = new_email

            break

    return RedirectResponse(url='/profile', status_code=303)   

@app.get('/basic', response_class=HTMLResponse)
def basic(request: Request):
    return templates.TemplateResponse(
        name='basic.html',
        request=request,
        context={'request': request}
    )
@app.post('/basic')
def basic(request: Request, 
    q1: str = Form(...), q2: str = Form(...), q3: str = Form(...), q4: str = Form(...), q5: str = Form(...), 
    q6: str = Form(...), q7: str = Form(...), q8: str = Form(...), q9: str = Form(...), q10: str = Form(...)): 
    
    score = 0
    message = ''
     
    user_answers = { 
        'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 
        'q6': q6, 'q7': q7, 'q8': q8, 'q9': q9, 'q10': q10 
    } 
     
    correct_answers = { 
        "q1": "B", "q2": "B", "q3": "C", "q4": "B", "q5": "C", 
        "q6": "C", "q7": "C", "q8": "B", "q9": "B", "q10": "A" 
    } 
 
    for value in user_answers:
        if user_answers[value] == correct_answers[value]:
            score += 1
             
    if 9 <= score <= 10:
        message = "Excellent 🎉"
    elif 7 <= score <= 8:
        message = 'good 👍'
    elif 5 <= score <= 6:
        message = ' average👍'
    else:
        message = 'needs practise'

    scores.append({
        'email': request.session.get('user_email'),
        'quiz': 'basic',
        'score': score,
        'message': message
    })
    
         
    return RedirectResponse(
        url=f'/result?score={score}&message={message}&quiz=basic',
        status_code=303
    )
# <-- Naya /result endpoint jo score aur message templates par show karwaye ga
@app.get('/result', response_class=HTMLResponse)
def result(request: Request, score: int, message: str, quiz: str):
    return templates.TemplateResponse(
        name='result.html',
        request=request,
        context={
            'request': request,
            'score': score,
            'message': message,
            'quiz': quiz
        }
    )


@app.get('/variable',response_class=HTMLResponse)
def variable(request:Request):
    return templates.TemplateResponse(
        name='variable.html',
        request=request,
        context={
           'request':request
        }
    )
@app.post('/variable')
def variable(request : Request,
    q1: str = Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4: str = Form(...),
    q5: str = Form(...),
    q6: str = Form(...),
    q7: str = Form(...),
    q8: str = Form(...),
    q9: str = Form(...),
    q10: str = Form(...)):
    score=0
    message=''
    user_answers = {
        'q1':q1,
        'q2':q2,
        'q3':q3,
        'q4':q4,
        'q5':q5,
        'q6':q6,
        'q7':q7,
        'q8':q8,
        'q9':q9,
        'q10':q10
    }
    correct_answers = {
    "q1": "C",   # student_name
    "q2": "C",   # int
    "q3": "B",   # 25
    "q4": "C",   # str()
    "q5": "C",   # type()
    "q6": "A",   # Ali
    "q7": "C",   # float
    "q8": "A",   # x = y = 10
    "q9": "A",   # bool
    "q10": "B"  # status = True
   }
    for i in user_answers:
      if user_answers[i] == correct_answers[i]:
        score += 1

    if 9 <= score <= 10:
      message = "Excellent 🎉"
    elif 7 <= score <= 8:
       message = "Good 👍"
    elif 5 <= score <= 6:
       message = "Average 👍"
    else:
       message = "Needs Practice 📚"
    scores.append({
    'email': request.session.get('user_email'),
    'quiz': 'variable',
    'score': score,
    'message': message
})
    return RedirectResponse(url=f'/result?score={score}&message={message}&quiz=variable',status_code=303)

@app.get('/result', response_class=HTMLResponse)
def result(request: Request, score: int, message: str):
    return templates.TemplateResponse(
        request=request,
        name='result.html',
        context={
            'request': request,
            'score': score,
            'message': message
        }
    )

@app.get('/function',response_class=HTMLResponse)
def function(request:Request):
    return templates.TemplateResponse(
        name='function.html',
        request=request,
        context={
            'request':request
        }
    )
@app.post('/function')
def function (request: Request,
    q1: str = Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4: str = Form(...),
    q5: str = Form(...),
    q6: str = Form(...),
    q7: str = Form(...),
    q8: str = Form(...),
    q9: str = Form(...),
    q10: str = Form(...)):
    score=0
    message=''
    user_answers=[{'q1':q1},
                  {'q2':q2},
                  {'q3':q3},
                  {'q4':q4},
                  {'q5':q5},
                  {'q6':q6},
                  {'q7':q7},
                  {'q8':q8},
                  {'q9':q9},
                  {'q10':q10}]
    correct_answers = [
    {"q1": "C"},
    {"q2": "B"},
    {"q3": "C"},
    {"q4": "C"},
    {"q5": "C"},
    {"q6": "C"},
    {"q7": "C"},
    {"q8": "A"},
    {"q9": "B"},
    {"q10": "B"}
   ]
    for i in range(len(user_answers)):
        user=user_answers[i]
        correct=correct_answers[i]
        for key in user:
            if(user[key]==correct[key]):
                score+=1
    if 9 <= score <= 10:
      message = "Excellent 🎉"
    elif 7 <= score <= 8:
       message = "Good 👍"
    elif 5 <= score <= 6:
       message = "Average 👍"
    else:
       message = "Needs Practice 📚"
    scores.append({
    'email': request.session.get('user_email'),
    'quiz': 'function',
    'score': score,
    'message': message
})
    return RedirectResponse(
    url=f'/result?score={score}&message={message}&quiz=function',
    status_code=303
)
@app.get('/exception', response_class=HTMLResponse)
def exception(request: Request):
    return templates.TemplateResponse(
        name='exception.html',
        request=request,
        context={
            'request': request
        }
    )
@app.post('/exception')
def exception(request:Request,
    q1: str = Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4:str = Form(...),
    q5:str = Form(...),
    q6:str = Form(...),
    q7:str = Form(...),
    q8:str = Form(...),
    q9:str = Form(...),
    q10:str = Form(...)):
    score=0
    message=''
    user_answers=[{'q1':q1},
                  {'q2':q2},
                  {'q3':q3},
                  {'q4':q4},
                  {'q5':q5},
                  {'q6':q6},
                  {'q7':q7},
                  {'q8':q8},
                  {'q9':q9},
                  {'q10':q10}]
    correct_answers = [
    {"q1": "B"},
    {"q2": "A"},
    {"q3": "C"},
    {"q4": "C"},
    {"q5": "B"},
    {"q6": "B"},
    {"q7": "B"},
    {"q8": "B"},
    {"q9": "B"},
    {"q10": "A"}
   ]
    for i in range(len(user_answers)):
        user=user_answers[i]
        correct=correct_answers[i]
        for value in user:
            if(user[value]==correct[value]):
                score+=1

    if 9 <= score <= 10:
      message = "Excellent 🎉"
    elif 7 <= score <= 8:
       message = "Good 👍"
    elif 5 <= score <= 6:
       message = "Average 👍"
    else:
       message = "Needs Practice 📚"
    scores.append({
    'email': request.session.get('user_email'),
    'quiz': 'exception',
    'score': score,
    'message': message
})
    return RedirectResponse(url=f'/result?score={score}&message={message}&quiz=exception',status_code=303)
@app.get('/file',response_class=HTMLResponse)
def file(request:Request):
    return templates.TemplateResponse(
        name='file.html',
        request=request,
        context={
            'request':request
        }
    )
@app.post('/file')
def file(request:Request,q1:str=Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4:str = Form(...),
    q5:str = Form(...),
    q6:str = Form(...),
    q7:str = Form(...),
    q8:str = Form(...),
    q9:str = Form(...),
    q10:str = Form(...)):
    score=0
    message=''
    user_answers=[{'q1':q1},
                  {'q2':q2},
                  {'q3':q3},
                  {'q4':q4},
                  {'q5':q5},
                  {'q6':q6},
                  {'q7':q7},
                  {'q8':q8},
                  {'q9':q9},
                  {'q10':q10}]

    correct_answers = [
    {"q1": "A"},
    {"q2": "B"},
    {"q3": "A"},
    {"q4": "C"},
    {"q5": "B"},
    {"q6": "B"},
    {"q7": "C"},
    {"q8": "A"},
    {"q9": "C"},
    {"q10": "D"}
    ]
    for i in user_answers:
        
        index = user_answers.index(i)
        correct = correct_answers[index]

        for key in i:
           if i[key] == correct[key]:
              score += 1
        
    if 9 <= score <= 10:
        message = "Excellent 🎉"
    elif 7 <= score <= 8:
        message = "Good 👍"
    elif 5 <= score <= 6:
        message = "Average 👍"
    else:
        message = "Needs Practice 📚"
    
    scores.append({
    'email': request.session.get('user_email'),
    'quiz': 'file',
    'score': score,
    'message': message
})
    return RedirectResponse(url=f'/result?score={score}&message={message}&quiz=file',
    status_code=303
)

    
@app.get('/advance',response_class=HTMLResponse)
def advance(request:Request):
    return templates.TemplateResponse(
        name='advance.html',
        request=request,
        context={
            'request':request
        }
    )
@app.post('/advance')
def advance(
    request: Request,
    q1: str = Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4: str = Form(...),
    q5: str = Form(...),
    q6: str = Form(...),
    q7: str = Form(...),
    q8: str = Form(...),
    q9: str = Form(...),
    q10: str = Form(...)
):
    score=0
    message=''
    user_answers=[{'q1':q1},
                  {'q2':q2},
                  {'q3':q3},
                  {'q4':q4},
                  {'q5':q5},
                  {'q6':q6},
                  {'q7':q7},
                  {'q8':q8},
                  {'q9':q9},
                  {'q10':q10}]

    correct_answers = [
    {"q1": "B"},
    {"q2": "B"},
    {"q3": "B"},
    {"q4": "B"},
    {"q5": "A"},
    {"q6": "B"},
    {"q7": "B"},
    {"q8": "B"},
    {"q9": "B"},
    {"q10": "C"}
]
    for i in range(len(user_answers)):
        user=user_answers[i]
        correct= correct_answers[i]
        for key in user:
            if ( user[key] == correct[key] ):
              score+=1
    if 9 <= score <= 10:
        message = "Excellent 🎉"
    elif 7 <= score <= 8:
        message = "Good 👍"
    elif 5 <= score <= 6:
        message = "Average 👍"
    else:
         message = "Needs Practice 📚"
    scores.append({
    'email': request.session.get('user_email'),
    'quiz': 'Advance',
    'score': score,
    'message': message
})
    return RedirectResponse(
    url=f'/result?score={score}&message={message}&quiz=advance',
    status_code=303
)












