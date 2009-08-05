#!/bin/bash
pg_dump --data-only --inserts --table=auth_user envirocon >default.sql #for survey_survey owner
pg_dump --data-only --table=auth_group_permissions envirocon >>default.sql
pg_dump --clean     --table=django_site envirocon >>default.sql
pg_dump --data-only --table=courseaffils_course envirocon >>default.sql
pg_dump --data-only --table=django_flatpage envirocon >>default.sql
pg_dump --data-only --table=django_flatpage_sites envirocon >>default.sql
pg_dump --data-only --table=survey_survey envirocon >>default.sql
pg_dump --data-only --table=survey_question envirocon >>default.sql
pg_dump --data-only --table=survey_choice envirocon >>default.sql

