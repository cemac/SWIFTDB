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

# Automatic

*coming soon*

 
