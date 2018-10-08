FROM python:alpine

WORKDIR /clocme

RUN apk add --no-cache git cloc

COPY requirements.txt .

RUN pip install -U --no-cache pip setuptools && \
    pip install -U -r requirements.txt tox

COPY *.py ./
COPY tests/ ./tests
COPY tox.ini ./

RUN pip install -e  .

ENTRYPOINT ["clocme"]
CMD ["--foo" ]
