# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn
from time import strftime

page = u'''
{% extends "base.html" %}
{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='rickshaw/rickshaw.min.css') }}">
<script src="{{ url_for('static', filename='rickshaw/vendor/d3.min.js') }}"></script>
<script src="{{ url_for('static', filename='rickshaw/rickshaw.min.js') }}"></script>

<style> svg {box-shadow: 0 0 3px} </style>
<script>
function enter(e) {
    if (e.keyCode == 13) {
	var value = document.getElementById('artigo').value.replace(/ /g, "_");
	location.pathname = location.pathname.substring(0,location.pathname.indexOf("/", 1)) + "/Evolução:" + value;
        return false;
    }
}
</script>
{% endblock %}
{% block content %}
<p>
<label for="artigo">Artigo:</label>
<input id="artigo" type="text" size=20 onkeypress="return enter(event)"/>
</p>
<p style="font-size:small">Evolução do tamanho {% if cat %}dos artigos da{% else %}do artigo{% endif %} {{ artigo|replace('_', ' ') }}.</p>
{% if query %}
<div id="chart"></div>

<script>
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
        name: "Tamanho {% if cat %}dos artigos somados{% else %}do artigo{% endif %}",
        data: data.size,
        color: '#149'
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
        return String(d.getUTCMonth() + 1) + '/' + String(d.getUTCFullYear())
    },
    yFormatter: function(y){return String(y) + ' bytes'}
});
</script>
{%- else %}
<span style="color:red"><b>{{ aviso or 'Erro' }}</b></span>
{%- endif %}
{% endblock %}
'''

def main(artigo=None):
    if not artigo:
        artigo = u'Wikipédia'
    cat = artigo.split(u':')[0].lower() == u'categoria'
    c = conn(u'Wikipédia')
    if c:
        if cat:
            c.execute("SELECT cl_from FROM categorylinks WHERE cl_to = ? AND cl_type = 'page'", (artigo.split(u':')[1],))
            ids = [int(l[0]) for l in c.fetchall()]
            if len(ids) > 300:
                return render_template_string(page, title=u'Evolução dos artigos da ' + artigo,
                    aviso=u'Muitos artigos na categoria, consulta abortada')
            c.execute('''SELECT
 rev_page,
 SUBSTR(rev_timestamp, 1, 6) mes,
 FLOOR(AVG(rev_len)) tamanho
 FROM revision
 WHERE rev_page IN (%s)
 GROUP BY rev_page, mes''' % ','.join(str(i) for i in ids))
            r = c.fetchall()
            r = [i for p in {l[0] for l in r} for i in complete([(l[1], l[2]) for l in r if l[0] == p])]
            r = [(m, sum(l[1] for l in r if l[0] == m)) for m in sorted({l[0] for l in r})]
            r = {'artigo': artigo, 'query': [map(int, l) for l in r], 'cat': cat}
        else:
            c.execute('''SELECT
 SUBSTR(rev_timestamp, 1, 6) mes,
 FLOOR(AVG(rev_len)) tamanho
 FROM page
 INNER JOIN revision ON rev_page = page_id
 WHERE page_namespace = 0 AND page_title = ?
 GROUP BY mes''', (artigo,))
            r = c.fetchall()
            r = {'artigo': artigo, 'query': [map(int, l) for l in complete(r)], 'cat': cat}
    else:
        r = {}
    title = u'Evolução ' + (cat and u'dos artigos da ' or u'do artigo ') + artigo
    return render_template_string(page, title=title, **r)

def complete(sizes):
    sizes.sort()
    year = int(sizes[0][0][0:4])
    month = int(sizes[0][0][4:6])
    maxmonth = strftime('%Y%m')
    completed = [sizes.pop(0)]
    while True:
        if month == 12:
            year, month = year + 1, 1
        else:
            month += 1
        nextmonth = '%d%02d' % (year, month)
        if int(nextmonth) > int(maxmonth):
            raise Exception('Erro ao completar meses (%s)' % nextmonth)
        if sizes and sizes[0][0] == nextmonth:
            completed.append(sizes.pop(0))
        else:
            completed.append((nextmonth, completed[-1][1]))
        if nextmonth == maxmonth:
            break
    return completed
