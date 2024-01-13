FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY /gamedi .

RUN python manage.py collectstatic

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "gamedi.wsgi"]
