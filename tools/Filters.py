# -*- coding: utf-8 -*-

from flask import render_template_string
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
<span style="color:red"><b>Error</b></span>
{%- endif %}
{% endblock %}'''

## Gráfico de barra de todos filtros
allfilters = u'''{% extends "Tools.html" %}
{% block content %}

<p>Filters actions in the last 30 days:</p>
<br/>
<p><b>Legend: <span style="background-color:lightgreen">&nbsp; No action match &nbsp;</span> 
<span style="background-color:#55F; color:white">&nbsp; Warn &nbsp;</span> 
<span style="background-color:gold">&nbsp; Tag &nbsp;</span> 
<span style="background-color:red; color:white">&nbsp; Disallow &nbsp;</span></b></p>
  </tr>
{% if filters %}
<table style="width:100%" border=1 rules=rows frame=none bordercolor=lightgray>
{%- for f, t, n, a, e, d in filters %}
<tr>
  <td style="width:50px; font-size:1.8em; margin:5px 5px 5px 5px">
    <a href="//{{ link }}.org/wiki/Special:AbuseFilter/{{ f }}" title="{{ t }}">{{ f }}</a>
  </td>
  <td style="font-size:x-small">{% if n %}
    <div style="width:{{ (n * 100 / max)|round(1) }}%; height:10px; background-color:lightgreen" title="{{ n }} no action matches about {{ t|lower }}"></div>{% endif %}{% if a %}
    <div style="width:{{ (a * 100 / max)|round(1) }}%; height:10px; background-color:#55F" title="{{ a }} warns about {{ t|lower }}"></div>{% endif %}{% if e %}
    <div style="width:{{ (e * 100 / max)|round(1) }}%; height:10px; background-color:gold" title="{{ e }} tags about {{ t|lower }}"></div>{% endif %}{% if d %}
    <div style="width:{{ (d * 100 / max)|round(1) }}%; height:10px; background-color:red" title="{{ d }} disallows about {{ t|lower }}"></div>{% endif %}
  </td>
  <td style="font-size:0.8em; width:8px">
    <script>document.write('<a href="' + location.href + ':{{ f }}" title="Filter {{ f }} graph"><b>G</b></a>')</script>
  </td>
</tr>
{%- endfor %}
</table>
{% else %}
ERROR
{% endif %}
{% endblock %}
'''

# Página principal da ferramenta
mainpage = u'''{% extends "Tools.html" %}
{% block head %}
<script>
function wikichoose(){
  var lang = document.getElementById('lang');
  var wiki = document.getElementById('wiki').value;
  if (wiki == 'metawiki' || wiki == 'commonswiki' || wiki == 'wikidatawiki') {
    lang.value = '';
    lang.disabled = true;
  } else if (lang.disabled == true) {
  lang.disabled = false;
  }
}
function go(){
  var lang = document.getElementById('lang').value;
  var wiki = document.getElementById('wiki').value;
  location.href = 'https://tools.wmflabs.org/ptwikis/Filters:' + lang + wiki;
  return false;
}
</script>
{% endblock %}
{% block content %}

<p>Graphs of Abuse Filter actions.</p>
<p>Choose a wiki: <input id="lang" type="text" size=2 onkeypress="return enter(event, this, 'Filters:')"/>
<select id="wiki" style="margin-top:1em; border:1px solid #DDDDDD; background-color:#F6F6F6" onchange="wikichoose()">
  <option value="wiki">Wikipedia</option>
  <option value="wikibooks">Wikibooks</option>
  <option value="wikitionary">Wikitionary</option>
  <option value="wikiiversity">Wikiiversity</option>
  <option value="wikiinews">Wikiinews</option>
  <option value="wikiiquote">Wikiiquote</option>
  <option value="wikiisource">Wikiisource</option>
  <option value="wikiivoyage">Wikiivoyage</option>
  <option value="metawiki">Meta-Wiki</option>
  <option value="wikidatawiki">Wikidata</option>
  <option value="commonswiki">Commons</option>
</select>
<input type="button" onclick="go()" value="Go"/></p>
{% endblock %}
'''

def main(args=None):
    if not args:
	return render_template_string(mainpage, title='Abuse Filter Graphs')
    elif args.isdigit():
        wiki, filter = u'ptwiki', args
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
	return render_template_string(allfilters, title=wiki + ' Abuse Filter Graphs', **r)
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
	title = 'Filter ' + filter + ' at ' + wiki + u' – ' + title[0].decode('utf-8') 
	return render_template_string(onefilter, title=title, **r)
    else:
        r = {}
        return render_template_string(allfilters, title='Abuse Filter Graphs', **r)
