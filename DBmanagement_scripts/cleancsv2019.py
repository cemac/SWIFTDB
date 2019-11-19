'''
A script to take tab deliminated dump Lorraines excel work sheets and
tidy them up for postgres storage.

**Inprogess**

Known issues

Encoding with excel, python defaults to utf-8
excel uses something else, current fix is to resave
the file in atom!

Generalise:
Pass in file name and extract header names rather than hard code
'''
import pandas as pd
import re

file_name = 'deliverables.tab'
# Read in tab deliminated file
df = pd.read_csv(file_name, sep='\t')
# percents are Integer
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
df.to_csv(file_name, sep='\t', index=False, header=False)
file_name = 'tasks.tab'
# Read in tab deliminated file
df = pd.read_csv(file_name, sep='\t')
# percents are Integer
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
df.to_csv(file_name, sep='\t', index=False, header=False)
