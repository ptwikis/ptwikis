# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn

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
    <th colspan=6>Importância</th>
  </tr>
  <tr>
    <th>Qualidade</th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Escala-laranja-4de4.svg/68px-Escala-laranja-4de4.svg.png"></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Escala-laranja-3de4.svg/68px-Escala-laranja-3de4.svg.png"></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Escala-laranja-2de4.svg/68px-Escala-laranja-2de4.svg.png"></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/1/19/Escala-laranja-1de4.svg/68px-Escala-laranja-1de4.svg.png"></th>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/2/21/Escala-laranja-PA.svg/68px-Escala-laranja-PA.svg.png"></th>
    <th>Total</th>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/9/99/Escala-azul-1de6.svg/102px-Escala-azul-1de6.svg.png"></th>
    <td style="background:#ffa5a5">{{ qi[1][4] }}</td>
    <td style="background:#ffc3a5">{{ qi[1][3] }}</td>
    <td style="background:#ffe1a5">{{ qi[1][2] }}</td>
    <td style="background:#ffffa5">{{ qi[1][1] }}</td>
    <td style="background:#eeeeff">{{ qi[1][0] }}</td>
    <td>{{ qi[1]|sum }}</td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Escala-azul-2de6.svg/102px-Escala-azul-2de6.svg.png"></th>
    <td style="background:#ffc9a5">{{ qi[2][4] }}</td>
    <td style="background:#ffdbab">{{ qi[2][3] }}</td>
    <td style="background:#ffedb1">{{ qi[2][2] }}</td>
    <td style="background:#ffffb7">{{ qi[2][1] }}</td>
    <td style="background:#eeeeff">{{ qi[2][0] }}</td>
    <td>{{ qi[2]|sum }}</td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Escala-azul-3de6.svg/102px-Escala-azul-3de6.svg.png"></th>
    <td style="background:#ffeda5">{{ qi[3][4] }}</td>
    <td style="background:#fff9b1">{{ qi[3][3] }}</td>
    <td style="background:#fff9bd">{{ qi[3][2] }}</td>
    <td style="background:#ffffc9">{{ qi[3][1] }}</td>
    <td style="background:#eeeeff">{{ qi[3][0] }}</td>
    <td>{{ qi[3]|sum }}</td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/7/76/Escala-azul-4de6.svg/102px-Escala-azul-4de6.svg.png"></th>
    <td style="background:#edffa5">{{ qi[4][4] }}</td>
    <td style="background:#f3ffb7">{{ qi[4][3] }}</td>
    <td style="background:#f9ffc9">{{ qi[4][2] }}</td>
    <td style="background:#ffffdb">{{ qi[4][1] }}</td>
    <td style="background:#eeeeff">{{ qi[4][0] }}</td>
    <td>{{ qi[4]|sum }}</td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/db/Escala-azul-5de6.svg/102px-Escala-azul-5de6.svg.png"></th>
    <td style="background:#c9ffa5">{{ qi[5][4] }}</td>
    <td style="background:#dbffbd">{{ qi[5][3] }}</td>
    <td style="background:#edffd5">{{ qi[5][2] }}</td>
    <td style="background:#ffffed">{{ qi[5][1] }}</td>
    <td style="background:#eeeeff">{{ qi[5][0] }}</td>
    <td>{{ qi[5]|sum }}</td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/3/37/Escala-azul-6de6.svg/102px-Escala-azul-6de6.svg.png"></th>
    <td style="background:#a5ffa5">{{ qi[6][4] }}</td>
    <td style="background:#c3ffc3">{{ qi[6][3] }}</td>
    <td style="background:#e1ffe1">{{ qi[6][2] }}</td>
    <td style="background:#ffffff">{{ qi[6][1] }}</td>
    <td style="background:#eeeeff">{{ qi[6][0] }}</td>
    <td>{{ qi[6]|sum }}</td>
  </tr>
  <tr>
    <th style="padding:2px 2px 2px 2px"><img src="//upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Escala-azul-PA.svg/102px-Escala-azul-PA.svg.png"></th>
    <td style="background:#eeeeff">{{ qi[0][4] }}</td>
    <td style="background:#eeeeff">{{ qi[0][3] }}</td>
    <td style="background:#eeeeff">{{ qi[0][2] }}</td>
    <td style="background:#eeeeff">{{ qi[0][1] }}</td>
    <td style="background:#eeeeff">{{ qi[0][0] }}</td>
    <td>{{ qi[0]|sum }}</td>
  </tr>
  <tr>
    <th>Total</th>
    <td>{{ qi[7][4] }}</td>
    <td>{{ qi[7][3] }}</td>
    <td>{{ qi[7][2] }}</td>
    <td>{{ qi[7][1] }}</td>
    <td>{{ qi[7][0] }}</td>
    <td>{{ qi[7]|sum }}</td>
  </tr>
</table>
<p>Nota: Esta ferramenta ainda está em desenvolvimento.</p>
{%- endif %}
{% if erro %}<p style="color:#a00; padding-left:60px">Erro: assunto não encontrado.</p>{% endif %}
{% endblock %}'''

def main(args=None):
  if not args:
    return render_template_string(page, title=u'Matriz de classificação')
  c = conn('ptwiki')
  c.execute(u"""SELECT
 SUM(q.cl_to = '!Artigos_de_qualidade_desconhecida_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_de_qualidade_1_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_de_qualidade_2_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_de_qualidade_3_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_de_qualidade_4_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_bons_sobre_{0}'),
 SUM(q.cl_to = '!Artigos_destacados_sobre_{0}')
 FROM categorylinks i
 INNER JOIN categorylinks q ON i.cl_from = q.cl_from
 WHERE i.cl_to LIKE '!Artigos_de_importância_%_sobre_{0}'
 GROUP BY i.cl_to
 ORDER BY i.cl_to""".format(args.replace(u"'", u'')))
  r = c.fetchall()
  if not r:
    return render_template_string(page, title=u'Matriz de classificação', erro=True)
  qi = [map(int,i) for i in zip(*[r[4], r[0], r[1], r[2], r[3]])]
  return render_template_string(page, title=u'Matriz de classificação sobre {}'.format(args.replace('_', ' ')), qi=qi + [map(sum, zip(*qi))])
