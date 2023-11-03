FROM python:3.9-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY /src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /src .

RUN python3 manage.py collectstatic
