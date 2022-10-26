FROM python:3.10-alpine

WORKDIR /app
COPY . .

RUN pip install -r ./requirements.txt

CMD [ "python", "-m", "flask", "db", "upgrade"]

ENV FLASK_APP=api
ENTRYPOINT [ "python" ]
CMD [ "-m", "flask", "run", "--host=0.0.0.0"]
