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
CREATE SEQUENCE deliverables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ONLY deliverables ALTER COLUMN id SET DEFAULT nextval('deliverables_id_seq'::regclass);
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
CREATE SEQUENCE tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ONLY tasks ALTER COLUMN id SET DEFAULT nextval('tasks_id_seq'::regclass);
alter table work_packages add column "previous_report" VARCHAR;
alter table work_packages add column "date_edited" DATE;
update work_packages SET date_edited = '01-12-2019';
update work_packages set previous_report = status;
update work_packages set status = '';
update deliverables SET date_edited = '01-12-2019';
update tasks SET date_edited = '01-12-2019';
update deliverables set progress = '';
update tasks set progress = '';
