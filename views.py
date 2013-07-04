# -*- coding: utf-8  -*-
from flask import Flask, url_for, render_template
from urllib import quote
import re, os

app = Flask(__name__)

@app.route('/')
def index(page=None):
    return render_template('mainpage.html', title=u'Ferramentas para projetos lusófonos')

@app.route(u'/Usuário:<username>')
def user(username=None):
    import user
    if username:
        username = username.replace(u'_', u' ')
    title = u'Edições e direitos' + (username and u' de ' + username or u'')
    variables = username and user.EditsAndRights(username) or {}
    return render_template('user.html', title=title, **variables)

@app.route(u'/Teste:<html>')
def teste(html=None):
  for f in os.listdir('/data/project/ptwikis/ptwikis/templates'):
   if f == html.lower() + u'.html':
    return render_template(html.lower() + '.html', title=u'Página de teste:' + html.replace(u'_', u' '))
  return render_template('page_not_found.html', title=u'Página não encontrada'), 404

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', title=u'Página não encontrada'), 404

if __name__ == '__main__':
    app.debug = True
    from flup.server.fcgi_fork import WSGIServer
    WSGIServer(app).run()
