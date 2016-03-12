# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn, link

page = u'''
{% extends "base.html" %}
{% block content %}
<p>Lista número de transclusões de predefinições que redirecionam para predefinições de uma categoria.</p>
<table style="margin: 4em auto 5em auto;">
  <tr>
    <td>Categoria:</td>
    <td><input id="user" type="text" onkeypress="return enter(event, this, 'Transclusões3:')"/></td>
  </tr>
</table>
{% if lista %}
<table class="wikitable">
  <tr><th>Predefinição</th><th>Transclusões</th><th>Redireciona para</th></tr>
{%- for page, num, redir in lista %}
  <tr>
    <td><a href="//{{ link }}.org/w/index.php?title={{ page|replace(" ", "_") }}&redirect=no">{{ page|replace('_', ' ') }}</a></td>
    <td><a href="//{{ link }}.org/w/index.php?title=Especial:P%C3%A1ginas_afluentes/{{ page|replace(' ', '_') }}&hidelinks=1&hideredirs=1">{{ num }}</a></td>
    <td><a href="//{{ link }}.org/wiki/{{ redir|replace(" ", "_") }}">{{ redir|replace('_', ' ') }}</a></td>
  </tr>
{%- endfor %}
</table>
{% endif %}
{% if aviso %}<p style="color:#520">{{ aviso }}</p>{% endif %}
{% endblock %}
'''

def main(cat=None):
  if cat:
    wiki = u'Wikipédia'
    c = conn(wiki)
    c.execute(u"""SELECT
 redir,
 COUNT(tl_from) marca,
 redireciona_para
 FROM (SELECT
   CONCAT(IF(r.page_namespace = 4, 'Wikipédia', 'Predefinição'), ':', r.page_title) redir,
   r.page_namespace ns,
   r.page_title title,
   CONCAT(IF(m.page_namespace = 4, 'Wikipédia', 'Predefinição'), ':', m.page_title) redireciona_para
   FROM categorylinks
   INNER JOIN page m ON cl_from = m.page_id
   INNER JOIN redirect ON (rd_namespace, rd_title) = (m.page_namespace, m.page_title)
   INNER JOIN page r ON rd_from = r.page_id
   WHERE cl_to = ? AND m.page_namespace IN (4, 10)
 ) marcas
 LEFT JOIN templatelinks ON (tl_namespace, tl_title) = (ns, title)
 GROUP BY redir
 ORDER BY marca""", (cat,))
    r = c.fetchall()
    r = [(redir.decode('utf-8'), int(num), predef.decode('utf-8')) for redir, num, predef  in r]
    if r:
        resp = {'wiki': wiki, 'link': link(wiki), 'lista': r}
    else:
        resp = {'aviso': u'A consulta não retornou resultados'}
    return render_template_string(page, title=u'Transclusões de redirecionamentos para  predefinições da categoria ' + cat.replace(u'_', u' '), **resp)
  else:
    return render_template_string(page, title=u'Transclusões de redirecionametos para predefinições de uma categoria')
