# -*- coding: utf-8 -*-

from flask import render_template_string, redirect
from database import conn, link

# Gráfico das ações de um ou mais filtros no tempo
filtergraph = u'''{% extends "base.html" %}
{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='rickshaw/rickshaw.min.css') }}">
<script src="{{ url_for('static', filename='rickshaw/vendor/d3.min.js') }}"></script>
<script src="{{ url_for('static', filename='rickshaw/rickshaw.min.js') }}"></script>

<style> #graph svg {box-shadow: 0 0 3px} </style>
{% endblock %}
{% block content %}
{% if filters %}
<div id="graph"></div>{% if 1 != filters|length %}
<svg width="800" height="30"><g stroke="black" stroke-width="2">
  <path stroke-dasharray="2,2" d="M20 10 l45 0" />
  <path stroke-dasharray="4,4" d="M210 10 l45 0" />
  <path stroke-dasharray="2,2,8,2" d="M400 10 l45 0" />
  <path d="M590 10 l45 0" />
</g>
<g fill="black">
  <text x="70" y="15">Sem ação</text>
  <text x="260" y="15">Etiquetas</text>
  <text x="450" y="15">Avisos</text>
  <text x="640" y="15">Desautorizações</text>
</g></svg>{% endif %}
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
var palette = new Rickshaw.Color.Palette({scheme: 'munin'});
{%- else %}
var colors = ['#3F5', '#FE1', '#15F', '#D12'];
{%- endif %}
var legend = document.getElementById('legend');
var series = [];

for (var f in filters){
    var data = [[], [], [], []];
    var action = [0, 0, 0, 0];{% if 1 != filters|length %}
    var color = palette.color();{% endif %}
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
            series.push({name: 'Filtro ' + f + ':' + ['Sem ação', 'Etiquetas', 'Avisos', 'Desautorizações'][a], data: data[a], color: color{% if 1 == filters|length %}s[a]{% endif %}});
        }
    }
{%- if 1 != filters|length %}
    legend.innerHTML += '<span style="display:inline-block; width:40px; height:3px; border-top:4px solid ' +
        color + '"></span> <a href="//{{ link }}.org/wiki/Especial:Filtro_de_abusos/' + f + '">' + names[f] + '</a><br/>';
{%- endif %}
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

graph.render();{% if 1 != filters|length %}
graph.series.forEach(function(series){ switch (series.name.substr(series.name.indexOf(':'))){
    case ':Sem ação':
        series.path.setAttribute('stroke-dasharray', '2,2');
        break;
    case ':Etiquetas':
        series.path.setAttribute('stroke-dasharray', '4,4');
        break;
    case ':Avisos':
        series.path.setAttribute('stroke-dasharray', '2,2,8,2');
}});{% endif %}

var hoverDetailh = new Rickshaw.Graph.HoverDetail( {
    graph: graph,
    xFormatter: function(x){
        var d = new Date(x * 1000);
        var d2 = new Date((x + 518400) * 1000);
        return d.toLocaleDateString() + ' – ' + d2.toLocaleDateString();},
    yFormatter: function(y){return Math.floor(y)}
});
</script>
{%- else %}
<span style="color:red"><b>Erro</b></span>
{%- endif %}
{% endblock %}'''

## Gráfico de barra de todos filtros
allfilters = u'''{% extends "base.html" %}
{% block head %}
        <script src="//tools-static.wmflabs.org/cdnjs/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <style>.selected td {background-color: #FFE}</style>
        <script>
var filters = [];

function checkchange(checkbox){
  var tr = checkbox.parentNode.parentNode;
  if (!checkbox.checked && tr.className == "selected"){
    tr.className = "";
    filters.splice(filters.indexOf(checkbox.name), 1);
  }else if(checkbox.checked && !tr.className){
    tr.className = "selected";
    filters.push(checkbox.name);
  }
  buttoncheck();
}
function showgraph(){
  location.href = location.href + ':' + filters.sort().join('&');
}
function buttoncheck(){
  var disable = !filters.length;
  $(":button").each(function(i, elem){ elem.disabled = disable });
}
$(document).ready(function(){
  $("input").each(function(i, elem){
    if (elem.type == "checkbox" && elem.checked){
      elem.parentNode.parentNode.className = "selected";
      filters.push(elem.name);
    }
  });
  buttoncheck();
});
        </script>
{% endblock %}
{% block content %}


<p>Ações de filtros {% if wiki == "Wikipédia" %}na{% else %}no{% endif %} {{ wiki }} nos últimos 30 dias:</p>
<br/>
<p style="float:left"><b>Legenda: <span style="background-color:lightgreen">&nbsp; Correspondências sem ação &nbsp;</span> 
<span style="background-color:#55F; color:white">&nbsp; Avisos &nbsp;</span> 
<span style="background-color:gold">&nbsp; Etiquetas &nbsp;</span> 
<span style="background-color:red; color:white">&nbsp; Desautorizações &nbsp;</span></b></p>
{% if filters %}
<input type="button" style="float:right; margin-top:20px" value="Ver gráfico" onclick="showgraph()">
<table style="width:100%" border=1 rules=rows frame=none bordercolor=lightgray>
{%- for f, t, n, a, e, d in filters %}
<tr>
  <td style="width:50px; font-size:1.8em; margin:5px 5px 5px 5px">
    <a href="//{{ link }}.org/wiki/Especial:Filtro_de_abusos/{{ f }}" title="{{ t }}">{{ f }}</a>
  </td>
  <td style="font-size:x-small">{{ t }}{% if n %}
    <div style="width:{{ (n * 100 / max)|round(1) }}%; height:10px; background-color:lightgreen" title="{{ n }} correspondências sem ação sobre {{ t|lower }}"></div>{% endif %}{% if a %}
    <div style="width:{{ (a * 100 / max)|round(1) }}%; height:10px; background-color:#55F" title="{{ a }} avisos sobre {{ t|lower }}"></div>{% endif %}{% if e %}
    <div style="width:{{ (e * 100 / max)|round(1) }}%; height:10px; background-color:gold" title="{{ e }} etiquetas sobre {{ t|lower }}"></div>{% endif %}{% if d %}
    <div style="width:{{ (d * 100 / max)|round(1) }}%; height:10px; background-color:red" title="{{ d }} desautorizações sobre {{ t|lower }}"></div>{% endif %}
  </td>
  <td style="font-size:0.8em; width:8px">
    <input type="checkbox" onchange="checkchange(this)" name="{{ f }}" />
  </td>
</tr>
{%- endfor %}
</table>
<input type="button" style="float:right" value="Ver gráfico" onclick="showgraph()">
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
    elif args.replace(u'&', u'').replace(u'_', u'').isdigit():
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
 SUM(afl_actions = '') AS N,
 SUM(afl_actions = 'warn') AS A,
 SUM(afl_actions = 'tag') AS E,
 SUM(afl_actions = 'disallow') AS D
 FROM abuse_filter_log
 WHERE afl_timestamp > DATE_FORMAT(SUBDATE(NOW(), INTERVAL 30 DAY), '%Y%m%d%H%i%s')
 GROUP BY afl_filter) AS stats
 LEFT JOIN abuse_filter
 ON F = af_id''')
        r = c.fetchall()
        r = [(f, t and t.decode('utf8') or u'', int(n), int(a), int(e), int(d)) for f, t, n, a, e, d in r]
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
        filter = [f for f in filter.split('&') if f][0:10]
        filters, names = {}, {}
        for f in filter:
            c.execute(query, (f,))
            r = c.fetchall()
            filters[f] = []
            for l in r:
              if l[0][4:] == '0101' and filters[f] and int(str(filters[f][-1][0])[4:]) > 1225:
                filters[f][-1] = [filters[f][-1][0]] + [int(l[i]) + filters[f][-1][i] for i in range(1, 5)]
              else:
                filters[f].append(map(int, l))
	    c.execute('SELECT af_public_comments FROM abuse_filter WHERE af_id = ?', (f,))
	    names[f] = 'Filtro ' + f + u' – ' + c.fetchone()[0].decode('utf-8').replace(u'"', u'\\"')
        title = len(filter) == 1 and names[filter[0]] or ' + '.join(['Filtro ' + f for f in filter])
	r = {'wiki': wiki, 'link': link(wiki), 'filters': filters, 'names': names}
	return render_template_string(filtergraph, title=title, **r)
    else:
        r = {}
        return render_template_string(allfilters, title=u'Filtros', **r)
