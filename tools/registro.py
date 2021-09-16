# -*- coding: utf-8 -*-

from flask import request, render_template_string, jsonify, Response, session
from database import conn
import json

page = u'''{% extends "base.html" %}
{% block content %}
<p>{% if user %}Você está logado como <b>{{ user }}</b>.{% endif %}</p>
<br>
<p>Últimos registros</p>
<table class="wikitable">
<tr><th>id</th><th>tipo</th><th>tipo-id</th><th>status</th><th>commentário</th><th>usuário</th><th>timestamp</th></tr>
{% for id, type, type_id, status, comment, user, timestamp in tabela %}
<tr><td>{{ id }}</td><td>{{ type }}</td><td>{{ type_id }}</td><td>{{ status }}</td><td>{{ comment }}</td><td>{{-
    user }}</td><td>{{ timestamp }}</td></tr>
{% endfor %}
</table>
{% endblock %}
'''

joins = {
  'page': {'id': 'page_id', 'columns': ('page_namepace', 'page_title')},
  'revision': {'id': 'rev_id', 'cloumns': ('rev_user_text', 'rev_timestamp')},
  'user': {'id': 'user_id', 'columns': ('user_name', 'user_registration')},
  'abuse_filter_log': {'id': 'afl_id', 'columns': ('afl_filter', 'afl_timestamp')}
}

def main(args=None):
  if not request.args or request.args.get('action') != 'insert':
    _type = request.args.get('type')
    type_id = request.args.get('id')
    status = request.args.get('status')
    join = request.args.get('join')
    datFormat = request.args.get('format')
    extraColumns = ()
    innerJoin = ''
    where = []
    args = []
    if _type:
      if join and join in ('abuse_filter_log', 'revision', 'page', 'user'):
        innerJoin = ' INNER JOIN %s ON reg_type = ? AND reg_type_id = %s' % (join, joins[join]['id'])
        args.append(_type)
        extraColumns = joins[join]['columns']
        for column in extraColumns:
          if column in request.args:
            oper, cond = mkCond(request.args[column])
            where.append(column + oper)
            args.append(cond)
      else:
        where.append('reg_type = ?')
        args.append(_type)
    if status:
        where.append('reg_status = ?')
        args.append(status)
    if type_id:
        where.append('reg_type_id = ?')
        args.append(type_id)
    sql = u"""SELECT
 reg_id,
 reg_type,
 reg_type_id,
 reg_status,
 reg_comment,
 reg_user,
 reg_timestamp
FROM registro%s
ORDER BY reg_id DESC
LIMIT 50""" % (innerJoin + (where and ' WHERE ' + ' AND '.join(where) or ''))
    c = conn('s51206__ptwikis_p', 's2.labsdb')
    c.execute(sql, tuple(args))
    if datFormat == 'json':
      tabela = [{'id': i, 'type': t, 'type_id': ti, 'status': s, 'comment': c, 'user': u, 'timestamp': ts}
          for i, t, ti, s, c, u, ts in c.fetchall()[::-1]]
      if u'callback' in request.args:
        return Response(request.args[u'callback'] + '(%s)' % json.dumps(tabela), mimetype='text/javascript')
      else:
        return jsonify(tabela)
    return render_template_string(page, title=u'Registro', tabela=c.fetchall()[::-1], user=session.get('user'))

  # Salvar dados
  if not 'user' in session:
    return u'Erro: você não está logado'
  if not request.args.get('type'):
    return u'Erro: o parâmetro type deve ter um valor válido'
  typeid = request.args.get('id')
  status = request.args.get('status')
  comment = request.args.get('comment', '')
  if typeid is None or not typeid.isdigit() or status is None or not status.isdigit():
    return u'Erro: não foi passado valor válido para id ou status, ambos devem ser números'
  c = conn('s51206__ptwikis_p', 's2.labsdb')
  try:
    c.execute(u"""INSERT INTO registro (reg_type, reg_type_id, reg_status, reg_comment, reg_user, reg_timestamp)
VALUES
 (?, ?, ?, ?, ?, DATE_FORMAT(NOW(), '%Y%m%d%H%i%S'))""", (request.args['type']
    , typeid, status, comment, session['user']))
  except Exception as e:
    return repr(e)
  else:
    if u'callback' in request.args:
      return Response(request.args[u'callback'] + '({ "status": "success" })', mimetype='text/javascript')
    else:
      return jsonify(status='success')

def mkCond(cond):
  oper = '='
  if cond[0] in '><' and cond[1:].isdigit():
    oper = cond[0]
    cond = cond[1:]
  elif cond[-1] == '%':
    oper = 'LIKE'
  return (' %s ?' % oper, cond)
