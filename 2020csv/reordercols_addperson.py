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
m2d['date'] = m2d['Month'].map(str) + m2d['hyphen'].map(str) + m2d['Year'].map(str)
m2d.date = pd.to_datetime(m2d.date, format='%B-%Y')
month_dic = m2d.to_dict()['date']
file_name = ['deliverables', 'tasks']
for f in file_name:
    df = pd.read_csv(f + '.csv')
    df.percent = df.percent.fillna(0).astype(int)
    # theres some trailing white spaces
    df.partner = df.partner.str.strip()
    # Partners need to match existing keys
    # make everything upper case
    df.partner = df.partner.apply(lambda x: x.upper())
    up = ['UOL', 'UOR', 'GMET', 'NIMET', 'UON']
    mixp = ['UoL', 'UoR', 'GMet', 'NiMet', 'UoN']
    for i, p in enumerate(up):
        df.partner = df.partner.replace(p, mixp[i])
    dfnew = pd.DataFrame()
    dfnew = df[['id', 'code', 'work_package',
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
