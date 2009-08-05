--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: sky
--

INSERT INTO auth_user VALUES (1, 'sbd12', 'Schuyler', 'Duveen', 'sbd12@columbia.edu', '!', true, true, true, '2009-08-05 12:11:29.362848-04', '2009-08-05 12:08:33.701895-04');


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
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

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('django_site_id_seq', 2, true);


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: sky
--

INSERT INTO django_site VALUES (1, 'example.com', 'example.com');


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
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
1	/	Home page	This is to test whether we can make the home page with a flat page!	f		f
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: django_flatpage_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('django_flatpage_sites_id_seq', 2, true);


--
-- Data for Name: django_flatpage_sites; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY django_flatpage_sites (id, flatpage_id, site_id) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
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
1	Profile	profile	Fill out the questions, please.	2009-08-04 10:37:11-04	2009-08-31 10:37:20-04	t	f	t	f		1	1	17	1
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
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
1	1	R	t	Please list your current program of study.	1		1	1		0
3	1	A	t	Please describe your previous academic experience and interests.	3		\N	\N		2
4	1	C	t	Please check the box that best describes your area of expertise	5		\N	\N		3
5	1	T	f	Other expertise	6		\N	\N		4
8	1	A	f	If yes please detail, Conflict resolution courses, natural resource management, development projects, or general project management etc.	75		\N	\N		7
6	1	R	t	Have you participated in previous training programs related to this course? 	70		1	1		5
7	1	R	t	Do you have previous professional experience focusing specifically on positions that are relevant to the topics in this course and any development project management or design?	80		1	1		6
9	1	A	f	If yes, please detail and note how much time.	90		\N	\N		8
10	1	R	t	Have you had any previous fieldwork in a post-conflict context or direct experiences in a conflict zone?	100		1	1		9
11	1	A	f	If yes please detail.	110		\N	\N		10
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
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

