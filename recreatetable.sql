drop table deliverables;
drop table tasks;

CREATE TABLE deliverables (
    id integer PRIMARY KEY,
    code character varying NOT NULL,
    work_package character varying NOT NULL,
    description character varying NOT NULL,
    partner character varying NOT NULL,
    person_responsible character varying,
    month_due date NOT NULL,
    previous_report character varying,
    progress character varying,
    percent integer NOT NULL,
    papers character varying,
    paper_submission_date character varying,
    date_edited date
);


CREATE TABLE tasks (
    id integer PRIMARY KEY,
    code character varying NOT NULL,
    work_package character varying NOT NULL,
    description character varying NOT NULL,
    partner character varying NOT NULL,
    person_responsible character varying,
    month_due date NOT NULL,
    previous_report character varying,
    progress character varying,
    percent integer NOT NULL,
    papers character varying,
    paper_submission_date character varying,
    date_edited date
);


alter table work_packages add column "previous_report" VARCHAR;
alter table work_packages add column "date_edited" DATE;
update deliverables SET date_edited = '01-12-2019';
update tasks SET date_edited = '01-12-2019';
update work_packages SET date_edited = '01-12-2019';
update work_packages set previous_report = status;
update work_packages set status = '';
update deliverables set progress = '';
update tasks set progress = '';
