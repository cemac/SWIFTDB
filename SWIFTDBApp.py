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

class WP_Deliverables_Form(Form):
    code = StringField(u'Deliverable Code')
    work_package = StringField(u'Work Package')
    description = TextAreaField(u'Description')
    responsible_partner = StringField(u'Responsible Partner')
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
    #Get form (and tweak where necessary):
    form = eval(tableClass+"_Form")(request.form)
    if tableClass=='Deliverables':
        form.work_package.choices = table_list('Work_Packages','code')
        form.responsible_partner.choices = table_list('Partners','name')
    #Set title:
    title="Add to "+tableClass.replace("_"," ")
    #If user submits add entry form:
    if request.method == 'POST' and form.validate():
        #Get form fields:
        formdata=[]
        db_string = ""
        for f,field in enumerate(form):
            formdata.append(field.data)
            db_string += str(field.name) + "=formdata["+str(f)+"],"
        #Add to DB:
        db_string = tableClass+"("+db_string[:-1]+")"
        db_row = eval(db_string)
        psql_insert(db_row)
        #Return with success
        flash('Added to database', 'success')
        return redirect(url_for('add',tableClass=tableClass))
    return render_template('add.html',title=title,tableClass=tableClass,form=form)

#View table
@app.route('/view/<string:tableClass>')
def view(tableClass):
    #Retrieve all DB data for given table:
    data = psql_to_pandas(eval(tableClass).query.order_by(eval(tableClass).id))
    #Set title:
    title = "View "+tableClass.replace("_"," ")
    #Set table column names:
    colnames=[s.replace("_"," ").title() for s in data.columns.values[1:]]
    return render_template('view.html',title=title,colnames=colnames,tableClass=tableClass,admin=True,data=data)

#Delete entry
@app.route('/delete/<string:tableClass>/<string:id>', methods=['POST'])
def delete(tableClass,id):
    #Retrieve DB entry:
    db_row = eval(tableClass).query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Delete from DB:
    psql_delete(db_row)
    #Return with success:
    flash('Entry deleted', 'success')
    return redirect(url_for('view',tableClass=tableClass))

#Edit entry
@app.route('/edit/<string:tableClass>/<string:id>', methods=['GET','POST'])
def edit(tableClass,id):
    #Retrieve DB entry:
    db_row = eval(tableClass).query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Get form (and tweak where necessary):
    form = eval(tableClass+"_Form")(request.form)
    if tableClass=='Deliverables':
        form.work_package.choices = table_list('Work_Packages','code')
        form.responsible_partner.choices = table_list('Partners','name')
    #If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        #Get each form field and update DB:
        for field in form:
            exec("db_row."+field.name+" = field.data")
        db.session.commit()
        #Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('view',tableClass=tableClass))
    #Set title:
    title = "Edit "+tableClass[:-1].replace("_"," ")
    #Pre-populate form fields with existing data:
    for i,field in enumerate(form):
        if i==0: #Grey out first (immutable) field
            field.render_kw = {'readonly': 'readonly'}
        if not request.method == 'POST':
            exec("field.data = db_row."+field.name)
    return render_template('edit.html',title=title,tableClass=tableClass,id=id,form=form)

#WP summary
@app.route('/wp-summary/<string:id>')
def wp_summary(id):
    #Retrieve DB entry:
    db_row = Work_Packages.query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Retrieve all deliverables belonging to this work package:
    data = psql_to_pandas(Deliverables.query.filter_by(work_package=db_row.code).order_by(Deliverables.id))
    #Set title:
    title = "Deliverables for Work Package "+db_row.code+" ("+db_row.name+")"
    #Set table column names:
    colnames=[s.replace("_"," ").title() for s in data.columns.values[1:]]
    return render_template('view.html',title=title,colnames=colnames,tableClass='Deliverables',admin=False,data=data)

#Edit deliverable as WP-leader
@app.route('/wp-edit/<string:id>', methods=['GET','POST'])
def wp_edit(id):
    #Retrieve DB entry:
    db_row = Deliverables.query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Get form:
    form = WP_Deliverables_Form(request.form)
    #If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        #Get each form field and update DB:
        for field in form:
            exec("db_row."+field.name+" = field.data")
        db.session.commit()
        #Retrive id of work package this deliverable belongs to:
        wp_id = Work_Packages.query.filter_by(code=db_row.work_package).first().id
        #Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('wp_summary',id=wp_id))
    #Pre-populate form fields with existing data:
    for i,field in enumerate(form):
        if i<=4: #Grey out immutable fields
            field.render_kw = {'readonly': 'readonly'}
        if not request.method == 'POST':
             exec("field.data = db_row."+field.name)
    return render_template('wp-edit.html',id=id,form=form)

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
