FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN ./manage.py migrate
RUN apt-get update
RUN apt-get install sqlite3
RUN sqlite3 db.sqlite3 < routing.sql
EXPOSE 8000
CMD python3 /code/manage.py runserver 0.0.0.0:8000
