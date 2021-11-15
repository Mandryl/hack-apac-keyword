FROM registry.access.redhat.com/ubi8/python-39                                                                                                                           
  
COPY . /app
  
WORKDIR /app
  
RUN pip install Flask
RUN pip install -r requirements.txt
  
CMD ["python", "api.py"]
