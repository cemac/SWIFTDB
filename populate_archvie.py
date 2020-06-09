"""
Run locally using:
$ python populatePSQL.py
Run on Heroku using:
$ heroku run python populatePSQL.py

Based off populatePSQL.py but adapted to leave partners and work_packages
intact

This will populate the database with initial data contained within the .tab
files, thus avoiding the administrator having to input all this data via
the web forms.

***NB***: Running this script will first clear the tables, including any
modifications that have been made to the data via the web app
(e.g. updates to the progress and percent fields).
"""

from SWIFTDBApp import db
from SWIFTDBApp import (Work_Packages_Archive, Deliverables_Archive,
                        Tasks_Archive, Counts)
import csv


def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("You did not enter one of 'y' or 'n'. Assumed 'n'.")


ans = yes_or_no("***WARNING***: Running this script will populate the database\
                with initial data contained within the .tab files. IT WILL \
                FIRST CLEAR THE TABLES, including any modifications that have \
                been made to the data via the web app (e.g. updates to the \
                progress and percent fields. Proceed?")

if(ans):
    # Delete current data (no ForeignKey relationships here):
    print("Deleting current data")
    Work_Packages_Archive.query.delete()
    db.session.commit()
    Tasks_Archive.query.delete()
    db.session.commit()
    Deliverables_Archive.query.delete()
    db.session.commit()
    Counts.query.delete()
    db.session.commit()

    # Copy new data (in normal order):
    print("Copying new data")
    list = [['wp_archive.tab', Work_Packages_Archive],
            ['deliverables_archive.tab', Deliverables_Archive],
            ['tasks_archive.tab', Tasks_Archive],
            ['counts.tab', Counts]]
    for l in list:
        with open(l[0], 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                db_row = l[1](*row)
                db.session.add(db_row)
                db.session.commit()

    print("***SUCCESS***")
