# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn

page = u'''
{% extends "Tools.html" %}
{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='rickshaw/rickshaw.min.css') }}">
<script src="{{ url_for('static', filename='rickshaw/vendor/d3.min.js') }}"></script>
<script src="{{ url_for('static', filename='rickshaw/rickshaw.min.js') }}"></script>

<style>
  svg {box-shadow: 0 0 3px}
  table th{border-bottom:2px solid #555; padding:2px 5px 2px 5px}
  table td{padding:5px 2px 5px 2px; border-bottom:1px solid #DDD}
</style>
{% endblock %}
{% block content %}
<p>Graph of uploads in Wiki Loves Earth 2014 campaign.
{% if query %}
<div id="graph"></div>
<table id="countries" style="text-align:center; border-collapse:collapse; min-width:800px; margin-top:8px">
 <tr>
  <th></th>
  <th>Country</th>
  <th>Images</th>
  <th>Images used<br/>in the wikis</th>
  <th>Uploaders</th>
  <th>Uploaders regitered<br/>in May 2014</th></tr>
</table>
<script>

var series = [
  {{ query }}
];
series = series.sort(function(a, b){return b.data.slice(-1)[0].y - a.data.slice(-1)[0].y})
var palette = new Rickshaw.Color.Palette({scheme: 'munin'});
var contries = document.getElementById('countries');
for (var i = 0; i < series.length; i++){
  series[i]['color'] = palette.color(i);
  var uploads = series[i].data.slice(-1)[0].y;
  countries.innerHTML += '\\n<tr><td><span style="display:inline-block; width:40px; height:2px; border-top:4px solid ' +
    series[i].color + '"></span></td><td style="background-color:#F8F8F8">'  + series[i].name + '</td><td>' + String(uploads) +
    '</td><td style="background-color:#F8F8F8">' + String(series[i].usage) + ' (' + String(Math.round(100 * series[i].usage / uploads)) +
    '%)</td><td><a href="./WLE:' + series[i].name.replace(/ /g, '_') + '">' + String(series[i].users[0]) + '</a></td><td style="background-color:#F8F8F8">' +
    String(series[i].users[1]) + ' (' + String(Math.round(100 * series[i].users[1] / series[i].users[0])) + '%)</td></tr>';
}

var graph = new Rickshaw.Graph( {
    element: document.getElementById("graph"),
    width: 800,
    height: 500,
    renderer: 'line',
    stroke: true,
    preserve: true,
    series: series
});

graph.render();

var xAxis = new Rickshaw.Graph.Axis.Time({graph: graph});
xAxis.render();

var yAxis = new Rickshaw.Graph.Axis.Y({graph: graph});
yAxis.render();

var hoverDetail = new Rickshaw.Graph.HoverDetail( {
    graph: graph,
    xFormatter: function(x){
        var d = new Date(x * 1000);
        var dia = String(d.getUTCDate());
        return 'day ' + dia;
    },
    yFormatter: function(y){return y}
});

</script>
{%- else %}
<span style="color:red"><b>Erro</b></span>
{%- endif %}
{% endblock %}
'''

pageUsers = u'''
{% extends "Tools.html" %}
{% block head %}
<style>
  table th{border-bottom:2px solid #555; padding:2px 5px 2px 5px}
  table td{padding:5px 2px 5px 2px; border-bottom:1px solid #DDD}
</style>
{% endblock %}
{% block content %}
<p>Uploaders for Wiki Loves Earth campaign in {{ name }}.</p>
{% if query %}
<table style="text-align:center; border-collapse:collapse; min-width:800px; margin-top:8px">
 <tr>
  <th>Uploader</th>
  <th>Images</th>
  <th>Images used<br/>in the wikis</th>
  <th>Registration</th>
{% for user in query %}<tr>
  <td><a href="https://commons.wikimedia.org/wiki/Special:Contributions/{{ user[0]|replace(' ', '_') }}">{{ user[0] }}</a></td>
  <td style="background-color:#F8F8F8">{{ user[1] }}</td>
  <td>{{ user[2] }}</td>
  <td style="background-color:#F8F8F8{% if user[3][-7:] == '05/2014' %}; color:#080{% endif %}">{{ user[3] }}</td>
</tr>{% endfor %}
</table>
{%- else %}
<span style="color:red"><b>Error</b></span>
{%- endif %}
{% endblock %}
'''

def main(name=None):
    c = conn('commonswiki')
    if c and not name:
        c.execute(u'''SELECT
 SUBSTR(cl_to, 38) país,
 UNIX_TIMESTAMP(SUBSTR(img_timestamp, 1, 8)) dia,
 COUNT(*) upload
 FROM categorylinks INNER JOIN page ON cl_from = page_id INNER JOIN image ON page_title = img_name
 WHERE cl_type = 'file' AND cl_to IN (SELECT
   page_title
   FROM page
   WHERE page_namespace = 14 AND page_title LIKE 'Images_from_Wiki_Loves_Earth_2014_in_%' AND page_title NOT LIKE '%\_-\_%')
 GROUP BY país, dia''')
        r = [(i[0].decode('utf-8').replace(u'_', u' '), int(i[1]), int(i[2])) for i in c.fetchall()]
        paises = dict((i[0], 0) for i in r)
        def pSum(p, n):
            paises[p] += n
            return paises[p]
        paises = dict((p, {'data':u', '.join(u'{{x:{},y:{}}}'.format(i[1], pSum(p, i[2])) for i in r if i[0] == p and i[1] >= 1398816000)}) for p in paises)
        c.execute(u'''SELECT
 SUBSTR(cl_to, 38) país,
 SUM(img_name IN (SELECT DISTINCT gil_to FROM globalimagelinks)) use_in_wiki
 FROM categorylinks INNER JOIN page ON cl_from = page_id INNER JOIN image ON page_title = img_name
 WHERE cl_type = 'file' AND cl_to IN (SELECT
   page_title
   FROM page
   WHERE page_namespace = 14 AND page_title LIKE 'Images_from_Wiki_Loves_Earth_2014_in_%' AND page_title NOT LIKE '%\_-\_%')
 GROUP BY país''')
        r = dict((i[0].decode('utf-8').replace(u'_', u' '), int(i[1])) for i in c.fetchall())
        for p in paises:
            paises[p]['usage'] = r[p]
        c.execute(u'''SELECT
 país,
 COUNT(*),
 SUM(user_registration > 20140501000000)
 FROM (SELECT
   DISTINCT SUBSTR(cl_to, 38) país,
   img_user
   FROM categorylinks INNER JOIN page ON cl_from = page_id INNER JOIN image ON page_title = img_name
   WHERE cl_type = 'file' AND cl_to IN (SELECT
     page_title
     FROM page
     WHERE page_namespace = 14 AND page_title LIKE 'Images_from_Wiki_Loves_Earth_2014_in_%' AND page_title NOT LIKE '%\_-\_%')
   ) users
 INNER JOIN user ON img_user = user_id
 GROUP BY país;''')
        r = dict((i[0].decode('utf-8').replace(u'_', u' '), u'[{},{}]'.format(int(i[1]), int(i[2]))) for i in c.fetchall())
        for p in paises:
            paises[p]['users'] = r[p]
        query = u',\n  '.join(u'{{name:"{name}", usage:{usage}, users:{users}, data:[{data}]}}'.format(name=p.replace(u'the ', u''), **paises[p]) for p in paises)
        return render_template_string(page, title=u'Wiki Loves Earth 2014', query=query)
    elif c:
        name = name.replace(u'Netherlands', u'the_Netherlands')
        c.execute(u'''SELECT
 user_name,
 c,
 use_in_wiki,
 user_registration
 FROM (SELECT
   img_user,
   COUNT(*) c,
   SUM(img_name IN (SELECT DISTINCT gil_to FROM globalimagelinks)) use_in_wiki
   FROM categorylinks INNER JOIN page ON cl_from = page_id INNER JOIN image ON page_title = img_name
   WHERE cl_to = ? AND cl_type = 'file'
   GROUP BY img_user
   ORDER BY c DESC
  ) img INNER JOIN user ON img_user = user_id''', ('Images_from_Wiki_Loves_Earth_2014_in_{}'.format(name),))
        r = [(i[0].decode('utf-8').replace(u'_', u' '), int(i[1]), int(i[2]),
             i[3] and u'{}/{}/{}'.format(str(i[3])[6:8], str(i[3])[4:6], str(i[3])[0:4]) or u'?') for i in c.fetchall()]
        name = name.replace(u'_', u' ')
        return render_template_string(pageUsers, title=u'Wiki Loves Earth 2014 in ' + name, query=r, name=name)
    else:
        return render_template_string(page, title=u'Wiki Loves Earth 2014', query={})

