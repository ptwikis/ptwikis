# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn

page = u'''{% extends "Tools.html" %}
{% block content %}
<p>List of articles that exists in the English Wikipedia without interwiki to a determined language, ordered by existing interwikis.</p>
<p>Language prefix: <input id="user" type="text" size=2 onkeypress="return enter(event, this, 'common-iw:')"/></p>
{% if query %}<ul>
{%- for title, links in query %}
<li> {{ links }} <a href="https://en.wikipedia.org/wiki/{{ title }}" class="ext">{{ title|replace('_', ' ') }}</a> - <a href="https://{{ prefix }}.wikipedia.org/wiki/Special:Search/{{ title }}" style="color:#555">search in {{ prefix }}.wiki</a>
{%- endfor %}
</ul>{% endif %}
<p><i>The database is updated once a day</i></p>
{% endblock %}'''

def main(args=None):
  if not args:
    return render_template_string(page, title=u'Common interwiki articles')
  c = conn('p50380g50592__interwikis_p', 's1.labsdb')
  c.execute('SELECT ell_title, ell_links FROM enwiki_langlinks WHERE ell_langs NOT LIKE ? LIMIT 200', ('% {} %'.format(args),))
  r = c.fetchall()
  return render_template_string(page, title=u'Common interwiki articles missing in {}.wiki'.format(args), prefix=args, query=r)
