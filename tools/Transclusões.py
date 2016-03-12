# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn, link

page = u'''
{% extends "base.html" %}
{% block content %}
<p>Lista número de transclusões de predefinições por categoria.</p>
<table style="margin: 4em auto 5em auto;">
  <tr>
    <td>Categoria:</td>
    <td><input id="user" type="text" onkeypress="return enter(event, this, 'Transclusões:')"/></td>
  </tr>
</table>
{% if lista %}
<table class="wikitable">
  <tr><th>Predefinição</th><th>Transclusões</th></tr>
{%- for page, num in lista %}
  <tr>
    <td><a href="//{{ link }}.org/wiki/{{ page|replace(" ", "_") }}">{{ page|replace('_', ' ') }}</a></td>
    <td><a href="//{{ link }}.org/w/index.php?title=Especial:P%C3%A1ginas_afluentes/{{ page|replace(' ', '_') }}&hidelinks=1&hideredirs=1">{{ num }}</a></td>
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
 CONCAT(IF(page_namespace = 4, 'Wikipédia', 'Predefinição'), ':', page_title) p,
 COUNT(tl_title) t
 FROM (SELECT
   page_namespace,
   page_title
   FROM categorylinks
   INNER JOIN page ON cl_from = page_id
   WHERE cl_to = ? AND page_namespace IN (4, 10)
 ) predefs
 LEFT JOIN templatelinks ON (page_namespace, page_title) = (tl_namespace, tl_title)
 GROUP BY p
 ORDER BY t""", (cat,))
    r = c.fetchall()
    r = [(u.decode('utf-8'), int(n)) for u, n in r]
    if r:
        resp = {'wiki': wiki, 'link': link(wiki), 'lista': r}
    else:
        resp = {'aviso': u'A consulta não retornou resultados'}
    return render_template_string(page, title=u'Transclusões de predefinições da categoria ' + cat.replace(u'_', u' '), **resp)
  else:
    return render_template_string(page, title=u'Transclusões de predefinições de uma categoria')
