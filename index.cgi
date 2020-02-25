#!/home/kk1110/.local/share/virtualenvs/linebot-nxOg-56M/bin/python3.8
print("Content-Type: text/html\n\n")
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)
