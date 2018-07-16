from flask import Flask, render_template, flash, redirect, url_for, request, g, session
import datetime as dt
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

#Set config variables:
assert "APP_SETTINGS" in os.environ, "APP_SETTINGS environment variable not set"
assert "SECRET_KEY" in os.environ, "SECRET_KEY environment variable not set"
assert "ADMIN_PWD" in os.environ, "ADMIN_PWD environment variable not set"
assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable not set"
app.config.from_object(os.environ['APP_SETTINGS'])

#Configure postgresql database:
db = SQLAlchemy(app)
from models import Partners, Work_Packages, Deliverables #, Tasks, Tasks2Deliverables, Partners2Tasks

########## PSQL FUNCTIONS ##########
def psql_to_pandas(query):
    df = pd.read_sql(query.statement,db.session.bind)
    return df

def psql_insert(row):
    db.session.add(row)
    db.session.commit()
    return

def psql_delete(row):
    db.session.delete(row)
    db.session.commit()
    return
####################################

########## LOGGED-IN FUNCTIONS ##########
#Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, please login', 'danger')
            return redirect(url_for('index'))
    return wrap
#########################################

#Index
@app.route('/')
def index():
    return render_template('home.html')

#Add partner
@app.route('/add-partner', methods=["GET","POST"])
def add_partner():
    if request.method == 'POST':
        #Get form fields
        name = request.form['name']
        country = request.form['country']
        role = request.form['role']
        #Add to DB:
        max_id = Partners.query.order_by(Partners.partner_id.desc()).first().partner_id
        db_row = Partners(partner_id=max_id+1,name=name,country=country,role=role)
        psql_insert(db_row)
        #Return with success
        flash('Added to database', 'success')
        return redirect(url_for('add_partner'))
    return render_template('add-partner.html')

#View partner
@app.route('/view-partners')
def view_partners():
    partnersData = psql_to_pandas(Partners.query)
    return render_template('view-partners.html',partnersData=partnersData)

#Login
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        session['logged_in'] = True
        flash('You are now logged in', 'success')
        return redirect(url_for('index'))
    return render_template('login.html')

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
