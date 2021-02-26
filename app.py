from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.debug =  True
app.config['SECRET_KEY'] = 'secret secret'

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    return render_template('home.html', surveys=surveys)

@app.route('/survey/question/<int:num>')
def survey_display(num):
    """displays the next question in the survey"""
    survey= surveys[session.get('survey')]
    question=survey.questions
    answers = session['answers']
    last=False
    prev = True if str(num) in session['answers'] else False

    if question[num] == question[-1]:
        last = True


    return render_template('survey.html', question=question[num], last=last, num=num, prev=prev)

@app.route('/answer', methods=['POST'])
def add_answer():
    """Handles form data from the survey and appends to answers variable"""
    answer = request.form.get('answer')
    num = request.form.get('next')
    last = request.form.get('last')
    comment= request.form.get('comment')
    location = request.form.get('location')
    #getting and updateing the answer session variable
    answers= session['answers']
    answers[f'{int(num)-1}']= answer
    session['answers'] = answers

# check which direction the user wants to go
    if location == 'prev':
        prev = int(num)-2
        if prev<0:
            return redirect('/')
        return redirect(f'/survey/question/{int(num)-2}')
# check and add comments to session variable
    if comment:
        comments = session['comments']
        comments[int(num)-1]=comment
    if last == 'True':
        return redirect('/landing')
    else:
        return redirect(f'/survey/question/{num}')

@app.route('/initialize', methods=['POST'])
def session_start():
    """Initializes the survey by setting survey, question variables in session to be tracked"""
    if session.get('completed'):
        if request.form.get('survey_code') in session['completed']:
            flash('You have already completed this survey!', category = 'warning')
            return redirect('/')

    session.permanent = True
    session['completed']=[]
    session['answers']={}
    session['survey']= request.form.get('survey_code')
    session['comments']={}
    print(session['answers'])
    return redirect('/survey/question/0')

@app.route('/landing')
def landing():
    """set up the landing page to display questions, answers, and comments"""
    survey= surveys[session.get('survey')]
    questions=survey.questions
    completed = session['completed']
    completed.append(session.get('survey'))
    comments= session.get('comments')
    answers=session.get('answers')
    final=[]
    for i in range(len(questions)):
        if str(i) in comments:
            final.append([questions[i],answers[str(i)],comments[str(i)]])
        else:
            final.append([questions[i],answers[str(i)],False])

    return render_template('landing.html', questions=final)

