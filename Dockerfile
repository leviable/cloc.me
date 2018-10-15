FROM python:alpine

WORKDIR /clocme

RUN apk add --no-cache git cloc

ENV LC_ALL C

COPY requirements.txt .

RUN pip install -U --no-cache pip setuptools && \
    pip install -U -r requirements.txt

COPY *.py ./
COPY tests/ ./tests
COPY tox.ini ./

RUN pip install -e  .

ENTRYPOINT ["clocme"]
