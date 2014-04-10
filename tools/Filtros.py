# -*- coding: utf-8 -*-

from flask import render_template_string, redirect
from database import conn, link

# Gráfico das ações de um filtro no tempo
onefilter = u'''{% extends "base.html" %}
{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='rickshaw/rickshaw.min.css') }}">
<script src="{{ url_for('static', filename='rickshaw/vendor/d3.min.js') }}"></script>
<script src="{{ url_for('static', filename='rickshaw/rickshaw.min.js') }}"></script>

<style> svg {box-shadow: 0 0 3px} </style>
{% endblock %}
{% block content %}
{% if query %}
<div id="graph"></div>

<script>

var data = {
    nada: [],
    etiq: [],
    aviso: [],
    desaut: [],
    raw: {{ query }}
};

for (d in data.raw){
    var time = String(data.raw[d][0]);
    time = Date.UTC(time.substr(0, 4), time.substr(4, 2)-1, time.substr(6, 2))/1000;
    data.nada.push({x: time, y: data.raw[d][1]});
    data.etiq.push({x: time, y: data.raw[d][2]});
    data.aviso.push({x: time, y: data.raw[d][3]});
    data.desaut.push({x: time, y: data.raw[d][4]});
}

var graph = new Rickshaw.Graph( {
    element: document.getElementById("graph"),
    width: 800,
    height: 300,
    renderer: 'line',
    stroke: true,
    preserve: true,
    series: [{% if actions[0] %}{
	name: "{% if link[0:2] == "pt" %}Sem ação{% else %}No action{% endif %}",
        data: data.nada,
        color: '#3F5'
    }, {% endif %}{% if actions[1] %}{
	name: "{% if link[0:2] == "pt" %}Etiquetas{% else %}Tags{% endif %}",
        data: data.etiq,
        color: '#FE1'
    }, {% endif %}{% if actions[2] %}{
	name: "{% if link[0:2] == "pt" %}Avisos{% else %}Warns{% endif %}",
        data: data.aviso,
        color: '#15F'
    }, {% endif %}{% if actions[3] %}{
	name: "{% if link[0:2] == "pt" %}Desautorizações{% else %}Disallows{% endif %}",
        data: data.desaut,
        color: '#D12',
    }{% endif %}]
});

var x_axish = new Rickshaw.Graph.Axis.Time({
    graph: graph,
});

graph.render();

var hoverDetailh = new Rickshaw.Graph.HoverDetail( {
    graph: graph,
    yFormatter: function(y){return Math.floor(y)}
});
</script>
{%- else %}
<span style="color:red"><b>Erro</b></span>
{%- endif %}
{% endblock %}'''

## Gráfico de barra de todos filtros
allfilters = u'''{% extends "base.html" %}
{% block content %}


<p>{% if link[0:2] == "pt" %}Ações de filtros {% if wiki == "Wikipédia" %}na{% else %}no{% endif %} {{ wiki }} nos últimos 30 dias:
{% else %}Filters actions in the last 30 days:{% endif %}</p>
<br/>
<p><b>Legend{% if link[0:2] == "pt" %}a{% endif %}: <span style="background-color:lightgreen">&nbsp; {% if link[0:2] == "pt" %}Correspondências sem ação{% else %}No action{% endif %} &nbsp;</span> 
<span style="background-color:#55F; color:white">&nbsp; {% if link[0:2] == "pt" %}Avisos{% else %}Warn{% endif %} &nbsp;</span> 
<span style="background-color:gold">&nbsp; {% if link[0:2] == "pt" %}Etiquetas{% else %}Tag{% endif %} &nbsp;</span> 
<span style="background-color:red; color:white">&nbsp; {% if link[0:2] == "pt" %}Desautorizações{% else %}Disallow{% endif %} &nbsp;</span></b></p>
  </tr>
{% if filters %}
<table style="width:100%" border=1 rules=rows frame=none bordercolor=lightgray>
{%- for f, t, n, a, e, d in filters %}
<tr>
  <td style="width:50px; font-size:1.8em; margin:5px 5px 5px 5px">
    <a href="//{{ link }}.org/wiki/{% if link[0:2] == "pt" %}Especial:Filtro_de_abusos{% else %}Special:AbuseFilter{% endif %}/{{ f }}" title="{{ t }}">{{ f }}</a>
  </td>
  <td style="font-size:x-small">{% if n %}
    <div style="width:{{ (n * 100 / max)|round(1) }}%; height:10px; background-color:lightgreen" title="{{ n }} {% if link[0:2] == "pt" %}correspondências sem ação sobre{% else %}no action matches about{% endif %} {{ t|lower }}"></div>{% endif %}{% if a %}
    <div style="width:{{ (a * 100 / max)|round(1) }}%; height:10px; background-color:#55F" title="{{ a }} {% if link[0:2] == "pt" %}avisos sobre{% else %}warns about{% endif %} {{ t|lower }}"></div>{% endif %}{% if e %}
    <div style="width:{{ (e * 100 / max)|round(1) }}%; height:10px; background-color:gold" title="{{ e }} {% if link[0:2] == "pt" %}etiquetas sobre{% else %}tags about{% endif %} {{ t|lower }}"></div>{% endif %}{% if d %}
    <div style="width:{{ (d * 100 / max)|round(1) }}%; height:10px; background-color:red" title="{{ d }} {% if link[0:2] == "pt" %}desautorizações sobre{% else %}disallows about{% endif %} {{ t|lower }}"></div>{% endif %}
  </td>
  <td style="font-size:0.8em; width:8px">
    <script>document.write('<a href="' + location.href + ':{{ f }}" title="{% if link[0:2] == "pt" %}Gráfico do filtro {{ f }}{% else %}Filter {{ f }} graph{% endif %}"><b>G</b></a>')</script>
  </td>
</tr>
{%- endfor %}
</table>
{% else %}
ERRO
{% endif %}
<select style="margin:1em auto 2em auto; border:1px solid #A7D7F9; background-color:#F6F6F6" onchange="location.href = location.href.substring(0, location.href.lastIndexOf('/')) + '/Filtros:' + this.value">
  <option value="">Escolha outro projeto</option>
  <option>Wikipédia</option>
  <option>Wikilivros</option>
  <option>Wikcionário</option>
  <option>Wikiversidade</option>
  <option>Wikinotícias</option>
  <option>Wikiquote</option>
  <option>Wikisource</option>
  <option>Wikivoyage</option>
</select>
{% endblock %}
'''

def main(args=None):
    if not args:
        wiki, filter = u'Wikipédia', None
    elif args.isdigit():
        wiki, filter = u'Wikipédia', args
    elif args.split(':')[0] not in (u'Wikipédia', u'Wikilivros', u'Wikinotícias', u'Wikicionário', u'Wikiversidade', u'Wikiquote', u'Wikisource', u'Wikivoyage'):
	return redirect('https://tools.wmflabs.org/ptwikis/Filters:' + args)
    else:
        args = args.split(u':')
        wiki, filter = args[0], len(args) > 1 and args[1]
    c = conn(wiki)
    if c and not filter: # Todos os filtros
        c.execute('''SELECT
 F,
 af_public_comments,
 N,
 A,
 E,
 D
 FROM (
 SELECT
 afl_filter AS F,
 SUM(CASE WHEN afl_actions = '' THEN 1 ELSE 0 END) AS N,
 SUM(CASE WHEN afl_actions = 'warn' THEN 1 ELSE 0 END) AS A,
 SUM(CASE WHEN afl_actions = 'tag' THEN 1 ELSE 0 END) AS E,
 SUM(CASE WHEN afl_actions = 'disallow' THEN 1 ELSE 0 END) AS D
 FROM abuse_filter_log
 WHERE afl_timestamp > DATE_FORMAT(SUBDATE(NOW(), INTERVAL 30 DAY), '%Y%m%d%H%i%s')
 GROUP BY afl_filter) AS stats
 LEFT JOIN abuse_filter
 ON F = af_id
 ORDER BY CAST(F AS INT)''')
        r = c.fetchall()
        r = [(int(f), t and t.decode('utf8') or u'', int(n), int(a), int(e), int(d)) for f, t, n, a, e, d in r]
        r = {'wiki': wiki, 'link': link(wiki), 'filters': r, 'max': max(map(max, [f[2:] for f in r]))}
	return render_template_string(allfilters, title=r['link'][0:2] == 'pt' and 'Filtros' or 'Filters', **r)
    elif c and filter: # Um filtro ao longo do tempo
        c.execute('''SELECT
 SUBSTR(afl_timestamp, 1, 8) mês,
 SUM(afl_actions = '') nada,
 SUM(afl_actions = 'tag') etiq,
 SUM(afl_actions = 'warn') aviso,
 SUM(afl_actions = 'disallow') desaut
 FROM abuse_filter_log
 WHERE afl_filter = ? AND afl_timestamp LIKE '2013%'
 GROUP BY WEEK(afl_timestamp)''', (filter,))
        r = c.fetchall()
	c.execute('SELECT af_public_comments FROM abuse_filter WHERE af_id = ?', (filter,))
	title = c.fetchone()
	r = {'wiki': wiki, 'link': link(wiki), 'query': [map(int, l) for l in r]}
	r['actions'] = map(max, zip(*r['query'])[1:])
	title = (r['link'][0:2] == 'pt' and 'Filtro ' or 'Filter ') + filter + u' – ' + title[0].decode('utf-8') 
	return render_template_string(onefilter, title=title, **r)
    else:
        r = {}
        return render_template_string(allfilters, title=u'Filtros', **r)
