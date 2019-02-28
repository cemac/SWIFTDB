# BACK UP DIRECTORY

## MANUAL

Download the database pg_restore locally and dump to csv

```bash
heroku pg:backups:download --app swift-pm
creatdb SWIFTBAK
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $USER -d SWIFTBAK latest.dump
../dumpPSQL.sh
```

dumpPSQL is currently hard coded for these specific tables to check available data:

```bash
psql SWIFTBAK
\dt
```
`ctrl+D` to exit psql command line

'dumptoexcel.py' hardcoded python tool to produce excel table quickly

# Automatic and generic tools

1. Generate a token to access heroku with out password

**NB: make sure .netrc file is only readable by you **
`heroku auth:token`

2. ./backup.sh
