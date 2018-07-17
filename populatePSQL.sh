psql SWIFTDB <<EOF

-- Delete current data (in reverse order of foreign key relationships);
DELETE FROM deliverables;
DELETE FROM partners;
DELETE FROM work_packages;

-- Copy new data (in normal order);
\copy partners(name,country,role) FROM './partners.tsv';
\copy work_packages(code,name) FROM './work_packages.tsv';
\copy deliverables(code,work_package,description,responsible_partner,month_due,progress,percent) FROM './deliverables.tsv' WITH NULL AS '';
EOF
