# SWIFTDB
Repository for the AfricanSWIFT Project Management Tool

## To create copy of databse in MS Access:
1. Run script dumpPSQL.sh ($ bash dumpPSQL.sh) to dump data from
   the postgresql database tables into csv files
2. Make a copy of the MS Access database file:
   $ cp SWIFTDB_template.accdb SWIFTDB.accdb
3. Fire up Windows using rdesktop (on foe-linux) and open MS Access
   and open the file SWIFTDB.accdb
4. Click 'External Data -> Saved Imports' from the ribbon and click
   'Run' on each of the items in the Saved Imports list in turn.
   You may have to alter the paths to your csv files.
5. Save the database file, which should now include populated tables

## Requirements ##

* pip3
* pipenv
* autoenv
* python3
* python-libs
* Flaskr
* postgresql-10.4

# Installation

* `pipenv install --three`

## Usage ##

** fist use **
* initdb -D ~/postgresql_data/
* postgres -D ~/postgresql_data/ &
* assign:
```bash
  export  APP_SETTINGS='config.DevelopmentConfig'
  export SECRET_KEY='key'
  export ADMIN_PWD='psswd'
  export DATABASE_URL="postgresql://localhost/DBname"
```
* create database
```bash
createdb DBname
```
* populate with
```bash
python populatePSQL.py
python manage.py db upgrade
```
* run on localhost `python manage.py runserver`
