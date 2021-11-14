FROM python:alpine

WORKDIR /app

COPY ./app /app

RUN pip install Flask
RUN pip install -r requirements.txt

CMD ["python", "index.py"]