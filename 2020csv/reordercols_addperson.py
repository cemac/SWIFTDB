# -*- coding: utf-8 -*-
"""
.. module:: DBmanagement_scripts
    :platform: Unix
    :synopis:
.. moduleauther: CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the SWIFT
   Project. This is desinged to take existing tab files and add in new
   required columns.
   :copyright: © 2019 University of Leeds.
   :license: MIT.
Example:
    To use::
        python Addcomumns.py
.. CEMAC_SWIFTDB:
   https://github.com/cemac/SWIFTDB
"""
import pandas as pd

# Read in sql dump
m2d = pd.read_csv('month2date.tab')
m2d = m2d.set_index('No.')
m2d['hyphen'] = '-'
m2d['date'] = m2d['Month'].map(
    str) + m2d['hyphen'].map(str) + m2d['Year'].map(str)
m2d.date = pd.to_datetime(m2d.date, format='%B-%Y')
month_dic = m2d.to_dict()['date']
file_name = ['deliverables', 'tasks']
for f in file_name:
    dfcurrent = pd.read_csv(f + '_current.csv')
    dfcurrent['date_edited'] = '01-12-2019'
    dfcurrent['paper_submission_date'] = ''
    dfcurrent['person_responsible'] = ''
    dfcurrent['previous_report'] = dfcurrent['progress']
    dfnew = pd.DataFrame()
    dfnew = dfcurrent[['id', 'code', 'work_package',
                       'description',
                       'partner',
                       'person_responsible',
                       'month_due',
                       'previous_report',
                       'progress',
                       'percent',
                       'papers',
                       'paper_submission_date',
                       'date_edited']]
    month_due = dfnew.month_due
    month_due = month_due.replace(month_dic)
    dfnew['month_due'] = month_due
    # read in excel dump
    dfnov = pd.read_csv(f + '_nov.csv', sep='\t')
    # extract person person_responsible
    dfnov = dfnov[['code', 'person']].set_index('code')
    person_dict = dfnov.to_dict()['person']
    # add into
    code2person = dfnew['code']
    code2person = code2person.replace(person_dict)
    dfnew['person_responsible'] = code2person
    # save in headerless tab format
    dfnew.to_csv(f + '.tab', sep='\t', index=False, header=False)
