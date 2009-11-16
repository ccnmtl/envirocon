#!/bin/bash
PROJECT_NAME=${PWD##*/}
DB_NAME=$PROJECT_NAME
ssh discostu.ccnmtl.columbia.edu pg_dump ${DB_NAME} >Prod.sql
dropdb ${DB_NAME};
createdb ${DB_NAME};
psql ${DB_NAME} <Prod.sql
