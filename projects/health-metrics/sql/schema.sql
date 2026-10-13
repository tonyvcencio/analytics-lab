--
-- PostgreSQL database dump
--

\restrict ChyMyPZJfmNHOWypymgOrrQe6KqfHzUdUx4sI3hPRDHDRfBWgMuEpM7Bi8zWwf0

-- Dumped from database version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: system_observations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.system_observations (
    observation_id bigint NOT NULL,
    timestamp_utc timestamp with time zone NOT NULL,
    hostname text NOT NULL,
    cpu_percent double precision,
    memory_used_mb double precision,
    memory_available_mb double precision,
    disk_used_percent double precision,
    uptime_seconds bigint,
    CONSTRAINT valid_cpu_percent CHECK (((cpu_percent >= (0)::double precision) AND (cpu_percent <= (100)::double precision))),
    CONSTRAINT valid_disk_percent CHECK (((disk_used_percent >= (0)::double precision) AND (disk_used_percent <= (100)::double precision))),
    CONSTRAINT valid_uptime CHECK ((uptime_seconds >= 0))
);


--
-- Name: system_observations_observation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.system_observations ALTER COLUMN observation_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.system_observations_observation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: system_observations system_observations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_observations
    ADD CONSTRAINT system_observations_pkey PRIMARY KEY (observation_id);


--
-- Name: system_observations unique_host_timestamp; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_observations
    ADD CONSTRAINT unique_host_timestamp UNIQUE (hostname, timestamp_utc);


--
-- PostgreSQL database dump complete
--

\unrestrict ChyMyPZJfmNHOWypymgOrrQe6KqfHzUdUx4sI3hPRDHDRfBWgMuEpM7Bi8zWwf0

