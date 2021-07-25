from flask import request, render_template, url_for, flash, redirect, Markup
from sqlalchemy import or_
from interface.models import state, user, ban, input, insult
from interface.forms import InsultForm
from interface import app, db
import datetime

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/states', methods = ['GET', 'POST'])
def states():
    states = state.query.all()
    return render_template('states.html', states = states)

@app.route('/users', methods = ['GET', 'POST'])
def users():
    users = user.query.all()
    return render_template('users.html', users = users) 

@app.route('/bans', methods = ['GET', 'POST'])
def bans():
    bans = db.session.query(ban, user).join(user, ban.USER_ID == user.USER_ID).all()
    return render_template('bans.html', bans = bans)  

@app.route('/insults', methods = ['GET', 'POST'])
def insults():
    insults = insult.query.all()
    return render_template('insults.html', insults = insults)  

@app.route('/<id>', methods = ['GET', 'POST'])
def insult_edit(id):

    form = InsultForm()

    insult_id = insult.query.filter(insult.INSULT_ID == id).first()
    if request.method == 'POST' and form.validate_on_submit():
        insult_id.INSULT_TEXT = request.form['INSULT_TEXT']
        insult_id.INSULT_FILE = request.form['INSULT_FILE']
        insult_id.USER_REFERENCED = request.form['USER_REFERENCED']
        insult_id.ACTIVE = request.form.get('ACTIVE', 0)
        insult_id.INDEFINITE_BAN = request.form.get('INDEFINITE_BAN', 0)
        insult_id.UPDATE_DATE = datetime.datetime.now()
        db.session.commit()
        return redirect(url_for('insults'))  

    return render_template('insult.html', insult = insult_id, form = form) 

@app.route('/new', methods = ['GET', 'POST'])
def new():
    form = InsultForm()
    if request.method == 'POST' and form.validate_on_submit():
        record = insult(
                        INSULT_TEXT = request.form['INSULT_TEXT'],
                        INSULT_FILE = request.form['INSULT_FILE'],
                        USER_REFERENCED = request.form['USER_REFERENCED'],
                        ACTIVE = request.form.get('ACTIVE', 0),
                        INDEFINITE_BAN = request.form.get('INDEFINITE_BAN', 0),
                        CREATE_DATE = datetime.datetime.now(),
                        UPDATE_DATE = datetime.datetime.now())
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('insults'))  

    return render_template('new.html', form = form) 

@app.route('/inputs', methods = ['GET', 'POST'])
def inputs():
    inputs = db.session.query(input, user).join(user, input.USER_ID == user.USER_ID).order_by(input.INPUT_ID.desc()).limit(50)
    return render_template('inputs.html', inputs = inputs) 
