from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware  # <-- Session ke liye import kiya

app = FastAPI()

# <-- Session Middleware add kiya (Isse session work karega)
app.add_middleware(SessionMiddleware, secret_key="my_secret_key_for_python_quiz_hub")

users = []
ctemplates = Jinja2Templates(directory="templates")
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
    return templates.TemplateResponse(
        request=request,
        name='login.html',
        context={
            'request': request
        }
    )

@app.get('/register', response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='register.html',
        context={
           'request': request
        }
    )

@app.post('/register')
def register(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), gender: str = Form(...)):
    user = {
        'name': name,
        'email': email,
        'password': password,
        'gender': gender
    }
    users.append(user)
    
    # <-- Registration ke baad user email session mein save kiya
    request.session['user_email'] = email
    
    print(user)
    return RedirectResponse(url='/dashboard', status_code=303)

@app.post('/login')
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    for i in users:
        if i["email"] == email and i["password"] == password:
            # <-- Successful login par user email session mein save kiya
            request.session['user_email'] = email
            return RedirectResponse(url='/dashboard', status_code=303)

    return RedirectResponse(url='/dashboard', status_code=303)

@app.get('/dashboard', response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        name='dashboard.html',
        request=request,
        context={
            'request': request,
        }
    )

@app.get('/quiz_category', response_class=HTMLResponse)
def quiz_category(request: Request):
    return templates.TemplateResponse(
        name='quiz_category.html',
        request=request,
        context={'request': request}
    )

@app.get('/profile', response_class=HTMLResponse)
def profile(request: Request):
    return templates.TemplateResponse(
        name='profile.html',
        request=request,
        context={'request': request}
    )

@app.get('/view', response_class=HTMLResponse)
def view(request: Request):
    return templates.TemplateResponse(
        name='view.html',
        request=request,
        context={'request': request}
    )

@app.get('/basic', response_class=HTMLResponse)
def basic(request: Request):
    return templates.TemplateResponse(
        name='basic.html',
        request=request,
        context={
            'request': request
        }
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
        
    return RedirectResponse(url=f'/result?score={score}&message={message}', status_code=303)

# <-- Naya /result endpoint jo score aur message templates par show karwaye ga
@app.get('/result', response_class=HTMLResponse)
def result(request: Request, score: int, message: str):
    return templates.TemplateResponse(
        name='view.html',  # Aap apni marzi ke template ka naam de sakti hain (e.g., result.html ya view.html)
        request=request,
        context={
            'request': request,
            'score': score,
            'message': message
        }
    )

@app.get('/result',response_class=HTMLResponse)
def result(request:Request,score:int,message:str):
    return templates.TemplateResponse(request=request,
                                      name='result.html',
                                      context={
                                          'request':request,
                                          'message':message,
                                          'score':score

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
def variable(request: Request,
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

    return RedirectResponse(url=f'/result?score={score}&message={message}',status_code=303)

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
def funtion (request: Request,
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

    return RedirectResponse(url=f'/result?score{score}& message={message}',status_code=303)
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

    return RedirectResponse(url=f'/result?score={score}&message={message}',status_code=303)
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
def post(request:Request,q1:str=Form(...),
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
    return RedirectResponse()

    
@app.get('/advance',response_class=HTMLResponse)
def file(request:Request):
    return templates.TemplateResponse(
        name='advance.html',
        request=request,
        context={
            'request':request
        }
    )
    q3: str = Form(...),
    q4:str = Form(...),
    q5:str = Form(...),
    q6:str = Form(...),
    q7:str = Form(...),
    q8:str = Form(...),
    q9:str = Form(...),
    q10:str = Form(...),
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
    {"q1": "B"},   # y = x, isliye list change hoti hai
    {"q2": "B"},   # 10 + 5 = 15
    {"q3": "B"},   # 5 * 5 = 25
    {"q4": "B"},   # map se har number * 2
    {"q5": "A"},   # inner function outer ka x access karti hai
    {"q6": "B"},   # finally ka return override karta hai
    {"q7": "A"},   # next() pehle 1, phir 2 deta hai
    {"q8": "A"},   # decorator function ka behavior modify/extend kar sakta hai
    {"q9": "B"},   # local x = 20, global x = 10
    {"q10": "B"}   # even numbers [2, 4]
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

    return RedirectResponse(url=f'/result?score{score}& message={message}',status_code=303)












