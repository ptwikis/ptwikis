# -*- coding: utf-8  -*-
from flask import Flask, url_for, render_template, request
from urllib import quote
import re, os
import database

app = Flask(__name__)

@app.route('/')
def index(page=None):
    return render_template('mainpage.html', title=u'Ferramentas para projetos lusófonos')

@app.route(u'/Usuário:<username>')
def user(username=None):
    if username:
        username = username.replace(u'_', u' ')
        title = u'Edições e direitos' + (username and u' de ' + username or u'')
        variables = username and database.EditsAndRights(username) or {}
        return render_template('user.html', title=title, **variables)
    else:
        return page_not_found(404)

@app.route(u'/Consulta')
@app.route(u'/Consulta:<query>')
def consulta(query=None):
    if query and hasattr(database, query) and  hasattr(eval('database.' + query), '__call__'):
        resp = eval('database.' + query + '()')
        
    else:
        return page_not_found(404)

@app.route(u'/<html>')
def htmlpage(html=None):
    if html + u'.html' in os.listdir(app.root_path + '/templates'):
        return render_template(html + '.html', title=html.replace(u'_', u' '))
    else:
        return page_not_found(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', title=u'Página não encontrada'), 404

if __name__ == '__main__':
    app.debug = True
    from flup.server.fcgi_fork import WSGIServer
    WSGIServer(app).run()