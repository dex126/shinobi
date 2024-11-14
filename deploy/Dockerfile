FROM python:3.13-slim

RUN apt-get update && apt-get install -y iputils-ping

WORKDIR /shinobi
COPY . .

RUN pip install poetry && \
    poetry config virtualenvs.create false && poetry install

ENTRYPOINT [ "python3", "start.py" ]