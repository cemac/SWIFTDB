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

file_name = 'tasks.tab'
# Read in tab deliminated file
deliverables = pd.read_csv(file_name, sep='\t')
# Merges cells give NaNs so drop them
df = deliverables.dropna()
# In the format Jan 2018 Month XX
# Extract XX part
month = df['Planned Completion'].str[-10::].str.extract('(\d+)')
# Replace column
df['Planned Completion'] = month
# FUTURE WARNING:
'''
FutureWarning: currently extract(expand=None) means expand=False
(return Index/Series/DataFrame) but in a future version of pandas
this will be changed to expand=True (return DataFrame)
'''
# Extract Percentage
Percent = df['Update August 2018'].str[0:4].str.extract('(\d+)')
# However Lorraine has used completed instead of 100%
Percent[df['Update August 2018'].str.contains('completed', flags=re.IGNORECASE,
                                              regex=True)] = 100
# She also has used phrase 'Final version recieved'
Percent[df['Update August 2018'].str.contains('Final version received',
                                              flags=re.IGNORECASE,
                                              regex=True)] = 100
# Add in Percent
df['Percent'] = Percent
# Rest are unknown so fill with zeros
df = df.fillna(0)
df['Percent'] = df['Percent'].astype(int)
# Save and overwrite removing index and header
df.to_csv(file_name, sep='\t', index=False, header=False)
