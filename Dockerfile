FROM python:3.9-slim
ENV APP_HOME /app 
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "2", "app:app"]