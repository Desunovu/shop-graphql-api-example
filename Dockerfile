FROM python:3.10-alpine
MAINTAINER  'desunovu@gmail.com'

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./api /app/api
COPY ./migrations /app/migrations
COPY ./config.py /app/config.py
COPY ./runner.py /app/runner.py

COPY ./.env /app/.env

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["runner.py"]
