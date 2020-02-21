#!/home/kk1110/.local/share/virtualenvs/linebot-nxOg-56M/bin/python3.8
# print("Content-type: text/html\n")
# print("hello world cgi")
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)
