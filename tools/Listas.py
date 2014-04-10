# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn, ns
import re

page = u'''{% extends "base.html" %}
{% block head %}
        <script>
function listar(nome) {
    if (nome === undefined) {
	var busca1 = document.getElementById('busca1').value;
	var sobre1 = document.getElementById('sobre1').value.replace(/ /g, "_");
	var busca2 = document.getElementById('busca2').value;
	var sobre2 = document.getElementById('sobre2').value.replace(/ /g, "_");
	var ordenar = '&ordenar:' + document.getElementById('ordem').value.replace(/ /g, "_");
	if (!sobre1) {
	  alert('Preecha o nome de uma categoria, predefinição ou marca de projeto');
	  return false;}
	location.href = location.href.substring(0, location.href.lastIndexOf("/") + 1) + "Listas:" + busca1 + ':' + sobre1 + (sobre2 && ('&' + busca2 + ':' + sobre2) || '') + ordenar;
        return false;
    }
    else{
	location.href = location.href.substring(0, location.href.lastIndexOf("/") + 1) + "Listas:" + nome.replace(/ /g, "_");
    }
}
        </script>
	<style>table.lista td{padding:2px 5px 2px 5px}</style>
{% endblock %}
{% block content %}
<p>Buscar em páginas com a <select id="busca1"><option value="cat">categoria<option value="predef">predefinição<option value="marca">marca de projeto</select> 
  <input id="sobre1" type="text" size=30/>
<br/>Que tenham a <select id="busca2"><option value="cat">categoria<option value="predef">predefinição<option value="marca">marca de projeto</select> 
  <input id="sobre2" type="text" size=30/> (opcional)
<br/>Ordenar por <select id="ordem"><option>mais visitas<option>menos visitas<option>maior tamanho<option>menor tamanho</select>
  <input style="margin-left:100px" type="button" value="Listar" onClick="return listar()"></p>
<p>Listas especiais: <select id="especial"><option>Páginas com mais reversões<option>Usuários mais revertidos</select> <input type="button" value="Listar" onClick="return listar(document.getElementById('especial').value)"></p>
{% if query %}
<table class="lista">{% for item in query %}
<tr><td>{%if not user %}<a class="ext" href="https://pt.wikipedia.org/wiki/{{ item[0] }}">{{ item[0]|replace('_', ' ') }}</a> (<a class="ext" href="https://pt.wikipedia.org/w/index.php?title={{ item[0] }}&action=history">hist</a>){% else %}<a class= "ext" href="https://pt.wikipedia.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{ item[0] }}">{{ item[0]|replace('_', ' ') }}{% endif %}</td>{% for d in item[1:] %}<td>{{ d }}</td>{% endfor %}</tr>
{% endfor %}</table>{% endif %}
<p>{{ aviso }}</p>
{% endblock %}'''

def main(args=None):
  if not args:
    return render_template_string(page, title=u'Listas')
  args = args.split(u'&')

  # Se não for página especial
  if u':' in args[0]:
    params = {}
    ordens = {u'mais_visitas': 'vi_mes DESC, page_len DESC',
              u'menos_visitas': 'vi_mes, page_len DESC',
	      u'maior_tamanho': 'page_len DESC, vi_mes DESC',
	      u'menor_tamanho': 'page_len, vi_mes DESC'}
    for arg in args:
      if arg.startswith(u'cat:'):
	params['cat' in params and 'cat2' or 'cat'] = arg[4:].capitalize()
      elif arg.startswith(u'predef:'):
	params['predef' in params and 'predef2' or 'predef'] = arg[7:].capitalize()
      elif arg.startswith(u'marca:'):
	params['marca' in params and 'marca2' or 'marca'] = arg[6:]
      elif arg.startswith(u'ordenar:'):
	params['ordenar'] = arg[8:]
    r = False
    ordenar = 'ordenar' in params and params['ordenar'] in ordens and ordens[params['ordenar']] or ordens['mais_visitas']
    # Marca nos parâmetros
    if 'marca' in params:
      if 'cat' in params:
        marca2, filtro2, textofiltro = u'', u"INNER JOIN ptwiki_p.categorylinks cc ON a.page_id = cc.cl_from AND cc.cl_to = ?", (params['cat'],)
        title = u'Lista de páginas com marca sobre ' + params['marca'].replace(u'_', u' ') + u' e a categoria ' + params['cat'].replace(u'_', u' ')
      elif 'predef' in params:
        marca2, filtro2, textofiltro = u'', u"INNER JOIN ptwiki_p.templatelinks ON a.page_id = tl_from AND tl_namespace = 10 AND tl_title = ?", (params['predef'],)
        title = u'Lista de páginas com marca sobre ' + params['marca'].replace(u'_', u' ') + u' e a predefinição ' + params['predef'].replace(u'_', u' ')
      elif 'marca2' in params:
        marca2, filtro2, textofiltro = u"INNER JOIN ptwiki_p.categorylinks cc ON c.cl_from = cc.cl_from AND cc.cl_to LIKE ?", u'', (u'!Artigos_de_importância_%_sobre_' + params['marca2'],)
        title = u'Lista de páginas com marcas sobre ' + params['marca'].replace(u'_', u' ') + u' e sobre ' + params['marca2'].replace(u'_', u' ')
      else:
        marca2, filtro2, textofiltro = u'', u'', ()
        title = u'Lista de páginas com marca sobre ' + params['marca'].replace(u'_', u' ')
      c = conn('p50380g50592__pt', 's2.labsdb')
      c.execute(u"""SELECT a.page_namespace, a.page_title, vi_mes, a.page_len
 FROM ptwiki_p.categorylinks c
 {0}
 INNER JOIN ptwiki_p.page d ON c.cl_from = page_id
 INNER JOIN ptwiki_p.page a ON a.page_namespace = (d.page_namespace - 1) AND d.page_title = a.page_title
 {1}
 LEFT JOIN visitas ON a.page_id = vi_page
 WHERE c.cl_to LIKE ?
 ORDER BY {2}
 LIMIT 200""".format(marca2, filtro2, ordenar), textofiltro + (u'!Artigos_de_importância_%_sobre_' + params['marca'],))
      r = c.fetchall()
      r = [((i[0] in ns and ns[i[0]] or u'') + i[1].decode('utf-8'), u'{} visita{}'.format(i[2] or u'Nenhuma', i[2] and i[2] > 0 and u's' or u''), u'{} bytes'.format(i[3])) for i in r]
    # Categoria nos parâmetros
    elif 'cat' in params:
      if 'predef' in params:
        filtro2, textofiltro = u"INNER JOIN ptwiki_p.templatelinks ON c.cl_from = tl_from AND tl_namespace = 10 AND tl_title = ?", (params['predef'],)
	title = u'Lista de páginas com a categoria ' + params['cat'].replace(u'_', u' ') + u' e a predefinição ' + params['predef'].replace(u'_', u' ')
      if 'cat2' in params:
        filtro2, textofiltro = u"INNER JOIN ptwiki_p.categorylinks cc ON c.cl_from = cc.cl_from AND cl_to = ?", (params['cat'],)
	title = u'Lista de páginas com a categoria ' + params['cat'].replace(u'_', u' ') + u' e a categoria ' + params['cat'].replace(u'_', u' ')
      else:
        filtro2, textofiltro = u'', ()
	title = u'Lista de páginas com a categoria ' + params['cat'].replace(u'_', u' ')
      c = conn('p50380g50592__pt', 's2.labsdb')
      c.execute(u"""SELECT page_namespace, page_title, vi_mes, page_len
 FROM ptwiki_p.categorylinks c
 {0}
 INNER JOIN ptwiki_p.page ON c.cl_from = page_id
 LEFT JOIN visitas ON page_id = vi_page
 WHERE cl_to = ? AND c.cl_type = 'page'
 ORDER BY {1}
 LIMIT 200""".format(filtro2, ordenar), textofiltro + (params['cat'],))
      r = c.fetchall()
      r = [((i[0] in ns and ns[i[0]] or u'') + i[1].decode('utf-8'), u'{} visita{}'.format(i[2] or u'Nenhuma', i[2] and i[2] > 0 and u's' or u''), u'{} bytes'.format(i[3])) for i in r]
    # Predefinição nos parâmetros
    elif 'predef' in params:
      if 'predef2' in params:
        predef2, textopredef2 = u"INNER JOIN ptwiki_p.templatelinks b ON a.tl_from = b.tl_from AND b.tl_namespace = 10 AND b.tl_title = ?", (params['predef2'],)
        title = u'Lista de páginas com a predefinição ' + params['predef'].replace(u'_', u' ') + u' e a predefinição ' + params['predef2'].replace(u'_', u' ')
      else:
        predef2, textopredef2 = u'', ()
        title = u'Lista de páginas com a predefinição ' + params['predef'].replace(u'_', u' ')
      c = conn('p50380g50592__pt', 's2.labsdb')
      c.execute(u"""SELECT page_namespace, page_title, vi_mes, page_len
 FROM ptwiki_p.templatelinks a
 {0}
 INNER JOIN ptwiki_p.page ON a.tl_from = page_id
 LEFT JOIN visitas ON page_id = vi_page
 WHERE a.tl_namespace = 10 AND a.tl_title = ?
 ORDER BY {1}
 LIMIT 200""".format(predef2, ordenar), (predef2 and (params['predef2'],) or ()) + (params['predef'],))
      r = c.fetchall()
      r = [((i[0] in ns and ns[i[0]] or u'') + i[1].decode('utf-8'), u'{} visita{}'.format(i[2] or u'Nenhuma', i[2] and i[2] > 0 and u's' or u''), u'{} bytes'.format(i[3])) for i in r]
    if r:
      if 'ordenar' in params and params['ordenar'] in (u'maior_tamanho', u'menor_tamanho'):
	r = [(i[0], i[2], i[1]) for i in r]
      return render_template_string(page, title=title, query=r)
    else:
      return render_template_string(page, title=title, aviso=u'<span style="color:#555555"><b>Nenhuma página com esses parâmetros</b></span>')

  # Páginas com mais reversões
  elif args[0] == u'Páginas_com_mais_reversões':
    c = conn('ptwiki')
    c.execute(u"SELECT rc_namespace, rc_title, SUM(rc_comment LIKE '[[WP:REV|%' OR rc_comment LIKE 'Foram [[WP:REV|%' OR rc_comment LIKE 'bot: revertidas edições de%' OR rc_comment LIKE 'Reversão de uma ou mais edições de%') rev FROM recentchanges WHERE TIMESTAMPDIFF(DAY, rc_timestamp, CURDATE()) <= 10 GROUP BY rc_namespace, rc_title HAVING rev > 0 ORDER BY rev DESC LIMIT 100")
    r = c.fetchall()
    r = [((i[0] in ns and ns[i[0]] or u'') + i[1].decode('utf-8'), u'{} reversões'.format(i[2])) for i in r]
    return render_template_string(page, title=u'Lista das páginas com mais reversões nos últimos 10 dias', query=r)

  # Usuários mais revertidos
  elif args[0] == u'Usuários_mais_revertidos':
    import re
    user = re.compile(r'pecial:Contrib.+?/(.+?)\|')
    c = conn('ptwiki')
    c.execute(u"SELECT SUBSTR(rc_comment, 1, 100) user, COUNT(*) FROM recentchanges WHERE TIMESTAMPDIFF(DAY, rc_timestamp, CURDATE()) <= 5 AND rc_type = 0 AND (rc_comment LIKE '[[WP:REV|%' OR rc_comment LIKE 'bot: revertidas edições de%' OR rc_comment LIKE 'Foram [[WP:REV|%' OR rc_comment LIKE 'Reversão de uma ou mais edições de%') GROUP BY user")
    r = c.fetchall()
    r = [(user.search(i[0]), int(i[1])) for i in r if ':CITE|' not in i[0]]
    r = [(i[0].group(1).decode('utf-8'), i[1]) for i in r if i[0]]
    r2 = {}
    for i in r:
      r2[i[0]] = i[0] in r2 and r2[i[0]] + i[1] or i[1]
    r = sorted(r2.items(), key=lambda i:i[1], reverse=True)[0:70]
    c.execute(u"SELECT afl_user_text user, COUNT(*) FROM abuse_filter_log WHERE TIMESTAMPDIFF(DAY, afl_timestamp, CURDATE()) <= 5 AND afl_user_text IN ({}) GROUP BY user".format(u','.join(u'?' * len(r))), tuple(i[0] for i in r))
    r2 = c.fetchall()
    r2 = dict((i[0].decode('utf-8'), int(i[1])) for i in r2)
    c.execute(u"SELECT ipb_address FROM ipblocks WHERE ipb_address IN ({}) AND (ipb_expiry = 'ininity' OR ipb_expiry > DATE_FORMAT(NOW(), '%Y%m%d%H%i%S'))".format(u','.join(u'?' * len(r))), tuple(i[0] for i in r))
    r3 = [i[0].decode('utf-8') for i in c.fetchall()]
    r = [(i[0], u'revertido {} vezes'.format(i[1]), i[0] in r2 and u'disparou filtros {} {}'.format(r2[i[0]], r2[i[0]] == 1 and u'vez' or u'vezes') or u'', i[0] in r3 and u'Bloqueado' or u'') for i in r]
    return render_template_string(page, title=u'Lista dos usuários mais revertidos nos últimos 5 dias', query=r, user=True)

  else:
    return render_template_string(page, title=u'Listas', aviso=u'Erro')
