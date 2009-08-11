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
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('auth_group_id_seq', 19, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 19, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('auth_user_id_seq', 4, true);


--
-- Name: courseaffils_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('courseaffils_course_id_seq', 1, true);


--
-- Name: survey_answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('survey_answer_id_seq', 33, true);


--
-- Name: teams_team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sky
--

SELECT pg_catalog.setval('teams_team_id_seq', 5, true);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY auth_group (id, name) FROM stdin;
1	hi
2	
3	sky1
4	team1
5	asdf: team1
6	Team : asdf: team1
7	Team:  - asdf - team1
8	Team:  - asdf - team2
9	src.cunix.local:columbia.edu
10	staff.cunix.local:columbia.edu
11	tlc.cunix.local:columbia.edu
12	tlcxml.cunix.local:columbia.edu
13	ALL_CU
14	Team:  - asdf
18	Team 4:  - asdf
19	Team 5:  - asdf
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
3	stud				sha1$72714$cae614e80f17de59c607d720e9cb0501bb0220e1	f	t	f	2009-08-05 17:32:16.022917-04	2009-08-05 16:33:25-04
1	sky			hi@hi.com	sha1$dd6b8$7f6039da841ef979dc348528969a72b1acbe07e9	t	t	t	2009-08-11 13:53:44.264455-04	2009-08-11 13:52:08.983845-04
4	sbd12	Schuyler	Duveen	sbd12@columbia.edu	!	t	t	t	2009-08-11 13:54:15.147253-04	2009-08-11 13:54:15.097573-04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
13	4	10
14	4	11
15	4	12
16	4	13
19	4	7
\.


--
-- Data for Name: courseaffils_course; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY courseaffils_course (id, group_id, title, faculty_group_id) FROM stdin;
1	13	asdf	\N
\.


--
-- Data for Name: survey_answer; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY survey_answer (id, user_id, question_id, session_key, text, submission_date, interview_uuid) FROM stdin;
15	1	1	2fc3bf7e6734fbe2e48c3a1c195af43a	SIPA MIA EPS	2009-08-05 11:48:17.631793-04	307ed5f3ea6e4570b8dfa4947af077cb
16	1	3	2fc3bf7e6734fbe2e48c3a1c195af43a	CSa;lk jasdlkfjsdf	2009-08-05 11:48:17.632581-04	307ed5f3ea6e4570b8dfa4947af077cb
17	\N	4	2fc3bf7e6734fbe2e48c3a1c195af43a	conflict resolution/prevention	2009-08-05 11:48:17.632965-04	
18	\N	4	2fc3bf7e6734fbe2e48c3a1c195af43a	reconstruction	2009-08-05 11:48:17.633329-04	
19	1	6	2fc3bf7e6734fbe2e48c3a1c195af43a	Yes	2009-08-05 11:48:17.633708-04	307ed5f3ea6e4570b8dfa4947af077cb
20	1	8	2fc3bf7e6734fbe2e48c3a1c195af43a	CC	2009-08-05 11:48:17.634088-04	307ed5f3ea6e4570b8dfa4947af077cb
21	1	7	2fc3bf7e6734fbe2e48c3a1c195af43a	No	2009-08-05 11:48:17.634462-04	307ed5f3ea6e4570b8dfa4947af077cb
22	1	10	2fc3bf7e6734fbe2e48c3a1c195af43a	No	2009-08-05 11:48:17.634838-04	307ed5f3ea6e4570b8dfa4947af077cb
23	4	1	7745b416b8a62d1d8c4c4b419e1f0114	SIPA MIA EPS	2009-08-11 14:17:49.026525-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
24	4	2	7745b416b8a62d1d8c4c4b419e1f0114	goo	2009-08-11 14:17:49.02724-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
25	4	3	7745b416b8a62d1d8c4c4b419e1f0114	previous academic experience is the bomb	2009-08-11 14:17:49.027627-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
26	4	4	7745b416b8a62d1d8c4c4b419e1f0114	conflict resolution/prevention	2009-08-11 14:17:49.028004-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
27	4	4	7745b416b8a62d1d8c4c4b419e1f0114	reconstruction	2009-08-11 14:17:49.028377-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
28	4	5	7745b416b8a62d1d8c4c4b419e1f0114	opt	2009-08-11 14:17:49.028762-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
29	4	6	7745b416b8a62d1d8c4c4b419e1f0114	Yes	2009-08-11 14:17:49.029136-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
30	4	8	7745b416b8a62d1d8c4c4b419e1f0114	asdf	2009-08-11 14:17:49.029507-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
31	4	7	7745b416b8a62d1d8c4c4b419e1f0114	No	2009-08-11 14:17:49.029879-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
32	4	10	7745b416b8a62d1d8c4c4b419e1f0114	Yes	2009-08-11 14:17:49.030252-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
33	4	11	7745b416b8a62d1d8c4c4b419e1f0114	last text field here!	2009-08-11 14:17:49.030624-04	b1b32a5f60aa4af5b7d1bbf3cee928fe
\.


--
-- Data for Name: teams_team; Type: TABLE DATA; Schema: public; Owner: sky
--

COPY teams_team (id, course_id, group_id, name, _order) FROM stdin;
1	1	7	team1	0
2	1	8	team2	1
3	1	14		2
4	1	18		3
5	1	19		4
\.


--
-- PostgreSQL database dump complete
--

