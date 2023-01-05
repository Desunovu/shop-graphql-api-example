FROM python:3.10-alpine

WORKDIR /app
COPY . .

RUN pip install -r ./requirements.txt

ENV FLASK_APP=api
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]