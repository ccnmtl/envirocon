--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('auth_user_id_seq', 12, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: sky
--

INSERT INTO auth_user VALUES (3, 'stud', '', '', '', 'sha1$72714$cae614e80f17de59c607d720e9cb0501bb0220e1', false, true, false, '2009-08-05 17:32:16.022917-04', '2009-08-05 16:33:25-04');
INSERT INTO auth_user VALUES (1, 'sky', '', '', 'hi@hi.com', 'sha1$dd6b8$7f6039da841ef979dc348528969a72b1acbe07e9', true, true, true, '2009-08-11 13:53:44.264455-04', '2009-08-11 13:52:08.983845-04');
INSERT INTO auth_user VALUES (6, 'rdk24', 'Ryan', 'Kelsey', 'rdk24@columbia.edu', '!', true, true, false, '2009-09-29 13:00:44.441282-04', '2009-09-29 13:00:44.347117-04');
INSERT INTO auth_user VALUES (8, 'pjs2153', 'Paul', 'Stengel', 'pjs2153@columbia.edu', '!', true, true, false, '2009-09-29 13:14:33.118397-04', '2009-09-29 13:14:33.04282-04');
INSERT INTO auth_user VALUES (9, 'dbeeby0', 'Daniel', 'Beeby', 'dbeeby0@columbia.edu', '!', true, true, false, '2009-09-29 13:23:16.60475-04', '2009-09-29 13:23:16.50154-04');
INSERT INTO auth_user VALUES (10, 'akq3', 'Ashlinn', 'Quinn', 'akq3@columbia.edu', '!', true, true, false, '2009-09-29 14:08:34.794937-04', '2009-09-29 14:02:32.849553-04');
INSERT INTO auth_user VALUES (11, 'mal85', '', '', '', 'sha1$cc46c$6a2e6548a58559fb8d4e105d7a4e6bbef6f18b36', false, true, false, '2009-09-29 17:07:00-04', '2009-09-29 17:07:00-04');
INSERT INTO auth_user VALUES (12, 'amf2145', '', '', '', 'sha1$c10a9$49b964a2c985a6c9bdf3ff4a7228f2a51c080079', false, true, false, '2009-09-29 17:07:29-04', '2009-09-29 17:07:29-04');
INSERT INTO auth_user VALUES (5, 'mj2402', 'Maria', 'Janelli', 'mj2402@columbia.edu', '!', true, true, false, '2009-09-29 15:07:45-04', '2009-09-29 12:43:54-04');
INSERT INTO auth_user VALUES (4, 'sbd12', 'Schuyler', 'Duveen', 'sbd12@columbia.edu', '!', true, true, true, '2009-09-29 16:09:54-04', '2009-08-11 13:54:15-04');
INSERT INTO auth_user VALUES (7, 'kmh2124', 'Kathryn', 'Hagan', 'kmh2124@columbia.edu', '!', true, true, true, '2009-09-29 13:06:10-04', '2009-09-29 13:06:10-04');


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('auth_group_id_seq', 42, true);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: sky
--

INSERT INTO auth_group VALUES (1, 'src.cunix.local:columbia.edu');
INSERT INTO auth_group VALUES (2, 'staff.cunix.local:columbia.edu');
INSERT INTO auth_group VALUES (3, 'tlc.cunix.local:columbia.edu');
INSERT INTO auth_group VALUES (4, 'tlcxml.cunix.local:columbia.edu');
INSERT INTO auth_group VALUES (5, 'ALL_CU');
INSERT INTO auth_group VALUES (6, 'test_faculty');
INSERT INTO auth_group VALUES (8, 't3.y2009.s001.cu8909.inaf.st.course:columbia.edu');
INSERT INTO auth_group VALUES (7, 't3.y2009.s001.cu8909.inaf.fc.course:columbia.edu');


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, true);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_pkey;
ALTER TABLE public.django_site ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.django_site_id_seq;
DROP TABLE public.django_site;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: sky; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO sky;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: sky
--

CREATE SEQUENCE django_site_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO sky;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sky
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('django_site_id_seq', 3, true);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: sky
--

ALTER TABLE django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: sky; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: courseaffils_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('courseaffils_course_id_seq', 3, true);


--
-- Data for Name: courseaffils_course; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY courseaffils_course (id, group_id, title, faculty_group_id) FROM stdin;
2	3	Test Course (CCNMTL)	4
3	8	Environment, Conflict, and Resolution Strategies	7
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: django_flatpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('django_flatpage_id_seq', 1, true);


--
-- Data for Name: django_flatpage; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY django_flatpage (id, url, title, content, enable_comments, template_name, registration_required) FROM stdin;
1	/asdf	Home page	This is to test whether we can make the home page with a flat page!	f		f
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: django_flatpage_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('django_flatpage_sites_id_seq', 6, true);


--
-- Data for Name: django_flatpage_sites; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY django_flatpage_sites (id, flatpage_id, site_id) FROM stdin;
6	1	1
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: survey_survey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('survey_survey_id_seq', 1, true);


--
-- Data for Name: survey_survey; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY survey_survey (id, title, slug, description, opens, closes, visible, public, restricted, allows_multiple_interviews, template_name, created_by_id, editable_by_id, recipient_type_id, recipient_id) FROM stdin;
1	Profile	profile	Fill out the questions, please.	2009-08-04 10:37:11-04	2009-12-31 09:37:20-05	t	f	t	f		1	1	17	3
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: survey_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('survey_question_id_seq', 11, true);


--
-- Data for Name: survey_question; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY survey_question (id, survey_id, qtype, required, text, "order", image, choice_num_min, choice_num_max, qstyle, _order) FROM stdin;
2	1	T	f	Other Program:	2		\N	\N		1
3	1	A	t	Please describe your previous academic experience and interests.	3		\N	\N		2
5	1	T	f	Other expertise	6		\N	\N		4
8	1	A	f	If yes please detail, Conflict resolution courses, natural resource management, development projects, or general project management etc.	75		\N	\N		7
6	1	R	t	Have you participated in previous training programs related to this course? 	70		1	1		5
9	1	A	f	If yes, please detail and note how much time.	90		\N	\N		8
10	1	R	t	Have you had any previous fieldwork in a post-conflict context or direct experiences in a conflict zone?	100		1	1		9
11	1	A	f	If yes please detail.	110		\N	\N		10
1	1	R	t	Please list your current *program* of study.	1		1	1		0
4	1	R	t	Please select the category that best describes your area of expertise.	5		\N	\N		3
7	1	R	t	Do you have professional experience focusing on areas that are relevant to the topics in this course and/or development, project management, or design?	80		1	1		6
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: survey_choice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('survey_choice_id_seq', 20, true);


--
-- Data for Name: survey_choice; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY survey_choice (id, question_id, text, image, "order", _order) FROM stdin;
9	1	Other		100	8
1	1	SIPA MIA EPS		1	0
2	1	SIPA MIA EPD		2	1
3	1	SIPA MIA IPS		3	2
4	1	SIPA MIA Other		4	3
5	1	MPA-ESP		5	4
6	1	Climate and Society		6	5
7	1	E3B		7	6
8	1	Teacher's College		8	7
10	4	environment resource management		1	0
11	4	conflict resolution/prevention		2	1
12	4	development		3	2
13	4	reconstruction		4	3
14	4	humanitarian aid/services		5	4
15	6	Yes		1	0
16	6	No		2	1
17	7	Yes		1	0
18	7	No		2	1
19	10	Yes		1	0
20	10	No		2	1
\.


--
-- PostgreSQL database dump complete
--

