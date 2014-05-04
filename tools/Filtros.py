# -*- coding: utf-8 -*-

from flask import render_template_string, redirect
from database import conn, link

# Gráfico das ações de um ou mais filtros no tempo
filtergraph = u'''{% extends "base.html" %}
{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='rickshaw/rickshaw.min.css') }}">
<script src="{{ url_for('static', filename='rickshaw/vendor/d3.min.js') }}"></script>
<script src="{{ url_for('static', filename='rickshaw/rickshaw.min.js') }}"></script>

<style> svg {box-shadow: 0 0 3px} </style>
{% endblock %}
{% block content %}
{% if filters %}
<div id="graph"></div>
<div style= "margin:20px 10px 10px 10px" id="legend"></div>

<script>

var filters = { {% for f, query in filters.iteritems()  %}
  {{ f }}: {{ query }}{% if loop.revindex != 1 %},{% endif %}
{%- endfor %}
};{% if 1 != filters|length %}
var names = { {% for f, name in names.iteritems() %}
  {{ f }}: "{{ name }}"{% if loop.revindex != 1 %},{% endif %}
{%- endfor %}
};
var colors = [['#FFA', '#FE5', '#FD0', '#A90'], ['#AFA', '#5F5', '#0F0', '#0A0'], ['#AAF', '#55F', '#00F', '#00A'], ['#FBB', '#F77', '#F00', '#A00']];
{%- else %}
var colors = [['#3F5', '#FE1', '#15F', '#D12']];
{%- endif %}
var legend = document.getElementById('legend');
var series = [];

for (var f in filters){
    var data = [[], [], [], []];
    var action = [0, 0, 0, 0];
    var color = colors.pop();
    for (var d in filters[f]){
        var time = String(filters[f][d][0]);
        time = Date.UTC(time.substr(0, 4), time.substr(4, 2)-1, time.substr(6, 2))/1000;
        data[0].push({x: time, y: filters[f][d][1]});
        data[1].push({x: time, y: filters[f][d][2]});
        data[2].push({x: time, y: filters[f][d][3]});
        data[3].push({x: time, y: filters[f][d][4]});
        action = [action[0] || filters[f][d][1], action[1] || filters[f][d][2], action[2] || filters[f][d][3], action[3] || filters[f][d][4]];
    }
    for (var a=0; a<4; a++){
        if (action[a]){
            series.push({name: 'Filtro ' + f + ':' + ['Sem ação', 'Etiquetas', 'Avisos', 'Desautorizações'][a], data: data[a], color: color[a]});
{%- if 1 != filters|length %}
            legend.innerHTML += '<span style="display:inline-block; width:40px; height:6px; border-bottom:5px solid ' +
                color[a] + '">&nbsp;</span> '  + names[f] + ' – ' + ['Sem ação', 'Etiquetas', 'Avisos', 'Desautorizações'][a] + '<br/>';
{%- endif %}
        }
    }
}

var graph = new Rickshaw.Graph( {
    element: document.getElementById("graph"),
    width: 800,
    height: 300,
    renderer: 'line',
    stroke: true,
    preserve: true,
    series: series
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
    elif args.replace(u'&', u'').isdigit():
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
	return render_template_string(allfilters, title='Filtros', **r)
    elif c and filter: # Um ou mais filtros ao longo do tempo
        query = '''SELECT
 SUBSTR(afl_timestamp, 1, 8) dia,
 SUM(afl_actions = '') nada,
 SUM(afl_actions = 'tag') etiq,
 SUM(afl_actions = 'warn') aviso,
 SUM(afl_actions = 'disallow') desaut
 FROM abuse_filter_log
 WHERE afl_filter = ? AND afl_timestamp > DATE_FORMAT(SUBDATE(NOW(), INTERVAL 1 YEAR), '%Y%m%d%H%i%s')
 GROUP BY WEEK(afl_timestamp)
 ORDER BY dia'''
        filter = filter.split('&')
        filters, names = {}, {}
        for f in filter[0:4]:
            c.execute(query, (f,))
            r = c.fetchall()
            filters[f] = [map(int, l) for l in r]
	    c.execute('SELECT af_public_comments FROM abuse_filter WHERE af_id = ?', (filter[0],))
	    names[f] = 'Filtro ' + f + u' – ' + c.fetchone()[0].decode('utf-8')
        title = len(filter) == 1 and names[filter[0]] or ' + '.join(['Filtro ' + f for f in filter[0:4]])
	r = {'wiki': wiki, 'link': link(wiki), 'filters': filters, 'names': names}
	return render_template_string(filtergraph, title=title, **r)
    else:
        r = {}
        return render_template_string(allfilters, title=u'Filtros', **r)
