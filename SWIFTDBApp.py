from flask import Flask, render_template, flash, redirect, url_for, request, g, session, abort
from wtforms import Form, validators, StringField, SelectField, TextAreaField, IntegerField, PasswordField, SelectMultipleField, widgets
import datetime as dt
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt

app = Flask(__name__)

#Set config variables:
assert "APP_SETTINGS" in os.environ, "APP_SETTINGS environment variable not set"
assert "SECRET_KEY" in os.environ, "SECRET_KEY environment variable not set"
assert "ADMIN_PWD" in os.environ, "ADMIN_PWD environment variable not set"
assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable not set"
app.config.from_object(os.environ['APP_SETTINGS'])

#Configure postgresql database:
db = SQLAlchemy(app)
from models import Partners, Work_Packages, Deliverables, Users, Users2Work_Packages, Tasks, Users2Partners

#Set any other parameters:
endMonth = 51 #End month (from project start month)

########## PSQL FUNCTIONS ##########
def psql_to_pandas(query):
    df = pd.read_sql(query.statement,db.session.bind)
    return df

def psql_insert(row,flashMsg=True):
    try:
        db.session.add(row)
        db.session.commit()
        if flashMsg:
            flash('Added to database', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Integrity Error: Violation of unique constraint(s)', 'danger')
    return

def psql_delete(row,flashMsg=True):
    try:
        db.session.delete(row)
        db.session.commit()
        if flashMsg:
            flash('Entry deleted', 'success')
    except:
        db.session.rollback()
        flash('Integrity Error: Cannot delete, other database entries likely reference this one', 'danger')
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

#Check if user is logged in as admin
def is_logged_in_as_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['username']=='admin':
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, please login as admin', 'danger')
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
        [validators.NumberRange(min=0,max=endMonth,message="Must be between 0 and "+str(endMonth))])
    progress = TextAreaField(u'Progress',
        validators=[validators.Optional()])
    percent = IntegerField(u'*Percentage Complete',
        [validators.NumberRange(min=0,max=100,message="Must be between 0 and 100")])

class WP_Deliverables_Form(Form):
    code = StringField(u'Deliverable Code')
    work_package = StringField(u'Work Package')
    description = TextAreaField(u'Description')
    responsible_partner = StringField(u'Responsible Partner')
    month_due = IntegerField(u'Month Due')
    progress = TextAreaField(u'Progress',
        validators=[validators.Optional()])
    percent = IntegerField(u'*Percentage Complete',
        [validators.NumberRange(min=0,max=100,message="Must be between 0 and 100")])

class Users_Form(Form):
    username = StringField('Username',[validators.Length(min=4, max=25)])
    password = PasswordField('Password',
        [validators.Regexp('^([a-zA-Z0-9]{8,})$',
        message='Password must be mimimum 8 characters and contain only uppercase letters, \
        lowercase letters and numbers')])

class ChangePwdForm(Form):
    current = PasswordField('Current password',
        [validators.DataRequired()])
    new = PasswordField('New password',
        [validators.Regexp('^([a-zA-Z0-9]{8,})$',
        message='Password must be mimimum 8 characters and contain only uppercase letters, \
        lowercase letters and numbers')])
    confirm = PasswordField('Confirm new password',
        [validators.EqualTo('new', message='Passwords do no match')])

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AccessForm(Form):
    username = StringField('Username')
    work_packages = MultiCheckboxField('This user is work package leader of (and can therefore update progress on deliverables belonging to...):')
    partners = MultiCheckboxField('This user is partner leader of (and can therefore update progress on tasks for which the responsible parner is...):')

class Tasks_Form(Form):
    code = StringField(u'*Task Code',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. T-R1.1.1"})
    description = TextAreaField(u'*Description',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. Development of reporting \
template for baselining the current provision of forecasts."})
    responsible_partner = SelectField(u'*Responsible Partner',
        [validators.NoneOf(('blank'),message='Please select')])
    month_due = IntegerField(u'Month Due',
        [validators.NumberRange(min=0,max=endMonth,message="Must be between 0 and "+str(endMonth))])
    progress = TextAreaField(u'Progress',
        validators=[validators.Optional()])
    percent = IntegerField(u'*Percentage Complete',
        [validators.NumberRange(min=0,max=100,message="Must be between 0 and 100")])

class Your_Tasks_Form(Form):
    code = StringField(u'Task Code')
    description = TextAreaField(u'Description')
    responsible_partner = StringField(u'Responsible Partner')
    month_due = IntegerField(u'Month Due')
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
@is_logged_in_as_admin
def add(tableClass):
    if tableClass not in ['Partners', 'Work_Packages', 'Deliverables', 'Users', 'Tasks']:
        abort(404)
    #Get form (and tweak where necessary):
    form = eval(tableClass+"_Form")(request.form)
    if tableClass=='Deliverables':
        form.work_package.choices = table_list('Work_Packages','code')
    if tableClass=='Deliverables' or tableClass=='Tasks':
        form.responsible_partner.choices = table_list('Partners','name')
    #Set title:
    title="Add to "+tableClass.replace("_"," ")
    #If user submits add entry form:
    if request.method == 'POST' and form.validate():
        #Get form fields:
        if tableClass=='Users':
            form.password.data = sha256_crypt.encrypt(str(form.password.data))
        formdata=[]
        db_string = ""
        for f,field in enumerate(form):
            formdata.append(field.data)
            db_string += str(field.name) + "=formdata["+str(f)+"],"
        #Add to DB:
        db_string = tableClass+"("+db_string[:-1]+")"
        db_row = eval(db_string)
        psql_insert(db_row)
        return redirect(url_for('add',tableClass=tableClass))
    return render_template('add.html',title=title,tableClass=tableClass,form=form)

#View table
@app.route('/view/<string:tableClass>')
@is_logged_in_as_admin
def view(tableClass):
    if tableClass not in ['Partners', 'Work_Packages', 'Deliverables', 'Users', 'Tasks']:
        abort(404)
    #Retrieve all DB data for given table:
    data = psql_to_pandas(eval(tableClass).query.order_by(eval(tableClass).id))
    data.fillna(value="", inplace=True)
    if tableClass=='Users':
        data['password'] = '********'
    #Set title:
    title = "View "+tableClass.replace("_"," ")
    #Set table column names:
    colnames=[s.replace("_"," ").title() for s in data.columns.values[1:]]
    return render_template('view.html',title=title,colnames=colnames,tableClass=tableClass,editLink="edit",data=data)

#Delete entry
@app.route('/delete/<string:tableClass>/<string:id>', methods=['POST'])
@is_logged_in_as_admin
def delete(tableClass,id):
    #Retrieve DB entry:
    db_row = eval(tableClass).query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Delete from DB:
    psql_delete(db_row)
    return redirect(url_for('view',tableClass=tableClass))

#Edit entry
@app.route('/edit/<string:tableClass>/<string:id>', methods=['GET','POST'])
@is_logged_in_as_admin
def edit(tableClass,id):
    if tableClass not in ['Partners', 'Work_Packages', 'Deliverables', 'Tasks']:
        abort(404)
    #Retrieve DB entry:
    db_row = eval(tableClass).query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Get form (and tweak where necessary):
    form = eval(tableClass+"_Form")(request.form)
    if tableClass=='Deliverables':
        form.work_package.choices = table_list('Work_Packages','code')
    if tableClass=='Deliverables' or tableClass=='Tasks':
        form.responsible_partner.choices = table_list('Partners','name')
    #If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        #Get each form field and update DB:
        if tableClass=='Users':
            form.password.data = sha256_crypt.encrypt(str(form.password.data))
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

#WP list for WP leaders
@app.route('/wp-list')
@is_logged_in
def wp_list():
    #Retrieve all work packages:
    all_wps = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    #Select only the accessible work packages for this user:
    if session['username'] == 'admin':
        accessible_wps = all_wps
    else:
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(username=session['username']))['work_package'].tolist()
        accessible_wps = all_wps[all_wps.code.isin(user_wps)]
    return render_template('wp-list.html',data=accessible_wps)

#WP deliverables summary for WP leaders
@app.route('/wp-summary/<string:id>')
@is_logged_in
def wp_summary(id):
    #Retrieve DB entry:
    db_row = Work_Packages.query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Check user has access to this wp:
    if not session['username'] == 'admin':
        wp_code = db_row.code
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(username=session['username']))['work_package'].tolist()
        if wp_code not in user_wps:
            abort(403)
    #Retrieve all deliverables belonging to this work package:
    data = psql_to_pandas(Deliverables.query.filter_by(work_package=db_row.code).order_by(Deliverables.id))
    del data['work_package']
    data.fillna(value="", inplace=True)
    #Set title:
    title = "Deliverables for Work Package "+db_row.code+" ("+db_row.name+")"
    #Set table column names:
    colnames=[s.replace("_"," ").title() for s in data.columns.values[1:]]
    return render_template('view.html',title=title,colnames=colnames,tableClass='Deliverables',editLink="wp-edit",data=data)

#Edit deliverable as WP leader
@app.route('/wp-edit/<string:id>', methods=['GET','POST'])
@is_logged_in
def wp_edit(id):
    #Retrieve DB entry:
    db_row = Deliverables.query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Check user has access to this deliverable:
    if not session['username'] == 'admin':
        wp_code = db_row.work_package
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(username=session['username']))['work_package'].tolist()
        if wp_code not in user_wps:
            abort(403)
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
    return render_template('alt-edit.html',id=id,form=form,title="Edit Deliverable",editLink="wp-edit")

#Tasks for a given user
@app.route('/task-list')
@is_logged_in
def task_list():
    #Retrieve all tasks:
    all_tasks = psql_to_pandas(Tasks.query.order_by(Tasks.id))
    #Select only the accessible tasks for this user:
    if session['username'] == 'admin':
        accessible_tasks = all_tasks
    else:
        user_partners = psql_to_pandas(Users2Partners.query.filter_by(username=session['username']))['partner'].tolist()
        accessible_tasks = all_tasks[all_tasks.responsible_partner.isin(user_partners)]
    accessible_tasks.fillna(value="", inplace=True)
    #Set title:
    title = "Your Tasks"
    #Set table column names:
    colnames=[s.replace("_"," ").title() for s in accessible_tasks.columns.values[1:]]
    return render_template('view.html',title=title,colnames=colnames,tableClass='Tasks',editLink="task-edit",data=accessible_tasks)

#Edit task as non-admin
@app.route('/task-edit/<string:id>', methods=['GET','POST'])
@is_logged_in
def task_edit(id):
    #Retrieve DB entry:
    db_row = Tasks.query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    #Check user has access to this task:
    if not session['username'] == 'admin':
        partner_name = db_row.responsible_partner
        user_partners = psql_to_pandas(Users2Partners.query.filter_by(username=session['username']))['partner'].tolist()
        if partner_name not in user_partners:
            abort(403)
    #Get form:
    form = Your_Tasks_Form(request.form)
    #If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        #Get each form field and update DB:
        for field in form:
            exec("db_row."+field.name+" = field.data")
        db.session.commit()
        flash('Edits successful', 'success')
        return redirect(url_for('task_list'))
    #Pre-populate form fields with existing data:
    for i,field in enumerate(form):
        if i<=3: #Grey out immutable fields
            field.render_kw = {'readonly': 'readonly'}
        if not request.method == 'POST':
             exec("field.data = db_row."+field.name)
    return render_template('alt-edit.html',id=id,form=form,title="Edit Task",editLink="task-edit")


#Access settings for a given user
@app.route('/access/<string:id>', methods=['GET','POST'])
@is_logged_in_as_admin
def access(id):
    form = AccessForm(request.form)
    form.work_packages.choices = table_list('Work_Packages','code')[1:]
    form.partners.choices = table_list('Partners','name')[1:]
    #Retrieve user DB entry:
    user = Users.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    #Retrieve all relevant entries in users2work_packages and users2partners:
    current_work_packages = psql_to_pandas(Users2Work_Packages.query.filter_by(username=user.username))['work_package'].tolist()
    current_partners = psql_to_pandas(Users2Partners.query.filter_by(username=user.username))['partner'].tolist()
    #If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        new_work_packages = form.work_packages.data
        new_partners = form.partners.data
        #Delete relevant rows from users2work_packages:
        wps_to_delete = list(set(current_work_packages)-set(new_work_packages))
        for wp in wps_to_delete:
            db_row = Users2Work_Packages.query.filter_by(username=user.username,work_package=wp).first()
            psql_delete(db_row,flashMsg=False)
        #Add relevant rows to users2work_packages:
        wps_to_add = list(set(new_work_packages)-set(current_work_packages))
        for wp in wps_to_add:
            db_row = Users2Work_Packages(username=user.username,work_package=wp)
            psql_insert(db_row,flashMsg=False)
        #Delete relevant rows from users2partners:
        partners_to_delete = list(set(current_partners)-set(new_partners))
        for partner in partners_to_delete:
            db_row = Users2Partners.query.filter_by(username=user.username,partner=partner).first()
            psql_delete(db_row,flashMsg=False)
        #Add relevant rows to users2work_packages:
        partners_to_add = list(set(new_partners)-set(current_partners))
        for partner in partners_to_add:
            db_row = Users2Partners(username=user.username,partner=partner)
            psql_insert(db_row,flashMsg=False)
        #Return with success
        flash('Edits successful', 'success')
        return redirect(url_for('access',id=id))
    #Pre-populate form fields with existing data:
    form.username.render_kw = {'readonly': 'readonly'}
    form.username.data = user.username
    form.work_packages.data = current_work_packages
    form.partners.data = current_partners
    return render_template('access.html',form=form,id=id)

#Login
@app.route('/login', methods=["GET","POST"])
def login():
    #Attempt to log in:
    if request.method == 'POST':
        #Get form fields
        username = request.form['username']
        password_candidate = request.form['password']
        #Check admin account:
        if username == 'admin':
            password = app.config['ADMIN_PWD']
            if password_candidate == password:
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
                return redirect(url_for('login'))
        #Check user accounts:
        user = Users.query.filter_by(username=username).first()
        if user is not None:
            password = user.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
                return redirect(url_for('login'))
        #Username not found:
        flash('Username not found', 'danger')
        return redirect(url_for('login'))
    #Already logged in:
    if 'logged_in' in session:
        flash('Already logged in', 'warning')
        return redirect(url_for('index'))
    #Not yet logged in:
    return render_template('login.html')

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

#Change password
@app.route('/change-pwd', methods=["GET","POST"])
@is_logged_in
def change_pwd():
    form = ChangePwdForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users.query.filter_by(username=session['username']).first()
        password = user.password
        current = form.current.data
        if sha256_crypt.verify(current, password):
            user.password = sha256_crypt.encrypt(str(form.new.data))
            db.session.commit()
            flash('Password changed', 'success')
            return redirect(url_for('change_pwd'))
        else:
            flash('Current password incorrect', 'danger')
            return redirect(url_for('change_pwd'))
    return render_template('change-pwd.html',form=form)
# ssl
@app.route('/.well-known/acme-challenge/0pQ9Y9nneRwz6xitl6qTxzdBRC38pHJYgw-ey0JMJgI')
def letsencrypt_check():
    return '0pQ9Y9nneRwz6xitl6qTxzdBRC38pHJYgw-ey0JMJgI.eo3R_jzJhz37owhBTH73qvPeAHxNjuWt8W-FQJOCpeg'



if __name__ == '__main__':
    app.run()
