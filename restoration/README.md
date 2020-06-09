## Restoration Process

disaster recovery
take current snap shot of site and last night's backup
```bash
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

```
now run `./dumpPSQL.sh` (edited to point to SWIFTOLD or SWIFTNEW) to generate csvs.

`merge_changes.py` will create new tab files with missing data restored...

then update db as normal fromt the new tab files (ensure to remove relevant delete and add sections if only doing one table... )

```
python populatedb.py
python manage db upgrade
# check locally
git add .
git commit -am ':floppy_disk: restored'
heroku login
git push heroku hotfix:master
heroku run -a swift-pm python populatedb.py
heroku run -a swift-pm python manage.py db upgrade
```

**NB** is best to test in staging heroku first!
