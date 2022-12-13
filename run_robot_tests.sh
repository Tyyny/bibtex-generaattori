#!/bin/bash

SQLALCHEMY_DATABASE_URI=sqlite:///test.db poetry run python3 src/app.py &

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5000/)" != "200" ]];
  do sleep 1;
done

poetry run robot src/tests/
status=$?

find / -type f -print 2>/dev/null | grep references.bib

kill $(lsof -t -i:5000)
rm src/instance/test.db
exit $status
