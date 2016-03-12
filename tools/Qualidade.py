# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn

page = u'''
{% extends "base.html" %}
{% block content %}
<p>Número de páginas por qualidade, considerando as {{soma}} páginas com marcas de projeto com avaliação humana ou automática.</p>
<table class="wikitable">
<caption>Páginas por qualidade</caption>
<tr><th>Qualidade</th><th>Número de páginas</th></tr>
<tr><td style="font-size:2em"><a href="//pt.wikipedia.org/wiki/Especial:%C3%8Dndice_por_prefixo/Categoria:!Artigos_de_qualidade_1_sobre">1</a></td><td>{{ qualidade[0]|replace('.', ',') }}</td></tr>
<tr><td style="font-size:2em"><a href="//pt.wikipedia.org/wiki/Especial:%C3%8Dndice_por_prefixo/Categoria:!Artigos_de_qualidade_2_sobre">2</a></td><td>{{ qualidade[1]|replace('.', ',') }}</td></tr>
<tr><td style="font-size:2em"><a href="//pt.wikipedia.org/wiki/Especial:%C3%8Dndice_por_prefixo/Categoria:!Artigos_de_qualidade_3_sobre">3</a></td><td>{{ qualidade[2]|replace('.', ',') }}</td></tr>
<tr><td style="font-size:2em"><a href="//pt.wikipedia.org/wiki/Especial:%C3%8Dndice_por_prefixo/Categoria:!Artigos_de_qualidade_4_sobre">4</a></td><td>{{ qualidade[3]|replace('.', ',') }}</td></tr>
<tr><td style="font-size:2em"><a href="//pt.wikipedia.org/wiki/Especial:%C3%8Dndice_por_prefixo/Categoria:!Artigos_bons_sobre">5</a></td><td>{{ qualidade[4]|replace('.', ',') }}</td></tr>
<tr><td style="font-size:2em"><a href="//pt.wikipedia.org/wiki/Especial:%C3%8Dndice_por_prefixo/Categoria:!Artigos_destacados_sobre">6</a></td><td>{{ qualidade[5]|replace('.', ',') }}</td></tr>
</table>
{% if aviso %}<p style="color: #520;">{{ aviso }}</p>{% endif %}
{% endblock %}
'''

def main(arg=None):
  c = conn(u'Wikipédia')
  c.execute(u"""SELECT
 SUM(SUBSTR(cl_to, 23, 1) = '1') Q1,
 SUM(SUBSTR(cl_to, 23, 1) = '2') Q2,
 SUM(SUBSTR(cl_to, 23, 1) = '3') Q3,
 SUM(SUBSTR(cl_to, 23, 1) = '4') Q4,
 SUM(SUBSTR(cl_to, 10, 4) = 'bons') Q5,
 SUM(SUBSTR(cl_to, 10, 10) = 'destacados') Q6
 FROM (SELECT
   cl_from,
   cl_to
   FROM categorylinks
   WHERE cl_to LIKE '!Artigos\_de\_qualidade\__\_sobre\_%' OR cl_to LIKE '!Artigos\_destacados\_sobre\_%' OR cl_to LIKE '!Artigos\_bons\_sobre\_%'
   GROUP BY cl_from) cl""")
  r = c.fetchall()
  if r:
    r = map(int, r[0])
    resp = {'qualidade': [u'{} ({}%)'.format(q, round(float(q) * 100 / sum(r), 2)) for q in r], 'soma': sum(r)}
  else:
    resp = {'aviso': u'Erro'}
  return render_template_string(page, title=u'Qualidade das páginas', **resp)
