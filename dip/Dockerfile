FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/

RUN pip install -r requirements.txt

CMD python manage.py migrate \
    && python manage.py createcachetable \
    && gunicorn -b 0.0.0.0:8000 dip.wsgi:application
