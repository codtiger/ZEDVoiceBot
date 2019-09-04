--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5
-- Dumped by pg_dump version 10.5

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100),
    voice_style text
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: voices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.voices (
    voice_id integer NOT NULL,
    owner_id integer NOT NULL,
    file_id text NOT NULL,
    tags text,
    voice_name text DEFAULT 'ZED'::text NOT NULL
);


--
-- Name: voices_owner_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.voices_owner_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: voices_owner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.voices_owner_id_seq OWNED BY public.voices.owner_id;


--
-- Name: voices_voice_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.voices_voice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: voices_voice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.voices_voice_id_seq OWNED BY public.voices.voice_id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: voices voice_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voices ALTER COLUMN voice_id SET DEFAULT nextval('public.voices_voice_id_seq'::regclass);


--
-- Name: voices owner_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voices ALTER COLUMN owner_id SET DEFAULT nextval('public.voices_owner_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, username, voice_style) FROM stdin;
1	KavehAranian	aggressively obnoxious, with beautifully placed points and dick in butt jokes,holds the record for the most iconic number of voices in ZED.
2	Farnood	the voice is often so nasal you wonder if you'll ever find the guy awake or in the mood to talk, talks a lot about his personal insecurities and self-aware identity crisis.
3	AmirHP	the ultimate cringe king,curses a lot,big fan of GOT,Real Madrid,David Beckham,etc.Dynamics is his biggest fear,big fan of that one-seated conservative Arzeshi woman,Babooshka-esque laugs(can't even describe,gotta listen)
4	Ahmad220	former member of Alcapoon,Javelin nose with great CS:GO skills,strangely loves one of his photos in which his head is poorly squeezed,started the \\"moody movie character profile picture with/without a quote\\" movement
5	AmirAliA2N	Drunk voice/video recording is only one of his professions,has a grandpa which is a bigger icon than him, showed his blessing to a vase by donating his urine,the first guy to actually confront Farnood for talking too much shit with a video
6	MiladCodisMyLife	holds the record for the most memed picture in one day,goes to beach with only two breads for 5 people,likes shooting people in the pit,big fan of ISIS before their dissolution,KeyDigital Mastermind
7	KasraMetallove	the nastiest boy in the group,former twitter megauser,weed lover,raids in WOW with Yaser and Ahmad,dont know why so obsessed with long voices(2 to 3 mins),KeyDigitals  second mastermind
8	Others	Other Voices, huge R.I.P to SoundMemesBot,you guys paved the way,Thanks you!
\.


--
-- Data for Name: voices; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.voices (voice_id, owner_id, file_id, tags, voice_name) FROM stdin;
4	1	AwADBAAD8QUAAk8EOVNppej-i7hPEgI	Zendaya	زندی یا مردی
5	3	AwADBAADKQYAAk1HiVP80aHt3jTlGgI	لطف ممنونم	خیلی لطف میکنی ممنونم
6	3	AwADBAADXwUAAvGvIFNufp9dpfqyCQI	دیوس عوضی آشغال کثافت GOT	اشغال کثافت غلیظ
7	3	AwADBAADKwYAAjsfkFGH6P8WbqrPRgI	برین ویس گیرآوردی	برین بریییییین
8	3	AwADBAADmQEAAhSzkFOO-WbCX-byzAI	تخم کفتر هفت صبح ده شب	تخم کفتر میخوری از صب تا شب
9	2	AwADBAADuQQAAgybsFMQ7t5eyY9bVQI	خودنگار آیتم فرنود	اقای خودنگار
10	8	AwADBAAD_wUAAqW--VNKvIev_T3QIwI	خایه مال سگ بگاد	خایه مال رو سگ بگاد
11	8	AwADAgADoAEAApm6gQmPVnUi10TwSAI	کیر کیرم به کیرم	به کیییییییییییییییییییییییرم
12	8	AwADAgADrgEAApm6gQm7Dy0gSklCOQI	وویس بهنام	وویس بهنام
13	6	AwADBAADSgEAAotJIFIstxE4fGAsUAI	خنده میلاد	خنده میلاد از ته دل
14	1	AwADBAADywUAArEX0VPCwVFkf7k4QwI	ضایع شدن poker	اهنگ موقع ضایع شدن
15	6	AwADBAADVgMAAmWq-FJkfcXcHoZodwI	صدا کس لیسی میلاد	صدای کس لیسی میلاد
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- Name: voices_owner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.voices_owner_id_seq', 1, false);


--
-- Name: voices_voice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.voices_voice_id_seq', 15, true);


--
-- Name: voices unique_voice_name; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voices
    ADD CONSTRAINT unique_voice_name UNIQUE (voice_name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: voices voices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voices
    ADD CONSTRAINT voices_pkey PRIMARY KEY (voice_id);


--
-- Name: voices voices_voice_path_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voices
    ADD CONSTRAINT voices_voice_path_key UNIQUE (file_id);


--
-- Name: voices voices_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.voices
    ADD CONSTRAINT voices_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

