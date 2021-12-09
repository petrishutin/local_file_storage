FROM python:3.8.10
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["/bin/sh","entrypoint.sh"]


