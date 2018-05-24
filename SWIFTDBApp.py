from flask import Flask, render_template, flash, redirect, url_for, request, g
from wtforms import Form, DecimalField, TextAreaField, RadioField, SelectField, validators
from wtforms.fields.html5 import DateField
import datetime as dt
import sqlite3
import os
import pandas as pd

app = Flask(__name__)
assert os.path.exists('AppSecretKey.txt'), "Unable to locate app secret key"
with open('AppSecretKey.txt','r') as f:
    key=f.read()
app.secret_key=key
DATABASE = 'SWIFTDB.db'
assert os.path.exists(DATABASE), "Unable to locate database"

#Set subdomain...
#If running locally (or index is the domain) set to blank, i.e. subd=""
#If index is a subdomain, set as appropriate *including* leading slash, e.g. subd="/SWIFTDB"
#Routes in @app.route() should NOT include subd, but all other references should...
#Use redirect(subd + '/route') rather than redirect(url_for(route))
#Pass subd=subd into every render_template so that it can be used to set the links appropriately
#
subd=""

#Connect to DB
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

#Close DB if app stops
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Query DB
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else (rv if rv else None)

#Query DB pandas
def pandas_db(query):
    db = get_db()
    df = pd.read_sql_query(query,db)
    db.close()
    return df

#Index
@app.route('/')
def index():
    return render_template('home.html',subd=subd)

#Login
@app.route('/login')
def login():
    return render_template('login.html',subd=subd)

if __name__ == '__main__':
    app.run(debug=True)
