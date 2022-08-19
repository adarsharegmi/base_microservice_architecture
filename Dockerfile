FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/user_service /src

WORKDIR /src/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]