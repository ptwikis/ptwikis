# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn, link

page = u'''
{% extends "base.html" %}
{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='rickshaw/rickshaw.min.css') }}">
<script src="{{ url_for('static', filename='rickshaw/vendor/d3.min.js') }}"></script>
<script src="{{ url_for('static', filename='rickshaw/rickshaw.min.js') }}"></script>

<style> svg {box-shadow: 0 0 3px} </style>
{% endblock %}
{% block content %}
<p>
<label for="artigo">Artigo:</label>
<input id="artigo" type="text" size=20 onkeypress="return enter(event)"/>
</p>
<p style="font-size:small">Evolução do tamanho do artigo {{ artigo|replace('_', ' ') }}.</p>
{% if query %}
<div id="chart"></div>

<script>
function enter(e) {
    if (e.keyCode == 13) {
	var value = document.getElementById('artigo').value.replace(/ /g, "_");
	location.pathname = location.pathname.substring(0,location.pathname.indexOf("/", 1)) + "/Evolução:" + value;
        return false;
    }
}

var data = {
    size: [],
    raw: {{ query|string }} };

for (d in data.raw){
    var time = String(data.raw[d][0]);
    time = Date.UTC(time.substr(0, 4), time.substr(4, 2), 1)/1000;
    data.size.push({x: time, y: data.raw[d][1]});
}

var graph = new Rickshaw.Graph( {
    element: document.getElementById("chart"),
    width: 800,
    height: 300,
    renderer: 'line',
    stroke: true,
    preserve: true,
    series: [{
        name: "Tamanho do artigo",
        data: data.size,
        color: '#CD2C49'
    }]
});

var x_axis = new Rickshaw.Graph.Axis.Time({
    graph: graph,
});

graph.render();

var hoverDetail = new Rickshaw.Graph.HoverDetail( {
    graph: graph,
    xFormatter: function(x){
        var d = new Date(x * 1000);
        return String(d.getUTCMonth()) + '/' + String(d.getUTCFullYear())
    },
    yFormatter: function(y){return String(y) + ' bytes'}
});
</script>
{%- else %}
<span style="color:red"><b>Erro</b></span>
{%- endif %}
{% endblock %}
'''

def main(artigo=None):
    if not artigo:
        artigo = u'Wikipédia'
    c = conn(u'Wikipédia')
    if c:
        c.execute('''SELECT
 SUBSTR(rev_timestamp, 1, 6) mes,
 MAX(rev_len) tamanho
 FROM page
 INNER JOIN revision ON rev_page = page_id
 WHERE page_namespace = 0 AND page_title = ?
 GROUP BY mes''', (artigo,))
        r = c.fetchall()
        r = {'artigo': artigo, 'query': [map(int, l) for l in r]}
    else:
        r = {}
    return render_template_string(page, title=u'Evolução do artigo ' + artigo, **r)
