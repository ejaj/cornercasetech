FROM python:3.9-alpine

RUN apk add \
  --no-cache \
  --upgrade \
  openssl \
  cargo \
  postgresql-client \
  libpq \
  postgresql-dev \
  zlib-dev jpeg-dev \
  gcc libffi-dev python3-dev \
  alpine-sdk

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN chmod a+x entrypoint.sh
RUN chmod a+x entrypoint.skip.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]