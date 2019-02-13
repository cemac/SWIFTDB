#!/usr/bin/python
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

df1 = pd.read_csv('deliverables.csv')
df2 = pd.read_csv('partners.csv')
df3 = pd.read_csv('tasks.csv')
df4 = pd.read_csv('users2partners.csv')
df5 = pd.read_csv('users2work_packages.csv')
df6 = pd.read_csv('work_packages.csv')

with pd.ExcelWriter('swiftbak.xlsx') as writer:
    df1.to_excel(writer, sheet_name='deliverables')
    df2.to_excel(writer, sheet_name='partners')
    df3.to_excel(writer, sheet_name='tasks')
    df4.to_excel(writer, sheet_name='users2partners')
    df5.to_excel(writer, sheet_name='users2work_packages')
    df6.to_excel(writer, sheet_name='work_packages')
