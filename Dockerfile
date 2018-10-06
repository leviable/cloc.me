FROM python:alpine

WORKDIR /app

RUN apk add --no-cache git cloc

ENTRYPOINT ["python"]
CMD ["--version"]
