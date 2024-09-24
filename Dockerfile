FROM python:3.12-slim

RUN mkdir /biliard-pos

WORKDIR /bilard-pos

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV NAME .env-non-dev

CMD gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000