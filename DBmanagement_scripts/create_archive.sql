drop table deliverables_archive;
drop table tasks_archive;

CREATE TABLE deliverables_archive (
    id integer PRIMARY KEY,
    date_edited date,
    code character varying NOT NULL,
    person_responsible character varying,
    progress character varying,
    percent integer,
    papers character varying,
    paper_submission_date character varying
);
CREATE SEQUENCE deliverables_archive_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY deliverables_archive ALTER COLUMN id SET DEFAULT nextval('deliverables_archive_id_seq'::regclass);

CREATE TABLE tasks_archive (
    id integer PRIMARY KEY,
    date_edited date,
    code character varying NOT NULL,
    person_responsible character varying,
    progress character varying,
    percent integer,
    papers character varying,
    paper_submission_date character varying
);

CREATE SEQUENCE tasks_archive_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY tasks_archive ALTER COLUMN id SET DEFAULT nextval('tasks_archive_id_seq'::regclass);

CREATE TABLE work_packages_archive (
    id integer PRIMARY KEY,
    date_edited date,
    code character varying NOT NULL,
    status character varying,
    issues character varying,
    next_deliverable character varying
);

CREATE SEQUENCE wp_archive_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY work_packages_archive ALTER COLUMN id SET DEFAULT nextval('wp_archive_id_seq'::regclass);


CREATE TABLE counts (
    id integer PRIMARY KEY,
    code character varying NOT NULL,
    count integer NOT NULL
);

CREATE SEQUENCE counts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY counts ALTER COLUMN id SET DEFAULT nextval('counts_id_seq'::regclass);
