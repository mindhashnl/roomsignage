FROM python:3.7-alpine


RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev libxml2-dev libxslt-dev
RUN apk add jpeg-dev zlib-dev
RUN apk add nodejs npm

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


ADD . /app
WORKDIR /app

EXPOSE 8000
CMD python3 manage.py runserver