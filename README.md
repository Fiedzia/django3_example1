Usage:

Clone repository

edit routing.sql if you want change routes. This file is loaded when container is created.


docker build -t webapp1 .
docker run -p 8000:8000 webapp1


go to http://127.0.0.1:8000/route/?node_from=1&node_to=4


Notes:

1. This is basic example. No uwsgi, DEBUG=TRUE,
   data is loaded from database on each request to make testing easier

2. If you want to change routing while conainer is running, use docker exec
   and run sqlite3 db.sqlite3 to make your changes.


Assumptions:

Data is correct. Routes are not validated in any way.
Route exists


What I would change having more time:

Cache data in process so that we don't load it for each request
add visualisation
handle errors (route doesn't exist)
