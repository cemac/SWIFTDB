<div align="center">
<a href="https://swift-pm.herokuapp.com/">
  <img src="https://github.com/cemac/SWIFTDB/blob/master/static/pageview.png"></a>
  <br>
</div>

 <h1> <center>SWIFT Project Management Database </center> </h1>

![GitHub release](https://img.shields.io/github/release/cemac/SWIFTDB.svg) ![GitHub](https://img.shields.io/github/license/cemac/SWIFTDB.svg) [![DOI](https://zenodo.org/badge/134688007.svg)](https://zenodo.org/badge/latestdoi/134688007) [![GitHub top language](https://img.shields.io/github/languages/top/cemac/SWIFTDB.svg)](https://github.com/cemac/SWIFTDB) [![GitHub issues](https://img.shields.io/github/issues/cemac/SWIFTDB.svg)](https://github.com/cemac/SWIFTDB/issues) [![GitHub last commit](https://img.shields.io/github/last-commit/cemac/SWIFTDB.svg)](https://github.com/cemac/SWIFTDB/commits/master) [![GitHub All Releases](https://img.shields.io/github/downloads/cemac/SWIFTDB/total.svg)](https://github.com/cemac/SWIFTDB/releases)
[![HitCount](http://hits.dwyl.com/{cemac}/{SWIFTDB}.svg)](http://hits.dwyl.com/{cemac}/{SWIFTDB})

Repository for the [AfricanSWIFT](https://africanswift.org/) Project Management Tool [(swift-pm)](https://swift-pm.herokuapp.com/). A web app that hosts an editable database for the project Management of African SWIFT.

See [wiki](https://github.com/cemac/SWIFTDB/wiki) for user guide.

## Requirements

### Via anaconda

- [anaconda (python3)](https://www.anaconda.com/download/)
- [heroku cli](https://devcenter.heroku.com/articles/heroku-cli)

_Individual python modules are managed in the pip lock file and installed as per installation instructions_

### Pip

-   pip3 >= 18.0
-   pipenv
-   autoenv
-   python3
-   python-libs
-   Flaskr
-   postgresql-10.4

# Installation

-   `pipenv install --three`
- there after `pipenv shell`

**or**

-   `conda env create -f swift.yaml`
-   `conda activate swift` and thereafter to use

<hr>

## Usage

**first use**

-   `initdb -D ~/postgresql_data/`
-   `postgres -D ~/postgresql_data/ &`
-   assign:

```bash
  export  APP_SETTINGS='config.DevelopmentConfig'
  export SECRET_KEY='key'
  export ADMIN_PWD='chosen password'
  export DATABASE_URL="postgresql://localhost/DBname"
```

-   create database

```bash
createdb DBname
```

-   populate with

```bash
python populatePSQL.py
python manage.py db upgrade
```

-   run on localhost `python manage.py runserver`

**thereafter**

-   `pipenv shell` or `conda activate swift`
-   `postgres -D ~/postgresql_data/ &`
-   assign:

```bash
  export  APP_SETTINGS='config.DevelopmentConfig'
  export SECRET_KEY='key'
  export ADMIN_PWD='chosen password'
  export DATABASE_URL="postgresql://localhost/DBname"
```

-   run on localhost `python manage.py runserver`

<hr>

## Hosting

This app is currently hosted on [herokuapp](https://www.heroku.com/).

For example push changes and launch the app:

```bash
heroku login
git config heroku.remote heroku
git add -A
git commit -a -m'commit messgae'
git push heroku master
heroku run  -a swift-pm python manage.py db upgrade
```

or to populate the database:

```bash
heroku config:set DATABASE_URL="postgresql://localhost/DBNAME"
heroku run -a swift-pm python populatePSQL.py
```

<hr>

# Backups

For the SWIFT-pm app backups are scheduled daily at 00:00 (GMT) via

```bash
heroku pg:backups:schedule --at '00:00 Europe/London' --app <app name>
```

These are retained for 7 days with one weekly backup stored for one week.

To obtain a local copy to merge or manipulate or put to MS Access:

```bash
createdb myapp_devel  # start with an empty database
heroku run 'pg_dump -xO $DATABASE_URL' --app <app name> | psql myapp_devel
```

## To create copy of database in MS Access:

1.  Run script dumpPSQL.sh ($ bash dumpPSQL.sh) to dump data from
    the postgresql database tables into csv files
2.  Make a copy of the MS Access database file:
    $ cp SWIFTDB_template.accdb SWIFTDB.accdb
3.  Fire up Windows using rdesktop (on foe-linux) and open MS Access
    and open the file SWIFTDB.accdb
4.  Click 'External Data -> Saved Imports' from the ribbon and click
    'Run' on each of the items in the Saved Imports list in turn.
    You may have to alter the paths to your csv files.
5.  Save the database file, which should now include populated tables

## Alternatives:

```
# Create a public url
heroku pg:backups:url --app sushi | cat
# Download latest dump
heroku pg:backups:download
```
<hr>

# Web Page

Information on the web page template.

## Flask

The web app is built using python flask and thus the html file must adhere to the flask formatting rules. Each page builds on layout.html.

## Styling

The styling for this webpage uses [BOOTSTRAP](https://getbootstrap.com/docs/3.3/)

### Custom features:

To customise the bootstrap css a text css file is loaded in after the bootstrap library static/styles/stylesheet.css

1.  Navbar

-   An additional div container is added to the nav bar in order to allow interaction with a text/css
-   stylesheet.css then contains an update to navbar-default

2.  Tables

-   For admin the tables are very long added scrolling with sticky headers

## Scripting

The following javascript libraries are loaded:

-   [jquery](https://api.jquery.com/jquery.ajax/)
-   [bootstrap javascript](https://getbootstrap.com/docs/3.3/javascript/)
-   A script is added to view.html to add in a select all check checkbox
-   A script has been added to redirect to https

## Static

Here the custom style sheets and logos must be changed. If this system is to be used on another site the SWIFTlogo would need to be swapped and the colour coding (hex codes) in style sheet altered.
