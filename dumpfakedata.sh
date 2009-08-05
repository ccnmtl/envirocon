#!/bin/bash
pg_dump --data-only \
    --table=auth_user \
    --table=auth_group \
    --table=auth_user_groups \
    --table=courseaffils_course \
    --table=survey_answer \
    --table=teams_team \
    envirocon 
