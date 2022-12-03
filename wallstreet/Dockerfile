FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
WORKDIR /app/api
COPY ./requirements.txt /app/api
RUN pip install --no-cache-dir --requirement /app/api/requirements.txt
COPY . /app/api
EXPOSE 8000
