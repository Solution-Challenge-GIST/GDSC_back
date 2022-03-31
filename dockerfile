FROM python:3.9.0

RUN apt update

WORKDIR /home/juchan015326/

RUN mkdir .virtualenvs

WORKDIR /home/juchan015326/.virtualenvs/

RUN pip install virtualenv

RUN virtualenv soridam

SHELL ["/bin/bash", "-c"]

RUN source soridam/bin/activate

SHELL ["/bin/sh", "-c"]

WORKDIR /home/ubuntu/SoriDam/

COPY ./ /home/ubuntu/SoriDam/

RUN pip install gunicorn

RUN pip install --upgrade google-api-python-client

RUN pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2

RUN pip install -r /home/ubuntu/SoriDam/requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && gunicorn -w 4 --env DJANGO_SETTINGS_MODULE=SoriDam.settings SoriDam.wsgi --bind 0.0.0.0:8000 --timeout=30"]
