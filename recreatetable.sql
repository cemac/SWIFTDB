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
