# -*- coding: utf-8 -*-

from flask import render_template_string
from threading import Thread
from urllib2 import urlopen
import json, re
from difflib import ndiff

page = u'''
{% extends "base.html" %}
{% block content %}
<p>Analise de pontuação de edição baseado na <a href="https://pt.wikipedia.org/wiki/Usu%C3%A1rio(a):Salebot/Config">configuração do Salebot</a>.</p>
<table style="margin: 4em auto 5em auto;">
  <tr>
    <td>Id da edição:</td>
    <td><input id="user" type="text" onkeypress="return enter(event, this, 'Salebot:')"/></td>
  </tr>
</table>
{% if rev %}
<p><a href="https://pt.wikipedia.org/wiki/Especial:Diff/{{ rev }}">Edição {{ rev }}</a></p>
<table class="wikitable">
  <tr><th>Pontos</th><th>Termo encontrado</th><th>Expressão regular</th><th>Comentários</th></tr>
{%- for points, match, regex, comment in rules %}
  <tr>
    <td style="font-size:20px; font-weight:bold; color:{% if points >= 0 %}#090">+{% else %}#900">{% endif %}{{ points }}</td>
    <td>{{ match }}</td>
    <td>{{ regex }}</td>
    <td>{{ comment }}</td>
  </tr>
{%- endfor %}
</table>
<p style="font-size:20px; font-weight:bold">Total de pontos: <span style="color:{% if totalpoints >= 0 %}#090">+{% else %}#900">{% endif %}{{ totalpoints }}</p>
<br/>
<h2>Linhas adicionadas</h2><hr/>
<p style="font-family:monospace; font-size:13px">{{ adlines }}</p>
{% endif %}
{% if aviso %}<p style="color:#520">{{ aviso }}</p>{% endif %}
{% endblock %}
'''

rules = []

def config():
    api = urlopen('https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=Usu%C3%A1rio:Salebot/Config&rvprop=content')
    text = json.loads(api.read())['query']['pages'].values()[0]['revisions'][0]['*']

    pre = False
    for line in text.split(u'\n'):
        ignorecase = False
        if not pre:
            if u'<pre>' in line:
                pre = True
            continue
        if line and line[0] in '+-':
            rule = re.search(ur'^([+-]\d+)[ \t]*/(.*)/[ \t]*(?:# *(.*))?$', line)
            if not rule:
                print u'erro em ' + line
                continue
            rules.append((int(rule.group(1)), re.compile(rule.group(2), re.I if ignorecase else 0), rule.group(3)))
        elif line == u'[ignore-case=1]':
            ignorecase = True
        elif u'</pre>' in line:
            pre = False

adlines = None

def diff(rev):
    global adlines    
    api = urlopen('https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&revids=%d&rvprop=content|ids' % int(rev))
    rev1 = json.loads(api.read())['query']['pages'].values()[0]['revisions'][0]
    if rev1.get('parentid'):
      api = urlopen('https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&revids=%d&rvprop=content' % rev1['parentid'])
      rev0 = json.loads(api.read())['query']['pages'].values()[0]['revisions'][0]
    else:
      rev0 = {'*': ''}
    diff = ndiff(rev0['*'].splitlines(), rev1['*'].splitlines())
    adlines = u'\n'.join(l[2:] for l in diff if l.startswith('+'))

def main(rev=None):
    if not rev or not rev.isdigit():
      return render_template_string(page, title=u'Pontuação de edição para o Salebot')
    df = Thread(target=diff, args=(rev,))
    df.start()
    config()
    df.join()
    total = 0
    r = []
    for rule in rules:
        match = rule[1].search(adlines)
        if match:
            r.append((rule[0], match.group(0), rule[1].pattern, rule[2]))
            total += rule[0]
    return render_template_string(page, title=u'Pontuação da edição %s para o Salebot' % rev, rev=rev,
        rules=r, totalpoints=total, adlines=adlines)
