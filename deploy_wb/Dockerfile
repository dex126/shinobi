FROM python:3.13-slim

RUN apt-get update && apt-get install

WORKDIR /shinobi
COPY . .

RUN pip install poetry && \
    poetry config virtualenvs.create false && poetry install

ENTRYPOINT [ "sanic", "--host=0.0.0.0", "start_server:app" ]