--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5 (Homebrew)
-- Dumped by pg_dump version 15.5 (Homebrew)

-- Started on 2023-12-29 05:17:11 MSK

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
-- TOC entry 3624 (class 1262 OID 24968)
-- Name: barbie_land; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE barbie_land WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';


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
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- TOC entry 3625 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 42274)
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.locations (
    atm_id integer NOT NULL,
    latitude real,
    longitude real,
    address character varying(128)
);


--
-- TOC entry 214 (class 1259 OID 42273)
-- Name: locations1_atm_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.locations1_atm_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3626 (class 0 OID 0)
-- Dependencies: 214
-- Name: locations1_atm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.locations1_atm_id_seq OWNED BY public.locations.atm_id;


--
-- TOC entry 217 (class 1259 OID 42281)
-- Name: statistics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.statistics (
    statistics_id integer NOT NULL,
    atm_id integer,
    services_per_day integer,
    amount_per_day real,
    status character varying(128)
);


--
-- TOC entry 216 (class 1259 OID 42280)
-- Name: statistics1_statistics_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.statistics1_statistics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3627 (class 0 OID 0)
-- Dependencies: 216
-- Name: statistics1_statistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.statistics1_statistics_id_seq OWNED BY public.statistics.statistics_id;


--
-- TOC entry 3466 (class 2604 OID 42277)
-- Name: locations atm_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations ALTER COLUMN atm_id SET DEFAULT nextval('public.locations1_atm_id_seq'::regclass);


--
-- TOC entry 3467 (class 2604 OID 42284)
-- Name: statistics statistics_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.statistics ALTER COLUMN statistics_id SET DEFAULT nextval('public.statistics1_statistics_id_seq'::regclass);


--
-- TOC entry 3616 (class 0 OID 42274)
-- Dependencies: 215
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: -
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
INSERT INTO public.locations VALUES (11, 55.7667, 37.6251, 'Novy Arbat Street 22, Moscow');
INSERT INTO public.locations VALUES (12, 55.759, 37.6185, 'Bolshoi Theatre, Theatre Square 1, Moscow');
INSERT INTO public.locations VALUES (13, 55.7445, 37.6011, 'Patriarchs Ponds, Moscow');
INSERT INTO public.locations VALUES (14, 55.7724, 37.5917, 'Ostankino Tower, Moscow');
INSERT INTO public.locations VALUES (15, 55.781, 37.6209, 'Sokolniki Park, 1-Y Sokolnicheskiy Val 1, Moscow');


--
-- TOC entry 3618 (class 0 OID 42281)
-- Dependencies: 217
-- Data for Name: statistics; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.statistics VALUES (1, 1, 50, 1500.25, 'online');
INSERT INTO public.statistics VALUES (2, 2, 30, 900.75, 'online');
INSERT INTO public.statistics VALUES (3, 3, 20, 600.5, 'online');
INSERT INTO public.statistics VALUES (4, 4, 40, 1200, 'online');
INSERT INTO public.statistics VALUES (5, 5, 35, 1050.8, 'online');
INSERT INTO public.statistics VALUES (6, 6, 25, 750.25, 'online');
INSERT INTO public.statistics VALUES (7, 7, 45, 1350.5, 'online');
INSERT INTO public.statistics VALUES (8, 8, 15, 450.75, 'online');
INSERT INTO public.statistics VALUES (10, 9, 28, 840.3, 'online');
INSERT INTO public.statistics VALUES (9, 10, 25, 1650, 'online');


--
-- TOC entry 3628 (class 0 OID 0)
-- Dependencies: 214
-- Name: locations1_atm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.locations1_atm_id_seq', 1, false);


--
-- TOC entry 3629 (class 0 OID 0)
-- Dependencies: 216
-- Name: statistics1_statistics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.statistics1_statistics_id_seq', 1, false);


--
-- TOC entry 3469 (class 2606 OID 42279)
-- Name: locations locations1_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations1_pkey PRIMARY KEY (atm_id);


--
-- TOC entry 3471 (class 2606 OID 42286)
-- Name: statistics statistics1_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics1_pkey PRIMARY KEY (statistics_id);


--
-- TOC entry 3472 (class 2606 OID 42287)
-- Name: statistics statistics1_atm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics1_atm_id_fkey FOREIGN KEY (atm_id) REFERENCES public.locations(atm_id);


-- Completed on 2023-12-29 05:17:12 MSK

--
-- PostgreSQL database dump complete
--

