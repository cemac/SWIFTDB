#!/bin/bash
#title          :backup.sh
#description    :A Script to automate the heroku back up to cloud excel sheets
#author         :CEMAC - Helen
#date           :20190228
#version        :0.1
#usage          :./backup.sh
#notes          :
#bash_version   :4.2.46(2)-release
#============================================================================

orig=${cwd}
cd $HOME/SWIFTDB2/BACKUP
source .env
if [ -e latest.dump ]
then
  mv latest.dump previous.dump
  echo 'WARNING OLD DUMP file found, renamed previous dump (just in case)'
fi
heroku pg:backups:download --app swift-pm
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $USER -d SWIFTBAK latest.dump
./dumpPSQL.sh
folder=csvs/$(date +%Y%m%d)
if [ ! -e $folder ]
then
  mkdir $folder
fi
./dumpPSQL.sh
mv *.csv $folder
python dumptoexcel.py $(date +%Y%m%d)
cp -p csvs/$(date +%Y%m%d)swiftbak.xlsx $HOME/public_html/SHARE/SWIFT/
cd $orig
