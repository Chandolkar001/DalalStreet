FROM python:3.10-alpine
ENV PYTHONBUFFERED=1
WORKDIR /usr/src/wallstreet
COPY requirements.txt ./
RUN apk add --no-cache bash
RUN pip install -r requirements.txt