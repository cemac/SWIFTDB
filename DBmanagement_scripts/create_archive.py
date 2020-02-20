"""
Bespoke example script for creating archive
take current snap shot of site and last night's backup
"""

import pandas as pd
import glob

print('requires pandas 1.0.0')
# The current state of WPS,tasks,deliverables
workpackages = pd.read_csv('current/work_packages.csv')
tasks = pd.read_csv('current/tasks.csv')
deliverables = pd.read_csv('current/deliverables.csv')
workpackages = workpackages[['code', 'status', 'issues',
                            'next_deliverable', 'date_edited']]
tasks = tasks[['code', 'person_responsible', 'month_due', 'progress',
               'percent', 'papers', 'paper_submission_date', 'date_edited']]
deliverables = deliverables[['code', 'person_responsible', 'month_due', 'progress',
               'percent', 'papers', 'paper_submission_date', 'date_edited']]
# go back through backups
for wp in glob.iglob('../BACKUP/csvs/*/work_packages.csv'):
    wparchive = pd.read_csv(wp)
    try:
        wparchive = wparchive[['code', 'status', 'issues',
                               'next_deliverable', 'date_edited']]
    except KeyError:
        wparchive = wparchive[['code', 'status', 'issues',
                               'next_deliverable']]
        datestr = wp[15:-18]
        year = datestr[0:4]
        mnt = datestr[4:6]
        day = datestr[6::]
        wparchive['date_edited'] = str(year + '-' + mnt + '-' + day)
    workpackages = workpackages.append(wparchive)

workpackages = workpackages.set_index('date_edited')
workpackages = workpackages[workpackages.status.notnull()]
workpackages = workpackages.drop_duplicates(keep='last')
# remove 2019-03-22
