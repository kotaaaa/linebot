#!/usr/local/bin/python
print "Content-type: text/html\n"
print "hello world cgi"
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)
