FROM python:3.9.7
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV FLASK_APP=app
ENV FLASK_DEBUG=1
EXPOSE 5000
CMD ["uwsgi","--ini","/app/uwsgi.ini"]
