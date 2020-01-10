--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: earhbu
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO earhbu;

--
-- Name: deliverables; Type: TABLE; Schema: public; Owner: earhbu
--

CREATE TABLE public.deliverables (
    id integer NOT NULL,
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


ALTER TABLE public.deliverables OWNER TO earhbu;

--
-- Name: partners; Type: TABLE; Schema: public; Owner: earhbu
--

CREATE TABLE public.partners (
    id integer NOT NULL,
    name character varying NOT NULL,
    country character varying,
    role character varying
);


ALTER TABLE public.partners OWNER TO earhbu;

--
-- Name: partners_id_seq; Type: SEQUENCE; Schema: public; Owner: earhbu
--

CREATE SEQUENCE public.partners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.partners_id_seq OWNER TO earhbu;

--
-- Name: partners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: earhbu
--

ALTER SEQUENCE public.partners_id_seq OWNED BY public.partners.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: earhbu
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
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


ALTER TABLE public.tasks OWNER TO earhbu;

--
-- Name: users; Type: TABLE; Schema: public; Owner: earhbu
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying,
    password character varying
);


ALTER TABLE public.users OWNER TO earhbu;

--
-- Name: users2partners; Type: TABLE; Schema: public; Owner: earhbu
--

CREATE TABLE public.users2partners (
    id integer NOT NULL,
    username character varying NOT NULL,
    partner character varying NOT NULL
);


ALTER TABLE public.users2partners OWNER TO earhbu;

--
-- Name: users2partners_id_seq; Type: SEQUENCE; Schema: public; Owner: earhbu
--

CREATE SEQUENCE public.users2partners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users2partners_id_seq OWNER TO earhbu;

--
-- Name: users2partners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: earhbu
--

ALTER SEQUENCE public.users2partners_id_seq OWNED BY public.users2partners.id;


--
-- Name: users2work_packages; Type: TABLE; Schema: public; Owner: earhbu
--

CREATE TABLE public.users2work_packages (
    id integer NOT NULL,
    username character varying NOT NULL,
    work_package character varying NOT NULL
);


ALTER TABLE public.users2work_packages OWNER TO earhbu;

--
-- Name: users2work_packages_id_seq; Type: SEQUENCE; Schema: public; Owner: earhbu
--

CREATE SEQUENCE public.users2work_packages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users2work_packages_id_seq OWNER TO earhbu;

--
-- Name: users2work_packages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: earhbu
--

ALTER SEQUENCE public.users2work_packages_id_seq OWNED BY public.users2work_packages.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: earhbu
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO earhbu;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: earhbu
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: work_packages; Type: TABLE; Schema: public; Owner: earhbu
--

CREATE TABLE public.work_packages (
    id integer NOT NULL,
    code character varying NOT NULL,
    name character varying NOT NULL,
    status character varying,
    issues character varying,
    next_deliverable character varying,
    previous_report character varying,
    date_edited date
);


ALTER TABLE public.work_packages OWNER TO earhbu;

--
-- Name: work_packages_id_seq; Type: SEQUENCE; Schema: public; Owner: earhbu
--

CREATE SEQUENCE public.work_packages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.work_packages_id_seq OWNER TO earhbu;

--
-- Name: work_packages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: earhbu
--

ALTER SEQUENCE public.work_packages_id_seq OWNED BY public.work_packages.id;


--
-- Name: partners id; Type: DEFAULT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.partners ALTER COLUMN id SET DEFAULT nextval('public.partners_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: users2partners id; Type: DEFAULT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2partners ALTER COLUMN id SET DEFAULT nextval('public.users2partners_id_seq'::regclass);


--
-- Name: users2work_packages id; Type: DEFAULT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2work_packages ALTER COLUMN id SET DEFAULT nextval('public.users2work_packages_id_seq'::regclass);


--
-- Name: work_packages id; Type: DEFAULT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.work_packages ALTER COLUMN id SET DEFAULT nextval('public.work_packages_id_seq'::regclass);


--
-- Name: users2partners _username_partner_uc; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2partners
    ADD CONSTRAINT _username_partner_uc UNIQUE (username, partner);


--
-- Name: users2work_packages _username_work_package_uc; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2work_packages
    ADD CONSTRAINT _username_work_package_uc UNIQUE (username, work_package);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: deliverables deliverables_pkey; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.deliverables
    ADD CONSTRAINT deliverables_pkey PRIMARY KEY (id);


--
-- Name: partners partners_name_key; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_name_key UNIQUE (name);


--
-- Name: partners partners_pkey; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: users2partners users2partners_pkey; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2partners
    ADD CONSTRAINT users2partners_pkey PRIMARY KEY (id);


--
-- Name: users2work_packages users2work_packages_pkey; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2work_packages
    ADD CONSTRAINT users2work_packages_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: work_packages work_packages_code_key; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.work_packages
    ADD CONSTRAINT work_packages_code_key UNIQUE (code);


--
-- Name: work_packages work_packages_pkey; Type: CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.work_packages
    ADD CONSTRAINT work_packages_pkey PRIMARY KEY (id);


--
-- Name: users2partners users2partners_partner_fkey; Type: FK CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2partners
    ADD CONSTRAINT users2partners_partner_fkey FOREIGN KEY (partner) REFERENCES public.partners(name);


--
-- Name: users2partners users2partners_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2partners
    ADD CONSTRAINT users2partners_username_fkey FOREIGN KEY (username) REFERENCES public.users(username);


--
-- Name: users2work_packages users2work_packages_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2work_packages
    ADD CONSTRAINT users2work_packages_username_fkey FOREIGN KEY (username) REFERENCES public.users(username);


--
-- Name: users2work_packages users2work_packages_work_package_fkey; Type: FK CONSTRAINT; Schema: public; Owner: earhbu
--

ALTER TABLE ONLY public.users2work_packages
    ADD CONSTRAINT users2work_packages_work_package_fkey FOREIGN KEY (work_package) REFERENCES public.work_packages(code);


--
-- PostgreSQL database dump complete
--

