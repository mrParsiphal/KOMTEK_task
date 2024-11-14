FROM python:3.12


MAINTAINER MrParsiphal


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ="Europe/Moscow"


VOLUME ./refbooks/:/refbooks/

RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD cd refbooks
CMD python3 manage.py makemigrations
CMD python3 manage.py migrate
CMD cd ../
CMD gunicorn -b 0.0.0.0:8000 refbooks.refbooks.wsgi:application


EXPOSE 8000