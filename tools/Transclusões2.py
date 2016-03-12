# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn, link

page = u'''
{% extends "base.html" %}
{% block content %}
<p>Lista número de transclusões de predefinições por prefixo.</p>

<table style="margin: 4em auto 5em auto;">
  <tr>
    <td>Prefixo: Predefinição:</td>
    <td><input id="user" type="text" onkeypress="return enter(event, this, 'Transclusões2:')"/></td>
  </tr>
</table>
{% if lista %}
<p>Encontradas {{ lista|length }} predefinições.</p>
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

def main(predef=None):
  if predef:
    wiki = u'Wikipédia'
    c = conn(wiki)
    c.execute(u"""SELECT
 CONCAT('Predefinição', ':', page_title) p,
 COUNT(tl_title) t
 FROM (SELECT
   page_title
   FROM page
   WHERE page_namespace = 10 AND page_title LIKE ?
 ) predefs
 LEFT JOIN templatelinks ON page_title = tl_title AND tl_namespace = 10
 GROUP BY p
 ORDER BY t, p""", (predef + u'%',))
    r = c.fetchall()
    r = [(u.decode('utf-8'), int(n)) for u, n in r]
    if r:
        resp = {'wiki': wiki, 'link': link(wiki), 'lista': r}
    else:
        resp = {'aviso': u'A consulta não retornou resultados'}
    return render_template_string(page, title=u'Transclusões de predefinições com o prefixo "' + predef.replace(u'_', u' ') + u'..."', **resp)
  else:
    return render_template_string(page, title=u'Transclusões de predefinições com um prefixo')
