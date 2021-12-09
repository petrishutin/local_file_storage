FROM python:3.8.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./app .
COPY entrypoint.sh .
EXPOSE 8000
CMD ["/bin/sh","entrypoint.sh"]


