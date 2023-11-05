FROM python:3.10 as requirements-stage

WORKDIR /tmp

COPY ./requirements.txt /tmp/

FROM python:3.10

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
