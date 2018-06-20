#!/bin/bash
mv -f SWIFT.db SWIFT.db_old
sqlite3 SWIFT.db <<EOF
PRAGMA foreign_keys = ON;
CREATE TABLE partners(
  partner_id INTEGER PRIMARY KEY, 
  name TEXT UNIQUE,
  country TEXT,
  role TEXT
);
CREATE TABLE work_packages(
  wp_id TEXT PRIMARY KEY, 
  name TEXT
);
CREATE TABLE deliverables(
  deliverable_id TEXT PRIMARY KEY,
  work_package TEXT,
  description TEXT,
  responsible_partner INTEGER,
  month_due INTEGER,
  progress TEXT,
  percent INTEGER,
  FOREIGN KEY(work_package) REFERENCES work_packages(wp_id),
  FOREIGN KEY(responsible_partner) REFERENCES partners(partner_id)
);
CREATE TABLE tasks(
  task_id INTEGER PRIMARY KEY,
  description TEXT
);
CREATE TABLE tasks2deliverables(
  t2d_id INTEGER PRIMARY KEY,
  task TEXT,
  deliverable TEXT,
  FOREIGN KEY(task) REFERENCES tasks(task_id),
  FOREIGN KEY(deliverable) REFERENCES deliverables(deliverable_id),
  CONSTRAINT unique_t2d UNIQUE (task, deliverable)
);
CREATE TABLE partners2tasks_deliverables(
  p2td_id INTEGER PRIMARY KEY,
  partner INTEGER,
  task_or_deliverable BOOLEAN,
  task TEXT,
  deliverable TEXT,
  progress TEXT,
  percent INTEGER,
  FOREIGN KEY(partner) REFERENCES partners(partner_id),
  FOREIGN KEY(task) REFERENCES tasks(task_id),
  FOREIGN KEY(deliverable) REFERENCES deliverables(deliverable_id),
  CONSTRAINT unique_p2td UNIQUE (partner, task_or_deliverable, task, deliverable)
);
EOF

if [ -f partners.tsv ]; then
sqlite3 SWIFT.db <<EOF
PRAGMA foreign_keys = ON;
.separator "\t"
.import partners.tsv partners
EOF
fi

if [ -f work_packages.tsv ]; then
sqlite3 SWIFT.db <<EOF
PRAGMA foreign_keys = ON;
.separator "\t"
.import work_packages.tsv work_packages
EOF
fi

if [ -f deliverables.tsv ]; then
sqlite3 SWIFT.db <<EOF
CREATE TABLE temp AS SELECT * FROM deliverables WHERE 0;
PRAGMA foreign_keys = OFF;
.separator "\t"
.import deliverables.tsv temp
UPDATE temp SET responsible_partner = NULL WHERE responsible_partner = 'NULL';
PRAGMA foreign_keys = ON;
INSERT INTO deliverables SELECT * FROM temp;
DROP TABLE temp;
EOF
fi
