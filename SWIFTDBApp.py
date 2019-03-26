'''
SWIFTDBApp.py:

This module was developed by CEMAC as part of the AFRICAN SWIFT Project.
This is the database management tool and flask web app used to run the SWIFT
project management website hosted on heroku.

Example:
    To use::
        python manage.py

Attributes:
    endMonth(int): Project length in months

.. CEMAC_stomtracking:
   https://github.com/cemac/SWIFTDB
'''

from flask import Flask, render_template, flash, redirect, url_for, request
from flask import g, session, abort
from wtforms import Form, validators, StringField, SelectField, TextAreaField
from wtforms import IntegerField, PasswordField, SelectMultipleField, widgets
import datetime as dt
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt


app = Flask(__name__)

# Set config variables:
assert "APP_SETTINGS" in os.environ, "APP_SETTINGS environment variable not set"
assert "SECRET_KEY" in os.environ, "SECRET_KEY environment variable not set"
assert "ADMIN_PWD" in os.environ, "ADMIN_PWD environment variable not set"
assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable not set"
app.config.from_object(os.environ['APP_SETTINGS'])

# Configure postgresql database:
db = SQLAlchemy(app)
from models import Users2Work_Packages, Tasks, Users2Partners
from models import Partners, Work_Packages, Deliverables, Users
# Set any other parameters:
endMonth = 51  # End month (from project start month)
# ~~~~~~ PSQL FUNCTIONS ~~~~~~~ #


def psql_to_pandas(query):
    df = pd.read_sql(query.statement, db.session.bind)
    return df


def psql_insert(row, flashMsg=True):
    try:
        db.session.add(row)
        db.session.commit()
        if flashMsg:
            flash('Added to database', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Integrity Error: Violation of unique constraint(s)', 'danger')
    return


def psql_delete(row, flashMsg=True):
    try:
        db.session.delete(row)
        db.session.commit()
        if flashMsg:
            flash('Entry deleted', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Integrity Error: Cannot delete, other database entries likely' +
              'reference this one', 'danger')
    return
####################################
# ######### LOGGED-IN FUNCTIONS ##########
# Check if user is logged in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, please login', 'danger')
            return redirect(url_for('index'))
    return wrap

# Check if user is logged in as admin


def is_logged_in_as_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['username'] == 'admin':
            return f(*args, **kwargs)
        elif 'logged_in' in session and session['admin'] == 'True':
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, please login as admin', 'danger')
            return redirect(url_for('index'))
    return wrap
#########################################

# ######### MISC FUNCTIONS ##########


def table_list(tableClass, col):
    DF = psql_to_pandas(eval(tableClass).query.order_by(eval(tableClass).id))
    list = [('blank', '--Please select--')]
    for element in DF[col]:
        list.append((element, element))
    return list
#########################################

# ######### FORM CLASSES ##########


class Partners_Form(Form):
    name = StringField(u'*Partner Name',
                       [validators.InputRequired()],
                       render_kw={"placeholder": "e.g. Leeds"})
    country = StringField(u'Country',
                          render_kw={"placeholder": "e.g. UK"})
    role = StringField(u'Role', render_kw={"placeholder":
                                           "e.g. 'Academic' or 'Operational'"})


class Work_Packages_Form(Form):
    code = StringField(u'*Work Package Code',
                       [validators.InputRequired()],
                       render_kw={"placeholder": "e.g. WP-C1"})
    name = StringField(u'*Name',
                       [validators.InputRequired()],
                       render_kw={"placeholder": "e.g. Training"})
    status = StringField(u'*Work Package Status',
                         [validators.InputRequired()],
                         render_kw={"placeholder": "e.g. Overview of Progress as a whole"})
    issues = StringField(u'*Issues',
                         [validators.InputRequired()],
                         render_kw={"placeholder": "e.g. Highlight any potential issues or risks"})
    next_deliverable = StringField(u'*Next Quarter Deliverables',
                         [validators.InputRequired()],
                         render_kw={"placeholder": "e.g. Upcomming deliverables due"})


class Deliverables_Form(Form):
    code = StringField(u'*Deliverable Code',
                       [validators.InputRequired()],
                       render_kw={"placeholder": "e.g. D-R1.1"})
    work_package = SelectField(u'*Work Package',
                               [validators.NoneOf(('blank'),
                                                  message='Please select')])
    description = TextAreaField(u'*Description',
                                [validators.InputRequired()],
                                render_kw={"placeholder": "e.g. Report on current state of knowledge regarding user needs for forecasts at different timescales in each sector."})
    partner = SelectField(u'*Partner', [validators.NoneOf(('blank'),
                                                          message='Please select')])
    month_due = IntegerField(u'Month Due',
                             [validators.NumberRange(min=0, max=endMonth,
                                                     message="Must be between 0 and " + str(endMonth))])
    progress = TextAreaField(u'Progress',
                             validators=[validators.Optional()])
    percent = IntegerField(u'*Percentage Complete',
                           [validators.NumberRange(min=0, max=100,
                                                   message="Must be between 0 and 100")])


class Your_Work_Packages_Form(Form):
    code = StringField(u'*Work Package Code')
    name = StringField(u'*Name')
    status = StringField(u'*Work Package Status',
                         [validators.InputRequired()],
                         render_kw={"placeholder": "e.g. Overview of Progress as a whole"})
    issues = StringField(u'*Issues',
                         [validators.InputRequired()],
                         render_kw={"placeholder": "e.g. Highlight any potential issues or risks"})
    next_deliverable = StringField(u'*Next Quarter Deliverables',
                         [validators.InputRequired()],
                         render_kw={"placeholder": "e.g. Upcomming deliverables due"})

class Your_Deliverables_Form(Form):
    code = StringField(u'Deliverable Code')
    work_package = StringField(u'Work Package')
    description = TextAreaField(u'Description')
    partner = StringField(u'Partner')
    month_due = IntegerField(u'Month Due')
    progress = TextAreaField(u'Progress',
                             validators=[validators.Optional()])
    percent = IntegerField(u'*Percentage Complete',
                           [validators.NumberRange(min=0, max=100,
                                                   message="Must be between 0 and 100")])


class Users_Form(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password',
                             [validators.Regexp('^([a-zA-Z0-9]{8,})$',
                                                message='Password must be mimimum 8 characters and contain only uppercase letters, \
        lowercase letters and numbers')])


class ChangePwdForm(Form):
    current = PasswordField('Current password', [validators.DataRequired()])
    new = PasswordField('New password',
                        [validators.Regexp('^([a-zA-Z0-9]{8,})$',
                                           message='Password must be mimimum 8 characters and contain only uppercase letters, \
        lowercase letters and numbers')])
    confirm = PasswordField('Confirm new password',
                            [validators.EqualTo('new',
                                                message='Passwords do no match')])


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AccessForm(Form):
    username = StringField('Username')
    AdminReader = MultiCheckboxField(
        'ADMIN or View all Access: (Grant Admin privallages or the ability to view all (read-only)):')
    work_packages = MultiCheckboxField(
        'WORK PACKAGE LEADERS: Can update Work Package progress and view associated Task and Deliverables:')
    partners = MultiCheckboxField(
        'PARTNER LEADER: Can update progress on tasks and deliverables for which they are the responsible partner:')


class Tasks_Form(Form):
    code = StringField(u'*Task Code',
                       [validators.InputRequired()],
                       render_kw={"placeholder": "e.g. T-R1.1.1"})
    description = TextAreaField(u'*Description',
                                [validators.InputRequired()],
                                render_kw={"placeholder": "e.g. Development of reporting \
template for baselining the current provision of forecasts."})
    partner = SelectField(u'*Partner',
                          [validators.NoneOf(('blank'),
                                             message='Please select')])
    work_package = SelectField(u'*Work Package',
                               [validators.NoneOf(('blank'),
                                                  message='Please select')])
    month_due = IntegerField(u'*Month Due',
                             [validators.NumberRange(min=0, max=endMonth,
                                                     message="Must be between 0 and " + str(endMonth))])
    progress = TextAreaField(u'Progress',
                             validators=[validators.Optional()])
    percent = IntegerField(u'*Percentage Complete',
                           [validators.NumberRange(min=0, max=100,
                                                   message="Must be between 0 and 100")])


class Your_Tasks_Form(Form):
    code = StringField(u'Task Code')
    description = TextAreaField(u'Description')
    partner = StringField(u'Partner')
    work_package = StringField(u'Work Package')
    month_due = IntegerField(u'Month Due')
    progress = TextAreaField(u'Progress',
                             validators=[validators.Optional()])
    percent = IntegerField(u'*Percentage Complete',
                           [validators.NumberRange(min=0, max=100,
                                                   message="Must be between 0 and 100")])


# Index
@app.route('/', methods=["GET"])
def index():
    WP = 'none'
    Ps = 'none'
    try:
        username = session['username']
        if request.method == 'GET':
            user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
                                      username=session['username'])
                                      )['work_package'].tolist()
            user_partners = psql_to_pandas(Users2Partners.query.filter_by(
                username=session['username']))['partner'].tolist()
            WP =  ", ".join(user_wps)
            Ps =  ", ".join(user_partners)
            if len(user_wps[:]) < 1:
                WP = 'none'
            if len(user_partners[:]) < 1:
                Ps = 'none'
    except:
        WP = 'none'
        Ps = 'none'
    return render_template('home.html', WP=WP, Ps=Ps)


# Add entry
@app.route('/add/<string:tableClass>', methods=["GET", "POST"])
@is_logged_in_as_admin
def add(tableClass):
    if tableClass not in ['Partners', 'Work_Packages', 'Deliverables', 'Users', 'Tasks']:
        abort(404)
    # Get form (and tweak where necessary):
    form = eval(tableClass + "_Form")(request.form)
    if tableClass == 'Deliverables' or tableClass == 'Tasks':
        form.work_package.choices = table_list('Work_Packages', 'code')
        form.partner.choices = table_list('Partners', 'name')
    # Set title:
    title = "Add to " + tableClass.replace("_", " ")
    # If user submits add entry form:
    if request.method == 'POST' and form.validate():
        # Get form fields:
        if tableClass == 'Users':
            form.password.data = sha256_crypt.encrypt(str(form.password.data))
        formdata = []
        db_string = ""
        for f, field in enumerate(form):
            formdata.append(field.data)
            db_string += str(field.name) + "=formdata[" + str(f) + "],"
        # Add to DB:
        db_string = tableClass + "(" + db_string[:-1] + ")"
        db_row = eval(db_string)
        psql_insert(db_row)
        return redirect(url_for('add', tableClass=tableClass))
    return render_template('add.html', title=title, tableClass=tableClass,
                           form=form)


# View table
@app.route('/view/<string:tableClass>')
@is_logged_in_as_admin
def view(tableClass):
    if tableClass not in ['Partners', 'Work_Packages', 'Deliverables', 'Users', 'Tasks']:
        abort(404)
    # Retrieve all DB data for given table:
    data = psql_to_pandas(eval(tableClass).query.order_by(eval(tableClass).id))
    data.fillna(value="", inplace=True)
    if tableClass == 'Users':
        data['password'] = '********'
    # Set title:
    title = "View " + tableClass.replace("_", " ")
    # Set table column names:
    description = ('Admin access to ' + tableClass.replace("_", " "))
    colnames = [s.replace("_", " ").title() for s in data.columns.values[1:]]
    return render_template('view.html', title=title, colnames=colnames,
                           tableClass=tableClass, editLink="edit", data=data)


# Delete entry
@app.route('/delete/<string:tableClass>/<string:id>', methods=['POST'])
@is_logged_in_as_admin
def delete(tableClass, id):
    # Retrieve DB entry:
    db_row = eval(tableClass).query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    if tableClass=='Partners' and db_row.name == 'admin':
        abort(403)
    if tableClass=='Partners' and db_row.name == 'ViewAll':
        abort(403)
    # Delete from DB:
    psql_delete(db_row)
    return redirect(url_for('view', tableClass=tableClass))


# Edit entry
@app.route('/edit/<string:tableClass>/<string:id>', methods=['GET', 'POST'])
@is_logged_in_as_admin
def edit(tableClass, id):
    if tableClass not in ['Partners', 'Work_Packages', 'Deliverables', 'Tasks']:
        abort(404)
    # Retrieve DB entry:
    db_row = eval(tableClass).query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    # Get form (and tweak where necessary):
    form = eval(tableClass + "_Form")(request.form)
    if tableClass == 'Deliverables' or tableClass == 'Tasks':
        form.work_package.choices = table_list('Work_Packages', 'code')
        form.partner.choices = table_list('Partners', 'name')
    # If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        # Get each form field and update DB:
        if tableClass == 'Users':
            form.password.data = sha256_crypt.encrypt(str(form.password.data))
        for field in form:
            exec("db_row." + field.name + " = field.data")
        db.session.commit()
        # Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('view', tableClass=tableClass))
    # Set title:
    title = "Edit " + tableClass[:-1].replace("_", " ")
    # Pre-populate form fields with existing data:
    for i, field in enumerate(form):
        if i == 0:  # Grey out first (immutable) field
            field.render_kw = {'readonly': 'readonly'}
        if field.name == 'work_package':
            field.render_kw = {'readonly': 'readonly'}
        if not request.method == 'POST':
            exec("field.data = db_row." + field.name)
    return render_template('edit.html', title=title, tableClass=tableClass,
                           id=id, form=form)


# WP list for WP leaders
@app.route('/wp-list')
@is_logged_in
def wp_list():
    # Retrieve all work packages:
    all_wps = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    # Select only the accessible work packages for this user:
    if session['username'] == 'admin':
        accessible_wps = all_wps
        description = 'Admin view (read-only), please use admin menu to edit'
    else:
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
            username=session['username']))['work_package'].tolist()
        accessible_wps = all_wps[all_wps.code.isin(user_wps)]
        description = 'You are WP Leader for: ' +  ", ".join(user_wps)
    # Set title:
    title = "Your Work Packages"
    return render_template('wp-list.html', editLink="wp-edit",
                           tableClass='Work_Packages', data=accessible_wps,
                           description=description, title=title)


# WP list for WP leaders
@app.route('/wp-view')
@is_logged_in
def wp_view():
    # Retrieve all work packages:
    all_wps = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    # Select only the accessible work packages for this user:
    if session['username'] == 'admin':
        accessible_wps = all_wps
        description = 'Admin view (read-only), please use admin menu to edit'
    else:
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
            username=session['username']))['work_package'].tolist()
        accessible_wps = all_wps[all_wps.code.isin(user_wps)]
        description = 'You are WP Leader for: ' +  ", ".join(user_wps)
    # Set title:
    title = "Viewable Work Packages"
    return render_template('wp-list.html', editLink="none",
                           tableClass='Work_Packages', data=accessible_wps,
                           description=description, title=title)


# WP list for WP leaders
@app.route('/wp-reader')
@is_logged_in
def wp_readers():
    # Retrieve all work packages:
    all_wps = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    # Select only the accessible work packages for this user:
    if session['username'] == 'admin' or session['reader'] == 'True':
        accessible_wps = all_wps
        description = 'Admin view (read-only), please use admin menu to edit'
    else:
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
            username=session['username']))['work_package'].tolist()
        accessible_wps = all_wps[all_wps.code.isin(user_wps)]
        description = 'You are WP Leader for: ' +  ", ".join(user_wps)
    # Set title:
    title = "Viewable Work Packages"
    return render_template('wp-list.html', editLink="none",
                           tableClass='Work_Packages', data=accessible_wps,
                           description=description, title=title)


# WP edit status for WP leaders
@app.route('/wp-edit/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def wp_edit(id):
    # Retrieve DB entry:
    db_row = Work_Packages.query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    # Check user has access to this wp:
    if not session['username'] == 'admin':
        wp_code = db_row.code
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
            username=session['username']))['work_package'].tolist()
        if wp_code not in user_wps:
            abort(403)
    # Get form:
    form = Your_Work_Packages_Form(request.form)
    # If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        # Get each form field and update DB:
        for field in form:
            exec("db_row." + field.name + " = field.data")
        db.session.commit()
        flash('Edits successful', 'success')
        return redirect(url_for('wp_list'))
    # Pre-populate form fields with existing data:
    for i, field in enumerate(form):
        if i <= 1:  # Grey out immutable fields
            field.render_kw = {'readonly': 'readonly'}
        if not request.method == 'POST':
            exec("field.data = db_row." + field.name)
    return render_template('alt-edit.html', title="Update Work Package ",
                            id=id, form=form, editLink="wp-edit")


# Tasks for a given user

@app.route('/task-list')
@is_logged_in
def task_list():
    # Retrieve all tasks:
    all_tasks = psql_to_pandas(Tasks.query.order_by(Tasks.id))
    # Select only the accessible tasks for this user:
    if session['username'] == 'admin':
        accessible_tasks = all_tasks
        description = 'Admin view (read-only), please use admin menu to edit'
    else:
        user_partners = psql_to_pandas(Users2Partners.query.filter_by(
            username=session['username']))['partner'].tolist()
        accessible_tasks = all_tasks[all_tasks.partner.isin(user_partners)]
        try:
            user_partners.remove('admin')
            user_partners.remove('ViewAll')
        except ValueError:
            pass
        description = 'You are Partner Leader for: ' +  ", ".join(user_partners)
    accessible_tasks.fillna(value="", inplace=True)
    data = accessible_tasks.drop_duplicates(keep='first', inplace=False)
    # Set title:
    title = "Tasks associated with your partner lead"
    # Set table column names:
    colnames = [s.replace("_", " ").title()
                for s in accessible_tasks.columns.values[1:]]
    return render_template('view.html', title=title, colnames=colnames,
                           tableClass='Tasks', editLink="task-edit",
                           data=data, description=description)


@app.route('/task-view')
@is_logged_in
def task_view():
    # Retrieve all tasks:
    all_tasks = psql_to_pandas(Tasks.query.order_by(Tasks.id))
    # Select only the accessible tasks for this user:
    if session['username'] == 'admin':
        accessible_tasks = all_tasks
        description = 'Read-only - Displaying All Tasks'
    else:
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
            username=session['username']))['work_package'].tolist()
        accessible_tasks = all_tasks[all_tasks.work_package.isin(user_wps)]
        accessible_tasks.fillna(value="", inplace=True)
        description = 'Displaying Tasks associated with Work Package(s): ' +  ", ".join(user_wps)
    accessible_tasks.fillna(value="", inplace=True)
    data = accessible_tasks.drop_duplicates(keep='first', inplace=False)
    # Set title:
    title = "Viewable Tasks"
    # Set table column names:
    colnames = [s.replace("_", " ").title()
                for s in accessible_tasks.columns.values[1:]]
    return render_template('view.html', title=title, colnames=colnames,
                           tableClass='Tasks', editLink="none",
                           data=data, description=description)


@app.route('/task-reader')
@is_logged_in
def task_reader():
    # Retrieve all tasks:
    all_tasks = psql_to_pandas(Tasks.query.order_by(Tasks.id))
    # Select only the accessible tasks for this user:
    if session['username'] == 'admin' or session['reader'] == 'True':
        accessible_tasks = all_tasks
        description = 'Read-only - Displaying All Tasks'
    else:
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
            username=session['username']))['work_package'].tolist()
        accessible_tasks = all_tasks[all_tasks.work_package.isin(user_wps)]
        accessible_tasks.fillna(value="", inplace=True)
        description = 'Displaying Tasks associated with Work Package(s): ' +  ", ".join(user_wps)
    accessible_tasks.fillna(value="", inplace=True)
    data = accessible_tasks.drop_duplicates(keep='first', inplace=False)
    # Set title:
    title = "Viewable Tasks"
    # Set table column names:
    colnames = [s.replace("_", " ").title()
                for s in accessible_tasks.columns.values[1:]]
    return render_template('view.html', title=title, colnames=colnames,
                           tableClass='Tasks', editLink="none",
                           data=data, description=description)


# Edit task as non-admin
@app.route('/task-edit/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def task_edit(id):
    # Retrieve DB entry:
    db_row = Tasks.query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    # Check user has access to this task:
    if not session['username'] == 'admin':
        partner_name = db_row.partner
        user_partners = psql_to_pandas(Users2Partners.query.filter_by(
            username=session['username']))['partner'].tolist()
        if partner_name not in user_partners:
            abort(403)
    # Get form:
    form = Your_Tasks_Form(request.form)
    # If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        # Get each form field and update DB:
        for field in form:
            exec("db_row." + field.name + " = field.data")
        db.session.commit()
        flash('Edits successful', 'success')
        return redirect(url_for('task_list'))
    # Pre-populate form fields with existing data:
    for i, field in enumerate(form):
        if i <= 4:  # Grey out immutable fields
            field.render_kw = {'readonly': 'readonly'}
        if not request.method == 'POST':
            exec("field.data = db_row." + field.name)
    return render_template('alt-edit.html', id=id, form=form,
                           title="Edit Task", editLink="task-edit")


# Tasks for a given user
@app.route('/deliverables-list')
@is_logged_in
def deliverables_list():
    # Retrieve all work packages:
    all_wps = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    # Retrieve all tasks:
    all_tasks = psql_to_pandas(Deliverables.query.order_by(Deliverables.id))
    # Select only the accessible tasks for this user:
    if session['username'] == 'admin':
        accessible_data = all_tasks
        description = 'Admin view (read-only), please use admin menu to edit'
    else:
        user_partners = psql_to_pandas(Users2Partners.query.filter_by(
            username=session['username']))['partner'].tolist()
        accessible_data = all_tasks[all_tasks.partner.isin(user_partners)]
        try:
            user_partners.remove('admin')
            user_partners.remove('ViewAll')
        except ValueError:
            pass
        description = 'You are Partner Leader for: ' + ", ".join(user_partners)
    accessible_data.fillna(value="", inplace=True)
    data = accessible_data.drop_duplicates(keep='first', inplace=False)
    title = "Deliverables for which you are Partner Leader "
    # Set table column names:
    colnames = [s.replace("_", " ").title() for s in
                accessible_data.columns.values[1:]]
    return render_template('view.html', title=title, colnames=colnames,
                           tableClass='Deliverables',
                           editLink="deliverables-edit", data=data,
                           description=description)


@app.route('/deliverables-view')
@is_logged_in
def deliverables_view():
    # Retrieve all work packages:
    all_wps = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    # Retrieve all tasks:
    all_tasks = psql_to_pandas(Deliverables.query.order_by(Deliverables.id))
    # Select only the accessible tasks for this user:
    if session['username'] == 'admin':
        accessible_data = all_tasks
        description = 'Read-only - Displaying All Tasks'
    else:
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
            username=session['username']))['work_package'].tolist()
        accessible_data = all_tasks[all_tasks.work_package.isin(user_wps)]
        accessible_data.fillna(value="", inplace=True)
        description = 'Displaying Deliverables associated with Work Package(s): ' + ", ".join(user_wps)
    accessible_data.fillna(value="", inplace=True)
    data = accessible_data.drop_duplicates(keep='first', inplace=False)
    title = "Viewable Deliverables"
    # Set table column names:
    colnames = [s.replace("_", " ").title() for s in
                accessible_data.columns.values[1:]]
    return render_template('view.html', title=title, colnames=colnames,
                           tableClass='Deliverables',
                           editLink="none", data=data,
                           description=description)


@app.route('/deliverables-reader')
@is_logged_in
def deliverables_reader():
    # Retrieve all work packages:
    all_wps = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    # Retrieve all tasks:
    all_tasks = psql_to_pandas(Deliverables.query.order_by(Deliverables.id))
    # Select only the accessible tasks for this user:
    if session['username'] == 'admin' or session['reader'] == 'True':
        accessible_data = all_tasks
        description = 'Read-only - Displaying All Tasks'
    else:
        user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
            username=session['username']))['work_package'].tolist()
        accessible_data = all_tasks[all_tasks.work_package.isin(user_wps)]
        accessible_data.fillna(value="", inplace=True)
        description = 'Displaying Deliverables associated with Work Package(s): ' + ", ".join(user_wps)
    accessible_data.fillna(value="", inplace=True)
    data = accessible_data.drop_duplicates(keep='first', inplace=False)
    title = "Viewable Deliverables"
    # Set table column names:
    colnames = [s.replace("_", " ").title() for s in
                accessible_data.columns.values[1:]]
    return render_template('view.html', title=title, colnames=colnames,
                           tableClass='Deliverables',
                           editLink="none", data=data,
                           description=description)


# Edit deliverable as WP leader
@app.route('/deliverables-edit/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def deliverables_edit(id):
    # Retrieve DB entry:
    db_row = Deliverables.query.filter_by(id=id).first()
    if db_row is None:
        abort(404)
    # Check user has access to this deliverable:
    # Check user has access to this task:
    if not session['username'] == 'admin':
        partner_name = db_row.partner
        user_partners = psql_to_pandas(Users2Partners.query.filter_by(
            username=session['username']))['partner'].tolist()
        if partner_name not in user_partners:
            abort(403)
    # Get form:
    form = Your_Deliverables_Form(request.form)
    # If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        # Get each form field and update DB:
        for field in form:
            exec("db_row." + field.name + " = field.data")
        db.session.commit()
        # Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('deliverables_list', id=id))
    # Pre-populate form fields with existing data:
    for i, field in enumerate(form):
        if i <= 4:  # Grey out immutable fields
            field.render_kw = {'readonly': 'readonly'}
        if not request.method == 'POST':
            exec("field.data = db_row." + field.name)
    return render_template('alt-edit.html', id=id, form=form,
                           title="Edit Deliverable",
                           editLink="deliverables-edit")


# Access settings for a given user
@app.route('/access/<string:id>', methods=['GET', 'POST'])
@is_logged_in_as_admin
def access(id):
    form = AccessForm(request.form)
    form.work_packages.choices = table_list('Work_Packages', 'code')[1:]
    form.partners.choices = table_list('Partners', 'name')[1:]
    # Retrieve user DB entry:
    user = Users.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    # Retrieve all relevant entries in users2work_packages and users2partners:
    current_work_packages = psql_to_pandas(Users2Work_Packages.query.filter_by(
        username=user.username))['work_package'].tolist()
    current_partners = psql_to_pandas(Users2Partners.query.filter_by(
        username=user.username))['partner'].tolist()
    # If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        new_work_packages = form.work_packages.data
        new_partners = form.partners.data
        # Delete relevant rows from users2work_packages:
        wps_to_delete = list(set(current_work_packages) -
                             set(new_work_packages))
        for wp in wps_to_delete:
            db_row = Users2Work_Packages.query.filter_by(
                username=user.username, work_package=wp).first()
            psql_delete(db_row, flashMsg=False)
        # Add relevant rows to users2work_packages:
        wps_to_add = list(set(new_work_packages) - set(current_work_packages))
        for wp in wps_to_add:
            db_row = Users2Work_Packages(
                username=user.username, work_package=wp)
            psql_insert(db_row, flashMsg=False)
        # Delete relevant rows from users2partners:
        partners_to_delete = list(set(current_partners) - set(new_partners))
        for partner in partners_to_delete:
            db_row = Users2Partners.query.filter_by(
                username=user.username, partner=partner).first()
            psql_delete(db_row, flashMsg=False)
        # Add relevant rows to users2work_packages:
        partners_to_add = list(set(new_partners) - set(current_partners))
        for partner in partners_to_add:
            db_row = Users2Partners(username=user.username, partner=partner)
            psql_insert(db_row, flashMsg=False)
        # Return with success
        flash('Edits successful', 'success')
        return redirect(url_for('access', id=id))
    # Pre-populate form fields with existing data:
    form.username.render_kw = {'readonly': 'readonly'}
    form.username.data = user.username
    form.work_packages.data = current_work_packages
    form.partners.data = current_partners
    return render_template('access.html', form=form, id=id)


# Login
@app.route('/login', methods=["GET", "POST"])
def login():
    WP='none'
    Ps='none'
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password_candidate = request.form['password']
        # Check trainee accounts first:
        user = Users.query.filter_by(username=username).first()
        if user is not None:
            password = user.password
            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['admin'] = 'False'
                session['reader'] = 'False'
                user_wps = psql_to_pandas(Users2Work_Packages.query.filter_by(
                                          username=session['username'])
                                          )['work_package'].tolist()
                user_partners = psql_to_pandas(Users2Partners.query.filter_by(
                    username=session['username']))['partner'].tolist()
                if len(user_wps[:]) >= 1 and len(user_partners[:]) >=1:
                    session['usertype'] = 'both'
                    flash('You are now logged in as both WP Leader and Partner Leader', 'success')
                elif len(user_wps[:]) >= 1:
                    session['usertype'] = 'WPleader'
                    flash('You are now logged in as WP Leader', 'success')
                elif len(user_partners[:]) >= 1:
                    session['usertype'] = 'Partnerleader'
                    flash('You are now logged in as Partner Leader', 'success')
                else:
                    flash('You are now logged in', 'success')
                if 'admin' in user_partners[:]:
                    session['admin'] = 'True'
                    flash('You have admin privallages', 'success')
                if 'ViewAll' in user_partners[:]:
                    session['reader'] = 'True'
                    flash('You view all access', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
                return redirect(url_for('login'))
        # Finally check admin account:
        if username == 'admin':
            password = app.config['ADMIN_PWD']
            if password_candidate == password:
                # Passed
                session['logged_in'] = True
                session['username'] = 'admin'
                # session['usertype'] = 'admin'
                flash('You are now logged in as admin', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
                return redirect(url_for('login'))
        # Username not found:
        flash('Username not found', 'danger')
        return redirect(url_for('login'))
    if 'logged_in' in session:
        flash('Already logged in', 'warning')
        return redirect(url_for('index'))
    # Not yet logged in:
    return render_template('login.html', WP=WP, P=Ps)


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


# Change password
@app.route('/change-pwd', methods=["GET", "POST"])
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
    return render_template('change-pwd.html', form=form)


# ssl
@app.route('/.well-known/acme-challenge/0pQ9Y9nneRwz6xitl6qTxzdBRC38pHJYgw-ey0JMJgI')
def letsencrypt_check():
    return '0pQ9Y9nneRwz6xitl6qTxzdBRC38pHJYgw-ey0JMJgI.eo3R_jzJhz37owhBTH73qvPeAHxNjuWt8W-FQJOCpeg'


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 403 status explicitly
    return render_template('403.html'), 403


@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
