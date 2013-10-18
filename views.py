# -*- coding: utf-8  -*-

import cgitb
cgitb.enable()

from flask import Flask, url_for, render_template, request
from urllib import quote
import re, os
import database

app = Flask(__name__)

@app.route('/')
def index(page=None):
    return render_template('mainpage.html', title=u'Ferramentas para projetos lusófonos')

@app.route(u'/<page>')
def htmlpage(page=None):
    page = page.split(':', 1)
    html = (page[0] + u'.html').encode('utf8')
    if html in os.listdir(app.root_path + '/templates'):
        return render_template(html, title=u':'.join(page).replace(u'_', u' '), **database.template(page[0], arg=len(page) > 1 and page[1] or None))
    else:
        return page_not_found(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', title=u'Página não encontrada'), 404

if __name__ == '__main__':
    from flup.server.fcgi_fork import WSGIServer
    WSGIServer(app).run()
    #app.debug = True; app.run()  # Utilize esta linha e comente as duas acima para rodar localmente
