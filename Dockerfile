FROM python:3.11

WORKDIR /hemli
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv sync -d

CMD pipenv run ./manage.py runserver 0.0.0.0:8000
EXPOSE 8000
