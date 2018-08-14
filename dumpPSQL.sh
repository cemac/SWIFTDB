: '
Run using:
$ bash dumpPSQL.sh

This will make a backup copy of the current SWIFT database.
Files created: [tableName].csv
Users table not dumped as contains (sha-encrypted) passwords
'

psql SWIFTDB <<EOF
\copy partners to 'partners.csv' csv header;
\copy work_packages to 'work_packages.csv' csv header;
\copy deliverables to 'deliverables.csv' csv header;
\copy users2work_packages to 'users2work_packages.csv' csv header;
EOF
