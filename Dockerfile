
FROM python:3.9-slim

ENV PYTHONBUFFERED 1 
WORKDIR /app


COPY . /app/
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"],["python", "manage.py", "migrate"]

