FROM python:3.6-alpine
RUN apk update \
    && apk add sqlite gcc musl-dev python3-dev libffi-dev openssl-dev

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["flask", "db", "init"]
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]