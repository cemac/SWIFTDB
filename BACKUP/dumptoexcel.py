#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dumptoexcel.py
.. module:: S_Box
    :platform: Unix (reccomended)
    :synopis:
.. moduleauther: CEMAC (UoL)
.. description: This module was developed by CEMAC as part of the GCRF African
   Swift Project. Currently hardcoded.
   :copyright: © 2019 University of Leeds.
   :license: MIT.
Example:
    To use::
        python dumptoexcel.py
.. CEMAC_SWIFTDB:
   https://github.com/cemac/SWIFTDB
"""

import pandas as pd
from dateutil.parser import parse
import argparse

# READ IN COMMAND LINE ARGUMENTS

parser = argparse.ArgumentParser(description="Dump heroku backup to excel")
parser.add_argument("date", help="Date string, format YYYYMMDD", type=str)
args = parser.parse_args()
date = args.date
#####

# Remove not allowed characters

df1 = pd.read_csv('csvs/' + str(date) + '/deliverables.csv')
df2 = pd.read_csv('csvs/' + str(date) + '/partners.csv')
df3 = pd.read_csv('csvs/' + str(date) + '/tasks.csv')
df4 = pd.read_csv('csvs/' + str(date) + '/users2partners.csv')
df5 = pd.read_csv('csvs/' + str(date) + '/users2work_packages.csv')
df6 = pd.read_csv('csvs/' + str(date) + '/work_packages.csv')


def cleandata(df):
    df = df.applymap(lambda x: x.encode('unicode_escape').decode(
        'utf-8') if isinstance(x, str) else x)
    return df


df1 = cleandata(df1)
df2 = cleandata(df2)
df3 = cleandata(df3)
df4 = cleandata(df4)
df5 = cleandata(df5)
df6 = cleandata(df6)


with pd.ExcelWriter('csvs/' + str(date) + 'swiftbak.xlsx') as writer:
    df1.to_excel(writer, sheet_name='deliverables')
    df2.to_excel(writer, sheet_name='partners')
    df3.to_excel(writer, sheet_name='tasks')
    df4.to_excel(writer, sheet_name='users2partners')
    df5.to_excel(writer, sheet_name='users2work_packages')
    df6.to_excel(writer, sheet_name='work_packages')
