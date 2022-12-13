#!/bin/bash

poetry run python3 src/app.py &

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5000/)" != "200" ]];
  do sleep 1;
done

poetry run robot src/tests/robottest.robot
poetry run robot src/tests/user_can_add_reference_type_book.robot
status=$?

kill $(lsof -t -i:5000)

exit $status
