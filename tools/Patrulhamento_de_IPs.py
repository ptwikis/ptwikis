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
{% if wiki == "Wikipédia" %}<p style="font-size:small">O gráfico a seguir se refere às <span style="color:#B44">edições de IPs</span>, <span style="color:#4B4">edições de IPs patrulhadas</span> (<span style="color:#47B">porcentagem</span>) e <span style="color:#B0B">edições revertidas</span>* no domínio principal da Wikipédia nos últimos 7 dias.</p>
{% else %}<p style="font-size:small">O gráfico a seguir se refere às <span style="color:#B44">edições de IPs</span> e <span style="color:#4B4">edições de IPs patrulhadas</span> (<span style="color:#47B">porcentagem</span>) no domínio principal do {{ wiki }} nos últimos 7 dias.</p>{% endif %}
{% if iphquery %}
<div id="iph"></div>
<br/><br/><p>Gráfico para os últimos 30 dias:</p>
<div id="ipd"></div>
{% if wiki == "Wikipédia" %}<p>* As reversões são obtidas pelo sumário da edição ("Foram [[WP:REV|..." e "Reversão de uma ou mais edições de..."), o número não é totalmente preciso.</p>{% endif %}

<script>

var data = {
    iph: [],
    iphpatrol: [],
    iphpatrolratio: [],
    iphrev: [],
    iphmax: 0,
    iphraw: [
{{ iphquery }}
],
    ipd: [],
    ipdpatrol: [],
    ipdpatrolratio: [],
    ipdrev: [],
    ipdmax: 0,
    ipdraw: [
{{ ipdquery }}
]};

for (d in data.iphraw.reverse()){
    var time = String(data.iphraw[d][0]);
    time = Date.UTC(time.substr(0, 4), time.substr(4, 2)-1, time.substr(6, 2), time.substr(8, 2))/1000;
    data.iph.push({x: time, y: data.iphraw[d][1]});
    data.iphpatrol.push({x: time, y: data.iphraw[d][2]});
    data.iphpatrolratio.push({x: time, y: Math.round(100*data.iphraw[d][2] / data.iphraw[d][1])});
{% if wiki == "Wikipédia" %}    data.iphrev.push({x: time, y: data.iphraw[d][3]}){% endif %}
    data.iphmax = Math.max(data.iphmax, data.iphraw[d][1])
}
for (d in data.ipdraw.reverse()){
    var time = String(data.ipdraw[d][0]);
    time = Date.UTC(time.substr(0, 4), time.substr(4, 2)-1, time.substr(6, 2))/1000;
    data.ipd.push({x: time, y: data.ipdraw[d][1]});
    data.ipdpatrol.push({x: time, y: data.ipdraw[d][2]});
    data.ipdpatrolratio.push({x: time, y: Math.round(100*data.ipdraw[d][2] / data.ipdraw[d][1])});
{% if wiki == "Wikipédia" %}    data.ipdrev.push({x: time, y: data.ipdraw[d][3]}) {% endif %}
    data.ipdmax = Math.max(data.ipdmax, data.ipdraw[d][1])
}

var graphh = new Rickshaw.Graph( {
    element: document.getElementById("iph"),
    width: 800,
    height: 300,
    renderer: 'line',
    stroke: true,
    preserve: true,
    series: [{
        name: "Edições de IPs",
        data: data.iph,
        color: '#B44'
    }, {
        name: "Edições de IPs patrulhadas",
        data: data.iphpatrol,
        color: '#4B4'
    }, {
        name: "Percentual de edições de IPs patrulhadas",
        data: data.iphpatrolratio,
        color: '#47B',
        scale: d3.scale.linear().domain([0, 100 / data.iphmax])
{% if wiki == "Wikipédia" %}    }, {
        name: "Edições revertidas*",
        data: data.iphrev,
        color: '#B0B',{% endif %}
    }]
});

var graphd = new Rickshaw.Graph( {
    element: document.getElementById("ipd"),
    width: 800,
    height: 300,
    renderer: 'line',
    stroke: true,
    preserve: true,
    series: [{
        name: "Edições de IPs",
        data: data.ipd,
        color: '#B44'
    }, {
        name: "Edições de IPs patrulhadas",
        data: data.ipdpatrol,
        color: '#4B4'
    }, {
        name: "Percentual de edições de IPs patrulhadas",
        data: data.ipdpatrolratio,
        color: '#47B',
        scale: d3.scale.linear().domain([0, 100 / data.ipdmax])
{% if wiki == "Wikipédia" %}    }, {
        name: "Edições revertidas*",
        data: data.ipdrev,
        color: '#B0B'{% endif %}
    }]
});

var x_axish = new Rickshaw.Graph.Axis.Time({
    graph: graphh,
});

var x_axisd = new Rickshaw.Graph.Axis.Time({
    graph: graphd,
});

graphh.render();

graphd.render();

var hoverDetailh = new Rickshaw.Graph.HoverDetail( {
    graph: graphh,
    xFormatter: function(x){
        var d = new Date(x * 1000);
        var h = String(d.getUTCHours());
        return h + 'h&ndash;' + h + 'h59 de ' + String(d.getUTCDate()) + '/' + String(d.getUTCMonth()+1) + '/' + String(d.getUTCFullYear())
    },
    yFormatter: function(y){return Math.floor(y)}
});

var hoverDetaild = new Rickshaw.Graph.HoverDetail( {
    graph: graphd,
    xFormatter: function(x){
        var d = new Date(x * 1000);
        return String(d.getUTCDate()) + '/' + String(d.getUTCMonth()+1) + '/' + String(d.getUTCFullYear())
    },
    yFormatter: function(y){return Math.floor(y)}
});
</script>
{%- else %}
<span style="color:red"><b>Erro</b></span>
{%- endif %}
<select style="margin:1em auto 2em auto; border:1px solid #A7D7F9; background-color:#F6F6F6" onchange="location.href = location.href.substring(0, location.href.lastIndexOf('/')) + '/Patrulhamento_de_IPs:' + this.value">
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

def main(wiki=None):
    if not wiki:
        wiki = u'Wikipédia'
    c = conn(wiki)
    if c:
        c.execute('''SELECT
 SUBSTR(rc_timestamp, 1, 10) AS HORA,
 SUM(CASE WHEN rc_user = 0 THEN 1 ELSE 0 END),
 SUM(CASE WHEN rc_user = 0 THEN rc_patrolled ELSE 0 END),
 SUM(CASE WHEN rc_comment LIKE ? OR rc_comment LIKE ? OR rc_comment LIKE ? THEN 1 ELSE 0 END)
 FROM recentchanges
 WHERE rc_namespace = 0 AND rc_type != 5
 GROUP BY HORA
 ORDER BY rc_id DESC
 LIMIT 168''', ('[[WP:REV|%', 'Foram [[WP:REV|%', u'Reversão de uma ou mais edições de%'))
        r1 = c.fetchall()
        c.execute('''SELECT
 SUBSTR(rc_timestamp, 1, 8) AS DIA,
 SUM(CASE WHEN rc_user = 0 THEN 1 ELSE 0 END),
 SUM(CASE WHEN rc_user = 0 THEN rc_patrolled ELSE 0 END),
 SUM(CASE WHEN rc_comment LIKE ? OR rc_comment LIKE ? THEN 1 ELSE 0 END)
 FROM recentchanges
 WHERE rc_namespace = 0 AND rc_type != 5
 GROUP BY DIA
 ORDER BY rc_id DESC''', ('Foram [[WP:REV|%', u'Reversão de uma ou mais edições de%'))
        r2 = c.fetchall()
        r = {'wiki': wiki, 'link': link(wiki)}
	r['iphquery'] = ','.join([(x in r1[6::6] and '\n[{},{},{},{}]' or '[{},{},{},{}]').format(*x) for x in r1])
	r['ipdquery'] = ','.join([(x in r2[6::6] and '\n[{},{},{},{}]' or '[{},{},{},{}]').format(*x) for x in r2][1:-1])
    else:
        r = {}
    return render_template_string(page, title=u'Patrulhamento de IPs' + (wiki and u': ' + wiki or u''), **r)

