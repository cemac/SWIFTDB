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

# Update task tab to include WP link
file_name = 'tasks.tab'
df = pd.read_csv(file_name, sep='\t', names=['tasks', 'descriptions',
                                             'partner', 'month due',
                                             'progess', 'percent'])
# WP-X.Y from T-RX.Y.N.M
# Replace T with WP
wp = df['tasks'].str.replace('T', 'WP')
# Extract T-RX.Y
wp = df['tasks'].str[0:5]
# Add back in and Save
df['WPs'] = wp
df = df[['tasks', 'descriptions', 'partner', 'WP', 'month due',
                                             'progess', 'percent']]
df.to_csv(file_name, sep='\t', index=False, header=False)

# Update WP to include summary update
file_name = 'work_packages.tab'
df = pd.read_csv(file_name, sep='\t', names=['Code', 'Name'])
# Add new blank column
df['Status Update'] = ""
df.to_csv(file_name, sep='\t', index=False, header=False)
