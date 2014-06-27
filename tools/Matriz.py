# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn, ns

page = u'''{% extends "base.html" %}
{% block head %}
        <script>
function enter(e) {
    if (e.keyCode == 13) {
	var value = document.getElementById('sobre').value.replace(/ /g, "_");
	location.href = location.href.substring(0, location.href.lastIndexOf("/") + 1) + "Matriz:" + value;
        return false;
    }
}
        </script>
{% endblock %}
{% block content %}
<p>Matriz de classificação sobre <input id="sobre" type="text" size=20 onkeypress="return enter(event)"/></p>
{%- if qi %}
<table class="wikitable" style="width:250px; margin:0 auto;">
  <tr>
    <td style="background:white; border-top:1px solid white; border-left:1px solid white"></td>
    <th colspan=6><a href="//pt.wikipedia.org/wiki/Predefini%C3%A7%C3%A3o:Escala_de_import%C3%A2ncia">Importância</a></th>
  </tr>
  <tr>
    <th><a href="//pt.wikipedia.org/wiki/Wikip%C3%A9dia:Avalia%C3%A7%C3%A3o_de_artigos">Qualidade</a></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Escala-laranja-4de4.svg/68px-Escala-laranja-4de4.svg.png"></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Escala-laranja-3de4.svg/68px-Escala-laranja-3de4.svg.png"></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Escala-laranja-2de4.svg/68px-Escala-laranja-2de4.svg.png"></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/1/19/Escala-laranja-1de4.svg/68px-Escala-laranja-1de4.svg.png"></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/2/21/Escala-laranja-PA.svg/68px-Escala-laranja-PA.svg.png"></th>
    <th>Total</th>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/9/99/Escala-azul-1de6.svg/102px-Escala-azul-1de6.svg.png"></th>
    <td style="background:#ffa5a5"><a href="/ptwikis/Matriz:{{ sobre }}&q1i4">{{ qi[1][4] }}</a></td>
    <td style="background:#ffc3a5"><a href="/ptwikis/Matriz:{{ sobre }}&q1i3">{{ qi[1][3] }}</a></td>
    <td style="background:#ffe1a5"><a href="/ptwikis/Matriz:{{ sobre }}&q1i2">{{ qi[1][2] }}</a></td>
    <td style="background:#ffffa5"><a href="/ptwikis/Matriz:{{ sobre }}&q1i1">{{ qi[1][1] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q1i0">{{ qi[1][0] }}</a></td>
    <td><a href="https://pt.wikipedia.org/wiki/Categoria:!Artigos_de_qualidade_1_sobre_{{ sobre }}">{{ qi[1]|sum }}</a></td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Escala-azul-2de6.svg/102px-Escala-azul-2de6.svg.png"></th>
    <td style="background:#ffc9a5"><a href="/ptwikis/Matriz:{{ sobre }}&q2i4">{{ qi[2][4] }}</a></td>
    <td style="background:#ffdbab"><a href="/ptwikis/Matriz:{{ sobre }}&q2i3">{{ qi[2][3] }}</a></td>
    <td style="background:#ffedb1"><a href="/ptwikis/Matriz:{{ sobre }}&q2i2">{{ qi[2][2] }}</a></td>
    <td style="background:#ffffb7"><a href="/ptwikis/Matriz:{{ sobre }}&q2i1">{{ qi[2][1] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q2i0">{{ qi[2][0] }}</a></td>
    <td><a href="https://pt.wikipedia.org/wiki/Categoria:!Artigos_de_qualidade_2_sobre_{{ sobre }}">{{ qi[2]|sum }}</a></td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Escala-azul-3de6.svg/102px-Escala-azul-3de6.svg.png"></th>
    <td style="background:#ffeda5"><a href="/ptwikis/Matriz:{{ sobre }}&q3i4">{{ qi[3][4] }}</a></td>
    <td style="background:#fff9b1"><a href="/ptwikis/Matriz:{{ sobre }}&q3i3">{{ qi[3][3] }}</a></td>
    <td style="background:#fff9bd"><a href="/ptwikis/Matriz:{{ sobre }}&q3i2">{{ qi[3][2] }}</a></td>
    <td style="background:#ffffc9"><a href="/ptwikis/Matriz:{{ sobre }}&q3i1">{{ qi[3][1] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q3i0">{{ qi[3][0] }}</a></td>
    <td><a href="https://pt.wikipedia.org/wiki/Categoria:!Artigos_de_qualidade_3_sobre_{{ sobre }}">{{ qi[3]|sum }}</a></td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/7/76/Escala-azul-4de6.svg/102px-Escala-azul-4de6.svg.png"></th>
    <td style="background:#edffa5"><a href="/ptwikis/Matriz:{{ sobre }}&q4i4">{{ qi[4][4] }}</a></td>
    <td style="background:#f3ffb7"><a href="/ptwikis/Matriz:{{ sobre }}&q4i3">{{ qi[4][3] }}</a></td>
    <td style="background:#f9ffc9"><a href="/ptwikis/Matriz:{{ sobre }}&q4i2">{{ qi[4][2] }}</a></td>
    <td style="background:#ffffdb"><a href="/ptwikis/Matriz:{{ sobre }}&q4i1">{{ qi[4][1] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q4i0">{{ qi[4][0] }}</a></td>
    <td><a href="https://pt.wikipedia.org/wiki/Categoria:!Artigos_de_qualidade_4_sobre_{{ sobre }}">{{ qi[4]|sum }}</a></td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/db/Escala-azul-5de6.svg/102px-Escala-azul-5de6.svg.png"></th>
    <td style="background:#c9ffa5"><a href="/ptwikis/Matriz:{{ sobre }}&q5i4">{{ qi[5][4] }}</a></td>
    <td style="background:#dbffbd"><a href="/ptwikis/Matriz:{{ sobre }}&q5i3">{{ qi[5][3] }}</a></td>
    <td style="background:#edffd5"><a href="/ptwikis/Matriz:{{ sobre }}&q5i2">{{ qi[5][2] }}</a></td>
    <td style="background:#ffffed"><a href="/ptwikis/Matriz:{{ sobre }}&q5i1">{{ qi[5][1] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q5i0">{{ qi[5][0] }}</a></td>
    <td><a href="https://pt.wikipedia.org/wiki/Categoria:!Artigos_bons_sobre_{{ sobre }}">{{ qi[5]|sum }}</a></td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/3/37/Escala-azul-6de6.svg/102px-Escala-azul-6de6.svg.png"></th>
    <td style="background:#a5ffa5"><a href="/ptwikis/Matriz:{{ sobre }}&q6i4">{{ qi[6][4] }}</a></td>
    <td style="background:#c3ffc3"><a href="/ptwikis/Matriz:{{ sobre }}&q6i3">{{ qi[6][3] }}</a></td>
    <td style="background:#e1ffe1"><a href="/ptwikis/Matriz:{{ sobre }}&q6i2">{{ qi[6][2] }}</a></td>
    <td style="background:#ffffff"><a href="/ptwikis/Matriz:{{ sobre }}&q6i1">{{ qi[6][1] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q6i0">{{ qi[6][0] }}</a></td>
    <td><a href="https://pt.wikipedia.org/wiki/Categoria:!Artigos_destacados_sobre_{{ sobre }}">{{ qi[6]|sum }}</a></td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Escala-azul-PA.svg/102px-Escala-azul-PA.svg.png"></th>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q0i4">{{ qi[0][4] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q0i3">{{ qi[0][3] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q0i2">{{ qi[0][2] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q0i1">{{ qi[0][1] }}</a></td>
    <td style="background:#eeeeff"><a href="/ptwikis/Matriz:{{ sobre }}&q0i0">{{ qi[0][0] }}</a></td>
    <td><a href="https://pt.wikipedia.org/wiki/Categoria:!Artigos_de_qualidade_desconhecida_sobre_{{ sobre }}">{{ qi[0]|sum }}</a></td>
  </tr>
  <tr>
    <th>Total</th>
    <td><a href="//pt.wikipedia.org/wiki/Categoria:!Artigos_de_import%C3%A2ncia_4_sobre_{{ sobre }}">{{ qi[7][4] }}</a></td>
    <td><a href="//pt.wikipedia.org/wiki/Categoria:!Artigos_de_import%C3%A2ncia_3_sobre_{{ sobre }}">{{ qi[7][3] }}</a></td>
    <td><a href="//pt.wikipedia.org/wiki/Categoria:!Artigos_de_import%C3%A2ncia_2_sobre_{{ sobre }}">{{ qi[7][2] }}</a></td>
    <td><a href="//pt.wikipedia.org/wiki/Categoria:!Artigos_de_import%C3%A2ncia_1_sobre_{{ sobre }}">{{ qi[7][1] }}</a></td>
    <td><a href="//pt.wikipedia.org/wiki/Categoria:!Artigos_de_import%C3%A2ncia_desconhecida_sobre_{{ sobre }}">{{ qi[7][0] }}</a></td>
    <td>{{ qi[7]|sum }}</td>
  </tr>
</table>
{%- endif %}
{% if erro %}<p style="color:#a00; padding-left:60px">Erro: assunto não encontrado.</p>{% endif %}
{%- if lista %}
<table class="lista">{% for item in lista %}
<tr><td><a class="ext" href="https://pt.wikipedia.org/wiki/{{ item[0] }}">{{ item[0]|replace('_', ' ') }}</a>
 (<a class="ext" href="https://pt.wikipedia.org/w/index.php?title={{ item[0] }}&action=history">hist</a> ·
 <a class="ext" href="https://pt.wikipedia.org/wiki/Discussão:{{ item[0] }}">disc</a>)</td>
 {%- for d in item[1:] %}<td>{{ d }}</td>{% endfor %}</tr>
{% endfor %}</table>
<p><small>Nota: os dados de visitas são de maio de 2014</small></p>
{%- endif %}
<p>{{ aviso }}</p>
{% endblock %}'''

def main(args=None):
  if not args:
    return render_template_string(page, title=u'Matriz de classificação')
  aviso = u''
  args = args.split(u'&')
  c = conn('ptwiki')
  query = u"""SELECT
 SUM(q.cl_to = '!Artigos_de_qualidade_desconhecida_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_de_qualidade_1_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_de_qualidade_2_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_de_qualidade_3_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_de_qualidade_4_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_bons_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_destacados_sobre_{0}'),
 SUBSTR(i.cl_to, 26, 1)
 FROM categorylinks i
 INNER JOIN categorylinks q ON i.cl_from = q.cl_from
 WHERE i.cl_to LIKE '!Artigos\_de\_importância\_%\_sobre\_{0}'
 GROUP BY i.cl_to
 ORDER BY i.cl_to"""
  c.execute(query.format(args[0].replace(u"'", u'')))
  r = c.fetchall()
  if not r:
    alt = args[0][0].swapcase() + args[0][1:]
    c.execute(query.format(alt.replace(u"'", u'')))
    r = c.fetchall()
    if not r:
      return render_template_string(page, title=u'Matriz de classificação', erro=True)
    else:
      args[0] = alt
  r = dict((i[7], i[0:7]) for i in r)
  r = [i in r and r[i] or (0, 0, 0, 0, 0, 0, 0) for i in ('d', '1', '2', '3', '4')]
  qi = [map(int,i) for i in zip(*[r[0], r[1], r[2], r[3], r[4]])]
  if len(args) == 2 and len(args[1]) == 4 and args[1][0] + args[1][2] == u'qi' and (args[1][1] + args[1][3]).isdigit():
    catq = u'!Artigos_{}_sobre_{}'.format(args[1][1] == u'5' and u'bons' or args[1][1] ==  u'6' and u'destacados' or
      u'de_qualidade_' + (args[1][1] == u'0' and u'desconhecida' or str(args[1][1])), args[0])
    cati = u'!Artigos_de_importância_{}_sobre_{}'.format(args[1][3] == u'0' and u'desconhecida' or args[1][3], args[0])
    c.execute(u"""SELECT page_namespace, page_title, ac_201405, page_len
 FROM (SELECT
   page_namespace ns, page_title title
   FROM categorylinks cq
   INNER JOIN categorylinks ci ON cq.cl_from = ci.cl_from
   INNER JOIN page ON cq.cl_from = page_id
   WHERE cq.cl_to = ? AND ci.cl_to = ? AND cq.cl_type = 'page'
   LIMIT 200
 ) talks
 INNER JOIN page ON page_namespace = (ns - (ns % 2)) AND page_title = title
 LEFT JOIN p50380g50592__pt.acessos ON page_id = ac_page AND ac_wiki = 'w'
 ORDER BY ac_201405 DESC
 LIMIT 200""", (catq, cati))
    r = c.fetchall()
    r = [((i[0] in ns and ns[i[0]] or u'') + i[1].decode('utf-8'), u'{} visita{}'.format(i[2] or u'Nenhuma', i[2] and i[2] > 0 and u's' or u''),
      u'{} bytes'.format(i[3])) for i in r]
    if not r:
      aviso = u'Não foram encontrados artigos com essa qualidade e importância.'
  else:
    r = None
  return render_template_string(page, title=u'Matriz de classificação sobre {}'.format(args[0].replace('_', ' ')), sobre = args[0],
    qi=qi + [map(sum, zip(*qi))], lista = r, aviso=aviso)
