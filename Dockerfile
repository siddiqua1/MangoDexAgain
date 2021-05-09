FROM python:3.8.1

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV PROD=true

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python app.py"]