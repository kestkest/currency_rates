FROM python:3.7-alpine
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8001

CMD [ "sh", "./entrypoint.sh" ]