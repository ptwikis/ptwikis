# -*- coding: utf-8  -*-

from flask import Flask, url_for, render_template, request
from urllib import quote
import re, os

app = Flask(__name__)
app.debug = True

@app.route('/')
def index(page=None):
    return render_template('mainpage.html', title=u'Ferramentas para projetos lusófonos')

@app.route(u'/<page>')
def htmlpage(page=None):
    page = page.split(':', 1)
    html = (page[0] + u'.html').encode('utf8')
    filename = (page[0] + u'.py').encode('utf-8')
    if filename in os.listdir(app.root_path + '/tools'):
      filename = app.root_path + '/tools/' + filename
      with open(filename, 'r') as f:
        source = f.read()
      tool = {}
      exec compile(source, filename, 'exec') in tool
      return len(page) == 1 and tool['main']() or tool['main'](page[1])
    elif html in os.listdir(app.root_path + '/templates'):
        import database #Depois que colocar as ferramentas que usam bd na pasta tools, não será mais necessácio chamar o database.py
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
