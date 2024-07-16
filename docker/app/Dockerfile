From python:3.12.4-alpine

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY booksh /app/booksh

CMD ["flask", "--app", "booksh", "run", "--host=0.0.0.0"]
