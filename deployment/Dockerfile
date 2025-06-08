FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app/src/backend

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt
RUN pip install psycopg2-binary

COPY src /app/src
COPY src/backend/.env /app/src/backend/.env

ENV DJANGO_SETTINGS_MODULE=app.settings
ENV PYTHONPATH=/app/src/backend

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
