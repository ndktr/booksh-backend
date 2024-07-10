From python:3.12.4-alpine

WORKDIR /app

RUN pip install --upgrade pip && pip install Flask

CMD ["flask", "--app", "booksh", "run", "--host=0.0.0.0"]