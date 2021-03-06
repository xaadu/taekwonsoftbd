FROM python:3.9.2
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

ENTRYPOINT [ "sh", "entrypoint.sh" ]
