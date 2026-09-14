FROM python:3.12-slim-bookworm

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN pip install .