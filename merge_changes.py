"""
Bespoke example script for scenario of reverting accidental changes

take current snap shot of site and last night's backup
conda activate swift-pm
postgres -D ~/postgresdata/ &
heroku login
heroku pg:backups:capture --app swift-pm
heroku pg:backups:download --app swift-pm
heroku pg:backups:download a500 --app swift-pm
createdb SWIFTOLD
createdb SWIFTNEW
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $USER -d SWIFTNEW latest.dump
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $USER -d SWIFTOLD latest.dump.1
./dumpPSQL (edited to point to SWIFTOLD or SWIFTNEW)
"""

import pandas as pd
current = pd.read_csv('current_csv/tasks.csv')
old = pd.read_csv('yesterday_csv/tasks.csv')
additions = current.loc[current['date_edited'] == '2020-02-12']
fix = old.copy()
for row in additions.itertuples():
    try:
        fix.loc[fix.id == row.id] = additions.loc[additions.id == row.id].values
    except SyntaxError:
        fix = fix.append(additions.loc[additions.id == row.id])
#fix = fix.fillna(0)
#fix.percent = fix.percent.astype(int)
fix = fix.drop(['id'], axis=1)
fix.to_csv('tasks.tab', sep='\t', index=False, header=False)
