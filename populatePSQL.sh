psql SWIFTDB <<EOF

-- Delete current data (in reverse order of foreign key relationships);
DELETE FROM deliverables;
DELETE FROM partners;
DELETE FROM work_packages;

-- Copy new data (in normal order);
\copy partners FROM './partners.tsv';
\copy work_packages FROM './work_packages.tsv';
\copy deliverables FROM './deliverables.tsv' WITH NULL AS '';
EOF