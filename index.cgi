#!~/myenv/bin/python
print("Content-type: text/html\n")
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)
