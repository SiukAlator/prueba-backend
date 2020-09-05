FROM python:3.6-alpine

EXPOSE 80
# Variable de entorno

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev
# RUN apk add py-mysqldb
COPY . ./django
WORKDIR ./
RUN pip install -r /django/requirements.txt
# RUN pip install django-bootstrap4
CMD python /django/manage.py runserver 0.0.0.0:80

