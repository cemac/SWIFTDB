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
def wp_list():
    wp_DF = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    list = [('blank','--Please select--')]
    for wp in wp_DF['code']:
        list.append((wp,wp))
    return list

def partner_list():
    partner_DF = psql_to_pandas(Partners.query.order_by(Partners.id))
    list = [('blank','--Please select--')]
    for partner in partner_DF['name']:
        list.append((partner,partner))
    return list
#########################################

########## FORM CLASSES ##########
class PartnerForm(Form):
    name = StringField(u'*Partner Name',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. Leeds"})
    country = StringField(u'Country',
        render_kw={"placeholder": "e.g. UK"})
    role = StringField(u'Role',
        render_kw={"placeholder": "e.g. 'Academic' or 'Operational'"})

class WorkPackageForm(Form):
    code = StringField(u'*Work Package Code',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. WP-C1"})
    name = StringField(u'*Name',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. Training"})

class DeliverableForm(Form):
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

#Add partner
@app.route('/add-partner', methods=["GET","POST"])
def add_partner():
    form = PartnerForm(request.form)
    if request.method == 'POST' and form.validate():
        #Get form fields
        name = form.name.data
        country = form.country.data
        role = form.role.data
        #Add to DB:
        db_row = Partners(name=name,country=country,role=role)
        psql_insert(db_row)
        #Return with success
        flash('Added to database', 'success')
        return redirect(url_for('add_partner'))
    return render_template('add-partner.html',form=form)

#View partners
@app.route('/view-partners')
def view_partners():
    partnersData = psql_to_pandas(Partners.query.order_by(Partners.id))
    return render_template('view-partners.html',partnersData=partnersData)

#Delete partner
@app.route('/delete-partner/<string:name>', methods=['POST'])
def delete_partner(name):
    db_row = Partners.query.filter_by(name=name).first()
    if db_row is None:
        abort(404)
    psql_delete(db_row)
    flash('Entry deleted', 'success')
    return redirect(url_for('view_partners'))

#Edit partner
@app.route('/edit-partner/<string:name>', methods=['GET','POST'])
def edit_partner(name):
    form = PartnerForm(request.form)
    db_row = Partners.query.filter_by(name=name).first()
    if db_row is None:
        abort(404)
    if request.method == 'POST' and form.validate():
        #Get form info:
        country = form.country.data
        role = form.role.data
        #Update DB:
        db_row.country = country
        db_row.role = role
        db.session.commit()
        #Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('view_partners'))
    form.name.render_kw = {'readonly': 'readonly'}
    form.name.data = db_row.name
    form.country.data = db_row.country
    form.role.data = db_row.role
    return render_template('edit-partner.html',form=form,name=name)

#Add work package
@app.route('/add-work-package', methods=["GET","POST"])
def add_work_package():
    form = WorkPackageForm(request.form)
    if request.method == 'POST' and form.validate():
        #Get form fields
        code = form.code.data
        name = form.name.data
        #Add to DB:
        db_row = Work_Packages(code=code,name=name)
        psql_insert(db_row)
        #Return with success
        flash('Added to database', 'success')
        return redirect(url_for('add_work_package'))
    return render_template('add-work-package.html',form=form)

#View work packages
@app.route('/view-work-packages')
def view_work_packages():
    wpData = psql_to_pandas(Work_Packages.query.order_by(Work_Packages.id))
    return render_template('view-work-packages.html',wpData=wpData)

#Delete work package
@app.route('/delete-work-package/<string:code>', methods=['POST'])
def delete_work_package(code):
    db_row = Work_Packages.query.filter_by(code=code).first()
    if db_row is None:
        abort(404)
    psql_delete(db_row)
    flash('Entry deleted', 'success')
    return redirect(url_for('view_work_packages'))

#Edit work package
@app.route('/edit-work-package/<string:code>', methods=['GET','POST'])
def edit_work_package(code):
    form = WorkPackageForm(request.form)
    db_row = Work_Packages.query.filter_by(code=code).first()
    if db_row is None:
        abort(404)
    if request.method == 'POST' and form.validate():
        #Get form info:
        name = form.name.data
        #Update DB:
        db_row.name = name
        db.session.commit()
        #Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('view_work_packages'))
    form.code.render_kw = {'readonly': 'readonly'}
    form.code.data = db_row.code
    form.name.data = db_row.name
    return render_template('edit-work-package.html',form=form,code=code)

#Add deliverable
@app.route('/add-deliverable', methods=["GET","POST"])
def add_deliverable():
    form = DeliverableForm(request.form)
    form.work_package.choices = wp_list()
    form.responsible_partner.choices = partner_list()
    if request.method == 'POST' and form.validate():
        #Get form fields
        code = form.code.data
        work_package = form.work_package.data
        description = form.description.data
        responsible_partner = form.responsible_partner.data
        month_due=form.month_due.data
        progress = form.progress.data
        percent = form.percent.data
        #Add to DB:
        db_row = Deliverables(code=code,work_package=work_package,
          description=description,responsible_partner=responsible_partner,
          month_due=month_due,progress=progress,percent=percent)
        psql_insert(db_row)
        #Return with success
        flash('Added to database', 'success')
        return redirect(url_for('add_deliverable'))
    return render_template('add-deliverable.html',form=form)

#View deliverables
@app.route('/view-deliverables')
def view_deliverables():
    deliverablesData = psql_to_pandas(Deliverables.query.order_by(Deliverables.id))
    return render_template('view-deliverables.html',deliverablesData=deliverablesData)

#Delete deliverable
@app.route('/delete-deliverable/<string:code>', methods=['POST'])
def delete_deliverable(code):
    db_row = Deliverables.query.filter_by(code=code).first()
    if db_row is None:
        abort(404)
    psql_delete(db_row)
    flash('Entry deleted', 'success')
    return redirect(url_for('view_deliverables'))

#Edit deliverable
@app.route('/edit-deliverable/<string:code>', methods=['GET','POST'])
def edit_deliverable(code):
    form = DeliverableForm(request.form)
    form.work_package.choices = wp_list()
    form.responsible_partner.choices = partner_list()
    db_row = Deliverables.query.filter_by(code=code).first()
    if db_row is None:
        abort(404)
    if request.method == 'POST' and form.validate():
        #Get form info:
        work_package = form.work_package.data
        description = form.description.data
        responsible_partner = form.responsible_partner.data
        month_due=form.month_due.data
        progress = form.progress.data
        percent = form.percent.data
        #Update DB:
        db_row.work_package = work_package
        db_row.description = description
        db_row.responsible_partner = responsible_partner
        db_row.month_due = month_due
        db_row.progress = progress
        db_row.percent = percent
        db.session.commit()
        #Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('view_deliverables'))
    form.code.render_kw = {'readonly': 'readonly'}
    form.code.data = db_row.code
    form.work_package.data = db_row.work_package
    form.description.data = db_row.description
    form.responsible_partner.data = db_row.responsible_partner
    form.month_due.data = db_row.month_due
    form.progress.data = db_row.progress
    form.percent.data = db_row.percent
    return render_template('edit-deliverable.html',form=form,code=code)

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
