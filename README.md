# SWIFTDB
Repository for the AfricanSWIFT Project Management Tool

## To create copy of databse in MS Access:
1. Run script dumpPSQL.sh ($ bash dumpPSQL.sh) to dump data from
   the postgresql database tables into csv files
2. Make a copy of the MS Access database file:
   $ cp SWIFTDB_template.accdb SWIFTDB.accdb
3. Fire up Windows using rdesktop (on foe-linux) and open MS Access
   and open the file SWIFTDB.accdb
4. Click 'External Data -> Saved Imports' from the ribbon and click
   'Run' on each of the items in the Saved Imports list in turn.
   You may have to alter the paths to your csv files.
5. Save the database file, which should now include populated tables
