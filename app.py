from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret secret'

toolbar = DebugToolbarExtension(app)

survey = satisfaction_survey

answers=[]
@app.route('/')
def home():
    return render_template('home.html',title=survey.title, instructions=survey.instructions)

@app.route('/survey/question/<int:num>')
def survey_display(num):
    """displays the next question in the survey"""
    question=survey.questions
    last=False

    if len(answers) == len(survey.questions):
        flash('You are trying to access an invalid url','warning')
        return redirect('/landing')

    if num != len(answers):
        flash('You are trying to access an invalid url','warning')
        return redirect(f'/survey/question/{len(answers)}')

    
    if question[num] == question[-1]:
        last = True


    return render_template('survey.html', question=question[num], last=last, num=num)

@app.route('/answer', methods=['POST'])
def add_answer():
    """Handles form data from the survey and appends to answers variable"""
    answer = request.form.get('answer')
    num = request.form.get('next')
    last = request.form.get('last')
    answers.append(answer)
    if last == 'True':
        return redirect('/landing')
    else:
        return redirect(f'/survey/question/{num}')

@app.route('/landing')
def landing():
    return render_template('landing.html')

