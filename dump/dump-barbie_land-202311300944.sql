--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4 (Homebrew)
-- Dumped by pg_dump version 15.4 (Homebrew)

-- Started on 2023-11-30 09:44:44 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE barbie_land;
--
-- TOC entry 3640 (class 1262 OID 24968)
-- Name: barbie_land; Type: DATABASE; Schema: -; Owner: bair
--

CREATE DATABASE barbie_land WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';


ALTER DATABASE barbie_land OWNER TO bair;

\connect barbie_land

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3641 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 219 (class 1259 OID 33225)
-- Name: atm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.atm (
    atm_id integer NOT NULL,
    location_name character varying(100),
    latitude numeric(9,6),
    longitude numeric(9,6),
    address character varying(255),
    city character varying(100),
    state character varying(50),
    country character varying(50),
    is_operational boolean,
    last_service_date date
);


ALTER TABLE public.atm OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 33224)
-- Name: atm_atm_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.atm_atm_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.atm_atm_id_seq OWNER TO postgres;

--
-- TOC entry 3642 (class 0 OID 0)
-- Dependencies: 218
-- Name: atm_atm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.atm_atm_id_seq OWNED BY public.atm.atm_id;


--
-- TOC entry 215 (class 1259 OID 24979)
-- Name: atm_statistics; Type: TABLE; Schema: public; Owner: bair
--

CREATE TABLE public.atm_statistics (
    stats_id integer NOT NULL,
    atm_id integer,
    transaction_date date,
    total_transactions integer,
    successful_transactions integer,
    failed_transactions integer
);


ALTER TABLE public.atm_statistics OWNER TO bair;

--
-- TOC entry 214 (class 1259 OID 24978)
-- Name: atm_statistics_stats_id_seq; Type: SEQUENCE; Schema: public; Owner: bair
--

CREATE SEQUENCE public.atm_statistics_stats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.atm_statistics_stats_id_seq OWNER TO bair;

--
-- TOC entry 3643 (class 0 OID 0)
-- Dependencies: 214
-- Name: atm_statistics_stats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bair
--

ALTER SEQUENCE public.atm_statistics_stats_id_seq OWNED BY public.atm_statistics.stats_id;


--
-- TOC entry 220 (class 1259 OID 33233)
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    atm_id integer NOT NULL,
    latitude real,
    longitude real,
    address character varying(128)
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 33137)
-- Name: statistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.statistics (
    atm_id integer NOT NULL,
    services_per_day integer,
    amount_per_day real
);


ALTER TABLE public.statistics OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 33136)
-- Name: statistics_atm_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.statistics_atm_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_atm_id_seq OWNER TO postgres;

--
-- TOC entry 3644 (class 0 OID 0)
-- Dependencies: 216
-- Name: statistics_atm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.statistics_atm_id_seq OWNED BY public.statistics.atm_id;


--
-- TOC entry 3477 (class 2604 OID 33228)
-- Name: atm atm_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atm ALTER COLUMN atm_id SET DEFAULT nextval('public.atm_atm_id_seq'::regclass);


--
-- TOC entry 3475 (class 2604 OID 24982)
-- Name: atm_statistics stats_id; Type: DEFAULT; Schema: public; Owner: bair
--

ALTER TABLE ONLY public.atm_statistics ALTER COLUMN stats_id SET DEFAULT nextval('public.atm_statistics_stats_id_seq'::regclass);


--
-- TOC entry 3476 (class 2604 OID 33140)
-- Name: statistics atm_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics ALTER COLUMN atm_id SET DEFAULT nextval('public.statistics_atm_id_seq'::regclass);


--
-- TOC entry 3633 (class 0 OID 33225)
-- Dependencies: 219
-- Data for Name: atm; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.atm VALUES (1, 'Central Bank ATM', 55.755800, 37.617600, 'Tverskaya Street 12', 'Moscow', NULL, 'Russia', true, '2023-11-30');
INSERT INTO public.atm VALUES (2, 'Red Square ATM', 55.753900, 37.621600, 'Red Square 1', 'Moscow', NULL, 'Russia', true, '2023-11-29');
INSERT INTO public.atm VALUES (3, 'Arbat Street ATM', 55.748400, 37.594400, 'Arbat Street 24', 'Moscow', NULL, 'Russia', true, '2023-11-28');
INSERT INTO public.atm VALUES (4, 'GUM Department Store ATM', 55.755700, 37.617600, 'GUM Department Store, Red Square', 'Moscow', NULL, 'Russia', true, '2023-11-27');
INSERT INTO public.atm VALUES (5, 'Kremlin ATM', 55.751700, 37.617700, 'Kremlin Wall', 'Moscow', NULL, 'Russia', true, '2023-11-26');
INSERT INTO public.atm VALUES (6, 'Pushkin Museum ATM', 55.737200, 37.594500, 'Pushkin Museum of Fine Arts, Volkhonka Street 12', 'Moscow', NULL, 'Russia', true, '2023-11-25');
INSERT INTO public.atm VALUES (7, 'Luzhniki Stadium ATM', 55.715700, 37.553600, 'Luzhniki Stadium, Luzhnetskaya Embankment 24', 'Moscow', NULL, 'Russia', true, '2023-11-24');
INSERT INTO public.atm VALUES (8, 'VDNKh Park ATM', 55.830400, 37.626500, 'VDNKh Park, Prospekt Mira 119', 'Moscow', NULL, 'Russia', true, '2023-11-23');
INSERT INTO public.atm VALUES (9, 'Sparrow Hills ATM', 55.703700, 37.530200, 'Sparrow Hills, Vorobyovy Gory', 'Moscow', NULL, 'Russia', true, '2023-11-22');
INSERT INTO public.atm VALUES (10, 'Tretyakov Gallery ATM', 55.741700, 37.620400, 'Tretyakov Gallery, Lavrushinsky Lane 10', 'Moscow', NULL, 'Russia', true, '2023-11-21');


--
-- TOC entry 3629 (class 0 OID 24979)
-- Dependencies: 215
-- Data for Name: atm_statistics; Type: TABLE DATA; Schema: public; Owner: bair
--



--
-- TOC entry 3634 (class 0 OID 33233)
-- Dependencies: 220
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.locations VALUES (1, 55.7558, 37.6176, 'Tverskaya Street 12, Moscow');
INSERT INTO public.locations VALUES (2, 55.7539, 37.6216, 'Red Square 1, Moscow');
INSERT INTO public.locations VALUES (3, 55.7484, 37.5944, 'Arbat Street 24, Moscow');
INSERT INTO public.locations VALUES (4, 55.7557, 37.6176, 'GUM Department Store, Red Square, Moscow');
INSERT INTO public.locations VALUES (5, 55.7517, 37.6177, 'Kremlin Wall, Moscow');
INSERT INTO public.locations VALUES (6, 55.7372, 37.5945, 'Pushkin Museum of Fine Arts, Volkhonka Street 12, Moscow');
INSERT INTO public.locations VALUES (7, 55.7157, 37.5536, 'Luzhniki Stadium, Luzhnetskaya Embankment 24, Moscow');
INSERT INTO public.locations VALUES (8, 55.8304, 37.6265, 'VDNKh Park, Prospekt Mira 119, Moscow');
INSERT INTO public.locations VALUES (9, 55.7037, 37.5302, 'Sparrow Hills, Vorobyovy Gory, Moscow');
INSERT INTO public.locations VALUES (10, 55.7417, 37.6204, 'Tretyakov Gallery, Lavrushinsky Lane 10, Moscow');


--
-- TOC entry 3631 (class 0 OID 33137)
-- Dependencies: 217
-- Data for Name: statistics; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.statistics VALUES (1, 50, 1500.25);
INSERT INTO public.statistics VALUES (2, 30, 900.75);
INSERT INTO public.statistics VALUES (3, 20, 600.5);
INSERT INTO public.statistics VALUES (4, 40, 1200);
INSERT INTO public.statistics VALUES (5, 35, 1050.8);
INSERT INTO public.statistics VALUES (6, 25, 750.25);
INSERT INTO public.statistics VALUES (7, 45, 1350.5);
INSERT INTO public.statistics VALUES (8, 15, 450.75);
INSERT INTO public.statistics VALUES (10, 28, 840.3);
INSERT INTO public.statistics VALUES (9, 25, 1650);


--
-- TOC entry 3645 (class 0 OID 0)
-- Dependencies: 218
-- Name: atm_atm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.atm_atm_id_seq', 10, true);


--
-- TOC entry 3646 (class 0 OID 0)
-- Dependencies: 214
-- Name: atm_statistics_stats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bair
--

SELECT pg_catalog.setval('public.atm_statistics_stats_id_seq', 3, true);


--
-- TOC entry 3647 (class 0 OID 0)
-- Dependencies: 216
-- Name: statistics_atm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.statistics_atm_id_seq', 1, false);


--
-- TOC entry 3483 (class 2606 OID 33232)
-- Name: atm atm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atm
    ADD CONSTRAINT atm_pkey PRIMARY KEY (atm_id);


--
-- TOC entry 3479 (class 2606 OID 24984)
-- Name: atm_statistics atm_statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: bair
--

ALTER TABLE ONLY public.atm_statistics
    ADD CONSTRAINT atm_statistics_pkey PRIMARY KEY (stats_id);


--
-- TOC entry 3485 (class 2606 OID 33237)
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (atm_id);


--
-- TOC entry 3481 (class 2606 OID 33142)
-- Name: statistics statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_pkey PRIMARY KEY (atm_id);


-- Completed on 2023-11-30 09:44:44 MSK

--
-- PostgreSQL database dump complete
--

