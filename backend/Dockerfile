FROM python:3.10-slim-buster

WORKDIR /backend

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV FLIT_ROOT_INSTALL 1

RUN apt-get update -y

RUN pip install --upgrade pip
COPY ./pyproject.toml ./pyproject.toml
RUN pip install flit
COPY . /backend

RUN python -m flit install
