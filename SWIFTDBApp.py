from flask import Flask, render_template, flash, redirect, url_for, request, g, session, abort
from wtforms import Form, validators, StringField
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

########## FORM CLASSES ##########
class PartnerForm(Form):
    name = StringField(u'Name',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. Leeds"})
    country = StringField(u'Country',
        render_kw={"placeholder": "e.g. UK"})
    role = StringField(u'Role',
        render_kw={"placeholder": "e.g. 'Academic' or 'Operational'"})

class WorkPackageForm(Form):
    wp_id = StringField(u'Work Package Code / ID',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. WP-C1"})
    name = StringField(u'Name',
        [validators.InputRequired()],
        render_kw={"placeholder": "e.g. Training"})
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
        max_id = Partners.query.order_by(Partners.partner_id.desc()).first().partner_id
        db_row = Partners(partner_id=max_id+1,name=name,country=country,role=role)
        psql_insert(db_row)
        #Return with success
        flash('Added to database', 'success')
        return redirect(url_for('add_partner'))
    return render_template('add-partner.html',form=form)

#View partners
@app.route('/view-partners')
def view_partners():
    partnersData = psql_to_pandas(Partners.query)
    return render_template('view-partners.html',partnersData=partnersData)

#Delete partner
@app.route('/delete-partner/<string:partner_id>', methods=['POST'])
def delete_partner(partner_id):
    db_row = Partners.query.filter_by(partner_id=partner_id).first()
    if db_row is None:
        abort(404)
    psql_delete(db_row)
    flash('Entry deleted', 'success')
    return redirect(url_for('view_partners'))

#Edit partner
@app.route('/edit-partner/<string:partner_id>', methods=['GET','POST'])
def edit_partner(partner_id):
    form = PartnerForm(request.form)
    db_row = Partners.query.filter_by(partner_id=partner_id).first()
    if db_row is None:
        abort(404)
    if request.method == 'POST' and form.validate():
        #Get form info:
        name = form.name.data
        country = form.country.data
        role = form.role.data
        #Update DB:
        db_row.name = name
        db_row.country = country
        db_row.role = role
        db.session.commit()
        #Return with success:
        flash('Edits successful', 'success')
        return redirect(url_for('view_partners'))
    form.name.data = db_row.name
    form.country.data = db_row.country
    form.role.data = db_row.role
    return render_template('edit-partner.html',form=form,partner_id=partner_id)


#Add work package
@app.route('/add-work-package', methods=["GET","POST"])
def add_work_package():
    form = WorkPackageForm(request.form)
    if request.method == 'POST' and form.validate():
        #Get form fields
        wp_id = form.wp_id.data
        name = form.name.data
        #Add to DB:
        db_row = Work_Packages(wp_id=wp_id,name=name)
        psql_insert(db_row)
        #Return with success
        flash('Added to database', 'success')
        return redirect(url_for('add_work_package'))
    return render_template('add-work-package.html',form=form)

#View work packages
@app.route('/view-work-packages')
def view_work_packages():
    wpData = psql_to_pandas(Work_Packages.query)
    return render_template('view-work-packages.html',wpData=wpData)

#Delete work package
@app.route('/delete-work-package/<string:wp_id>', methods=['POST'])
def delete_work_package(wp_id):
    db_row = Work_Packages.query.filter_by(wp_id=wp_id).first()
    if db_row is None:
        abort(404)
    psql_delete(db_row)
    flash('Entry deleted', 'success')
    return redirect(url_for('view_work_packages'))

#Edit work package
@app.route('/edit-work-package/<string:wp_id>', methods=['GET','POST'])
def edit_work_package(wp_id):
    form = WorkPackageForm(request.form)
    db_row = Work_Packages.query.filter_by(wp_id=wp_id).first()
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
    form.wp_id.render_kw = {'disabled': 'disabled'}
    form.wp_id.data = db_row.wp_id
    form.name.data = db_row.name
    return render_template('edit-work-package.html',form=form,wp_id=wp_id)


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
