FROM python:3.7-alpine

ENV PATH /usr/local/bin:$PATH

RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev libxml2-dev libxslt-dev
RUN apk add jpeg-dev zlib-dev
RUN apk add nodejs npm

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apk add wget xvfb unzip

# Set up the Chrome PPA

RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apk update
RUN apk add google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 77.0.3865.40
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

ADD . /app
WORKDIR /app

EXPOSE 8000
CMD python3 manage.py runserver