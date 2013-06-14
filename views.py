# -*- coding: utf-8  -*-
from flask import Flask, url_for, render_template
from urllib import quote
import re
app = Flask(__name__)

reuser = re.compile(ur'[Uu]suário:([\w._!$@*]+)')

@app.route('/')
@app.route('/<page>')
def index(page=None):
    if page and page.lower().startswith(u'usuário'):
        import user
        pagehtml = 'user.html'
        username = reuser.search(page)
        title = u'Edições e direitos' + (username and u' de ' + username.group(1) or u'')
        variables = username and user.EditsAndRights(username.group(1)) or {}
    else:
        pagehtml, title, variables = 'mainpage.html', u'Ferramentas para projetos lusófonos', {}
    return render_template(pagehtml, title=title, **variables)

if __name__ == '__main__':
    app.debug = True
    from flup.server.fcgi_fork import WSGIServer
    WSGIServer(app).run()