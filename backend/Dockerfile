FROM python:3.8-slim

RUN mkdir /food

COPY requirements.txt /food

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY backend/ /food

WORKDIR /food

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]