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
CREATE TABLE staff(
  staff_id INTEGER PRIMARY KEY, 
  name TEXT,
  partner INTEGER,
  position TEXT,
  role TEXT,
  email TEXT,
  notes TEXT,
  FOREIGN KEY(partner) REFERENCES partners(partner_id)
  CONSTRAINT unique_partner_name UNIQUE (partner, name)
);
CREATE TABLE partner_leads(
  partner INTEGER PRIMARY KEY,
  lead INTEGER,
  FOREIGN KEY(partner) REFERENCES partners(partner_id),
  FOREIGN KEY(lead) REFERENCES staff(staff_id),
  CONSTRAINT unique_leads UNIQUE (partner, lead)
);
CREATE TABLE work_packages(
  wp_id TEXT PRIMARY KEY, 
  name TEXT,
  uk_leader INTEGER,
  africa_leader INTEGER,
  FOREIGN KEY(uk_leader) REFERENCES staff(staff_id),
  FOREIGN KEY(africa_leader) REFERENCES staff(staff_id)
);
CREATE TABLE deliverables(
  deliverable_id TEXT PRIMARY KEY,
  work_package TEXT
  description TEXT,
  responsible_partner INTEGER,
  month_due INTEGER,
  progress TEXT,
  percent INTEGER,
  FOREIGN KEY(work_package) REFERENCES work_packages(wp_id),
  FOREIGN KEY(responsible_partner) REFERENCES partners(partner_id)
);
CREATE TABLE tasks(
  task_id TEXT PRIMARY KEY,
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

if [ -f staff.tsv ]; then
sqlite3 SWIFT.db <<EOF
PRAGMA foreign_keys = ON;
.separator "\t"
.import staff.tsv staff
EOF
fi

if [ -f partner_leads.tsv ]; then
sqlite3 SWIFT.db <<EOF
PRAGMA foreign_keys = ON;
.separator "\t"
.import partner_leads.tsv partner_leads
EOF
fi

if [ -f work_packages.tsv ]; then
sqlite3 SWIFT.db <<EOF
CREATE TABLE temp AS SELECT * FROM work_packages WHERE 0;
PRAGMA foreign_keys = OFF;
.separator "\t"
.import work_packages.tsv temp
UPDATE temp SET africa_leader = NULL WHERE africa_leader = 'NULL';
PRAGMA foreign_keys = ON;
INSERT INTO work_packages SELECT * FROM temp;
DROP TABLE temp;
EOF
fi
