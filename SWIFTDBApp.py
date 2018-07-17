from flask import Flask, render_template, flash, redirect, url_for, request, g, session, abort
from wtforms import Form, validators, StringField, SelectField, TextAreaField, IntegerField
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

########## MISC FUNCTIONS ##########
def table_list(tableClass,col):
    DF = psql_to_pandas(eval(tableClass).query.order_by(eval(tableClass).id))
    list = [('blank','--Please select--')]
    for element in DF[col]:
        list.append((element,element))
    return list
#########################################

########## FORM CLASSES ##########
class Partners_Form(Form):
    name = StringField(u'*Partner Name',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. Leeds"})
    country = StringField(u'Country',
        render_kw={"placeholder": "e.g. UK"})
    role = StringField(u'Role',
        render_kw={"placeholder": "e.g. 'Academic' or 'Operational'"})

class Work_Packages_Form(Form):
    code = StringField(u'*Work Package Code',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. WP-C1"})
    name = StringField(u'*Name',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. Training"})

class Deliverables_Form(Form):
    code = StringField(u'*Deliverable Code',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. D-R1.1"})
    work_package = SelectField(u'*Work Package',
        [validators.NoneOf(('blank'),message='Please select')])
    description = TextAreaField(u'*Description',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. Report on current state \
of knowledge regarding user needs for forecasts at \
different timescales in each sector."})
    responsible_partner = SelectField(u'*Responsible Partner',
        [validators.NoneOf(('blank'),message='Please select')])
    month_due = IntegerField(u'Month Due',
        validators=[validators.Optional()])
    progress = TextAreaField(u'Progress',
        validators=[validators.Optional()])
    percent = IntegerField(u'*Percentage Complete',
        [validators.NumberRange(min=0,max=100,message="Must be between 0 and 100")])
#########################################

#Index
@app.route('/')
def index():
    return render_template('home.html')

#Add entry
@app.route('/add/<string:tableClass>', methods=["GET","POST"])
def add(tableClass):
    form = eval(tableClass+"_Form")(request.form)
    #Set title and tweak form
    if tableClass=='Partners':
        title = "Add Partner"
    elif tableClass=='Work_Packages':
        title = "Add Work Package"
    elif tableClass=='Deliverables':
        title = "Add Deliverable"
        form.work_package.choices = table_list('Work_Packages','code')
        form.responsible_partner.choices = table_list('Partners','name')
    if request.method == 'POST' and form.validate():
        #Get form fields:
        formdata=[]
        for field in form:
            formdata.append(field.data)
        #Add to DB:
        if tableClass=='Partners':
            db_row = Partners(name=formdata[0],country=formdata[1],role=formdata[2])
        elif tableClass=='Work_Packages':
            db_row = Work_Packages(code=formdata[0],name=formdata[1])
        elif tableClass=='Deliverables':
            db_row = db_row = Deliverables(code=formdata[0],work_package=formdata[1],
              description=formdata[2],responsible_partner=formdata[3],
              month_due=formdata[4],progress=formdata[5],percent=formdata[6])
        psql_insert(db_row)
        #Return with success
        flash('Added to database', 'success')
        return redirect(url_for('add',tableClass=tableClass))
    return render_template('add.html',title=title,tableClass=tableClass,form=form)

#View table
@app.route('/view/<string:tableClass>')
def view(tableClass):
    data = psql_to_pandas(eval(tableClass).query.order_by(eval(tableClass).id))
    if tableClass=='Partners':
        title = "View Partners"
        colnames=['Partner Name','Country','Role']
        editlink="/edit-partner/"
    elif tableClass=='Work_Packages':
        title = "View Work Packages"
        colnames=['Code','Name']
        editlink="/edit-work-package/"
    elif tableClass=='Deliverables':
        title = "View Deliverables"
        colnames=['Code','Work Package','Description','Responsible Partner','Month Due','Progress','% Complete']
        editlink="/edit-deliverable/"
    return render_template('view.html',title=title,colnames=colnames,tableClass=tableClass,data=data)

#Delete entry
@app.route('/delete/<string:tableClass>/<string:id>', methods=['POST'])
def delete(tableClass,id):
    db_row = eval(tableClass).query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    psql_delete(db_row)
    flash('Entry deleted', 'success')
    return redirect(url_for('view',tableClass=tableClass))

#Edit entry
@app.route('/edit/<string:tableClass>/<string:id>', methods=['GET','POST'])
def edit(tableClass,id):
    form = eval(tableClass+"_Form")(request.form)
    db_row = eval(tableClass).query.filter_by(id=id).first()
    #Set title and tweak form
    if tableClass=='Partners':
        title = "Edit Partner"
    elif tableClass=='Work_Packages':
        title = "Edit Work Package"
    elif tableClass=='Deliverables':
        title = "Edit Deliverable"
        form.work_package.choices = table_list('Work_Packages','code')
        form.responsible_partner.choices = table_list('Partners','name')
    if db_row is None:
        abort(404)
    if request.method == 'POST' and form.validate():
        #Get each form field and update DB:
        for field in form:
            exec("db_row."+field.name+" = field.data")
        db.session.commit()
        #Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('view',tableClass=tableClass))
    #Pre-populate form fields with existing data
    for i,field in enumerate(form):
        if i==0: #Grey out first (immutable) field
            field.render_kw = {'readonly': 'readonly'}
        exec("field.data = db_row."+field.name)
    return render_template('edit.html',title=title,tableClass=tableClass,id=id,form=form)

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
    app.run()
