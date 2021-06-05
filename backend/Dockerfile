# Docker is chosen to be able to package up all application files and resources into a conatiner.
# This means the application can be reproduced and used OS-independently.
# By evading much of the useless and heavy VM software, Docker allows apps to be lightweight,
# portable and versatile.

FROM python:3.8-slim-buster

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

# Install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt

COPY . /backend