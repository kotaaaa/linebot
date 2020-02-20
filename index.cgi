#!~/myenv/bin/python
from wsgiref.handlers import CGIHandler
from testFlask import app
CGIHandler().run(app)
