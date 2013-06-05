#! /usr/bin/python
# -*- coding: utf-8 -*-


from flask import Flask
from flask import render_template, request


app = Flask(__name__)
app.debug = True

@app.route('/')
def mainpage():
	return render_template('mainpage.html')

@app.route('/ola')
def ola():
	return u"ola"


if __name__ == '__main__':
	from flup.server.fcgi_fork import WSGIServer
	WSGIServer(app).run()
