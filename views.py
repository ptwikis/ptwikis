#!/usr/bin/python
# -*- coding: utf-8  -*-

from flask import Flask, url_for, render_template, request, session, Response, jsonify
from urllib import quote
import re, os, requests, jwt, time, json
from requests_oauthlib import OAuth1

app = Flask(__name__)
app.debug = True

@app.route('/')
def index(page=None):
    return render_template('mainpage.html', title=u'Ferramentas para projetos lusófonos')

@app.route(u'/<path:page>')
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

@app.route('/login')
def login():
    with open('.oauth.key') as f:
        consumer_key, consumer_secret = f.read().rstrip('\n').split('\t')
    url = 'https://pt.wikipedia.org/w/index.php'
    if 'oauth_token' in request.args and 'oauth_verifier' in request.args:
        token, token_secret = session.get('token', '.').split('.')
        if not token or token != request.args['oauth_token']:
            with open('oauth.log', 'a') as f:
                f.write('%s\tErro: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'token desconhecido: %r' % token))
            return render_template('login.html', title='OAuth login', error=u'token desconhecido')
        del session['token']
        oauth = OAuth1(consumer_key, consumer_secret, token, token_secret, verifier=request.args['oauth_verifier'])
        r = requests.post(url=url, params={'title': 'Special:OAuth/token'}, auth=oauth)
        t = r.content.startswith('oauth_token') and dict(i.split('=', 1) for i in r.content.split('&'))
        oauth = OAuth1(consumer_key, consumer_secret, t['oauth_token'], t['oauth_token_secret'])
        r = requests.post(url=url, params={'title': 'Special:OAuth/identify'}, auth=oauth)
        data = jwt.decode(r.content, consumer_secret, audience=consumer_key)
        session.permanent = True
        session['user'] = data['username']
        with open('oauth.log', 'a') as f:
            f.write('%s\t%s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), data['username']))
        return render_template('login.html', title='OAuth login', user=data['username'])
    oauth = OAuth1(consumer_key, consumer_secret)
    r = requests.post(url=url, params={'title': 'Special:OAuth/initiate', 'oauth_callback': 'oob'}, auth=oauth)
    t = r.content.startswith('oauth_token') and dict(i.split('=', 1) for i in r.content.split('&'))
    if not t:
        with open('oauth.log', 'a') as f:
            f.write('%s\tErro: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), r.content))
        return render_template('login.html', title='OAuth login', error=r.content)
    session['token'] = '%(oauth_token)s.%(oauth_token_secret)s' % t
    authorize = url + '?title=Especial:OAuth/authorize&oauth_consumer_key=%s&oauth_token=%s' % (consumer_key,
            t['oauth_token'])
    if request.args.get('format') == 'json':
      resp = {'link': authorize, 'user': session.get('user', 'not logged')}
      if u'callback' in request.args:
        return Response(request.args[u'callback'] + '(%s)' % json.dumps(resp), mimetype='text/javascript')
      else:
        return jsonify(resp)
    return render_template('login.html', title='OAuth login', redirect=authorize, user=session.get('user'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', title=u'Página não encontrada', url=request.url), 404

if __name__ == '__main__':
    if os.uname()[1].startswith('tools-webgrid'):
        with open('.secret_key') as f:
            app.secret_key = f.read()
        app.config['APPLICATION_ROOT'] = '/ptwikis/'
        from flup.server.fcgi_fork import WSGIServer
        WSGIServer(app).run()
    else:
        # Roda a aplicação fora do Labs
        app.run()
