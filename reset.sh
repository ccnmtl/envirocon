#!/bin/bash
dropdb envirocon
createdb envirocon
./manage.py syncdb
psql envirocon <default.sql
#psql envirocon <fake.sql
./manage.py loaddata fixture_game.json
./manage.py loaddata fixture_courseaffils.json
./manage.py loaddata fixture_statefulgame.json
