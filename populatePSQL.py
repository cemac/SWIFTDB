'''
This will populate the database with initial data contained within the .tab
files, thus avoiding the administrator having to input all this data via the
web forms.

***NB***: Running this script will first clear the tables, including any
modifications that have been made to the data via the web app
(e.g. updates to the progress and percent fields).
'''

from SWIFTDBApp import db
from SWIFTDBApp import Partners, Work_Packages, Deliverables, Users
from SWIFTDBApp import Users2Work_Packages, Tasks, Users2Partners
import csv


# Confim potential data deleation
def yes_or_no(question):
    reply = str(input(question + ' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("You did not enter one of 'y' or 'n'. Assumed 'n'.")


ans = yes_or_no(('***WARNING***: Running this script will populate the \
database with initial data contained within the .tab \
files. IT WILL FIRST CLEAR THE TABLES, including any \
modifications that have been made to the data via the web \
app (e.g. updates to the progress and percent fields. \
Proceed?'))

if(ans):
    # Delete current data (in reverse order of foreign key relationships):
    print("Deleting current data")
    Tasks.query.delete()
    db.session.commit()
    Users2Work_Packages.query.delete()
    db.session.commit()
    Deliverables.query.delete()
    db.session.commit()
    Partners.query.delete()
    db.session.commit()
    Work_Packages.query.delete()
    db.session.commit()

    # Copy new data (in normal order):
    print("Copying new data")
    list = [['partners.tab', Partners],
            ['work_packages.tab', Work_Packages],
            ['deliverables.tab', Deliverables],
            ['tasks.tab', Tasks]]
    for l in list:
        with open(l[0], 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                db_row = l[1](*row)
                db.session.add(db_row)
                db.session.commit()

    print("***SUCCESS***")
