FROM python:3.7-alpine

ENV PATH /usr/local/bin:$PATH

RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev libxml2-dev libxslt-dev
RUN apk add jpeg-dev zlib-dev
RUN apk add nodejs npm

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN mv geckodriver /usr/bin/
RUN rm geckodriver-v0.24.0-linux64.tar.gz
RUN export PATH=$PATH:/usr/bin/

RUN wget https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN chmod +x chromedriver
RUN mv chromedriver /usr/bin/
RUN rm chromedriver_linux64.zip
RUN export PATH=$PATH:/usr/bin/


COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

ADD . /app
WORKDIR /app

EXPOSE 8000
CMD python3 manage.py runserver