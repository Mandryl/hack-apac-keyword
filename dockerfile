FROM python:alpine

WORKDIR /app/hack-apac-keyword

COPY ../hack-apac-keyword /app

RUN pip install Flask
RUN pip install flask-cors
RUN pip install -r requirements.txt

CMD ["python", "api.py"]

