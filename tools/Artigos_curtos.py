# -*- coding: utf-8 -*-

from flask import render_template_string
from database import query, link

page = u'''
{% extends "base.html" %}
{% block content %}
<p>Lista dos menores artigos da Wikipédia, desconsiderando as desambiguações.</p>
<table class="wikitable">
	<tr><th rowspan=2>Artigo</th><th rowspan=2>Tamanho</th><th colspan=2>Última edição</th><th rowspan=2>Categoria</th></tr>
  <tr><th>Data</th><th>Usuário</th></tr>
{%- for page, size, ts, user, cat in lista %}
  <tr>
    <td><a href="https://{{ link }}.org/wiki/{{ page }}">{{ page|replace("_", " ") }}</a></td>
    <td>{{ size }} bytes</td>
    <td>{{ "%s.%s.%s"|format(ts[6:8], ts[4:6], ts[2:4]) }}</td>
    <td><a href="https://{{ link }}.org/wiki/User:{{ user }}">{{ user|replace("_", " ") }}</a>
        (<a href="https://{{ link }}.org/wiki/User_Talk:{{ user }}">D</a> <a href="https://{{ link }}.org/wiki/Special:Contribs/{{ user }}">C</a>)</td>
<td>{% if cat != None %}<a href="https://{{ link }}.org/wiki/Category:{{ cat }}">{{ cat|replace("_", " ") }}</td>{% endif %}
  </tr>
{%- endfor %}
</table>
{% endblock %}
'''

def main(wiki=None):
    if not wiki:
        wiki = u'Wikipédia'
    r = query(u"""SELECT
 page_title,
 page_len,
 rev_timestamp,
 rev_user_text,
 cl_to
 FROM (
  SELECT
   page_id,
   page_latest,
   page_title,
   page_len
   FROM page
   WHERE page_namespace = 0 AND page_is_redirect = 0 AND page_id NOT IN (
    SELECT
     cl_from
     FROM categorylinks
     WHERE cl_to = 'Desambiguação'
   )
   AND page_len < 800
   ORDER BY page_len
   LIMIT 100
 ) p
 LEFT JOIN revision ON page_latest = rev_id
 LEFT JOIN categorylinks ON page_id = cl_from AND cl_to NOT LIKE '!%'
 GROUP BY page_title
 ORDER BY page_len""", wiki)
    if r:
        resp = {'wiki': wiki, 'link': link(wiki), 'lista': r}
    else:
        resp = {}
    return render_template_string(page, title=u'Artigos curtos', **resp)
