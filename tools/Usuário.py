# -*- coding: utf-8 -*-

from flask import render_template_string
from database import conn
from datetime import date
import re

page = u'''
{% extends "base.html" %}
{% block title %}Edições e grupos de {{user}}{% endblock %}
{% block content %}
<table class="wikitable">
    <tr>
        <td style="border:0; background-color:white"></td>
        <th>
<img src="//upload.wikimedia.org/wikipedia/commons/thumb/6/63/Wikipedia-logo.png/50px-Wikipedia-logo.png"/>
<br/><small><a href="//pt.wikipedia.org/wiki/Página_principal">Wikipédia</a></small>
        </th>
        <th>
<img src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Wikibooks-logo.png/50px-Wikibooks-logo.png"/>
<br/><small><a href="//pt.wikibooks.org/wiki/Página_principal">Wikilivros</a></small>
        </th>
        <th>
<img src="//upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Wiktionary-logo.svg/54px-Wiktionary-logo.svg.png"/>
<br/><small><a href="//pt.wiktionary.org/wiki/Página_principal">Wikicionário</a></small>
        </th>
        <th>
<img style="margin:7px 0 7px" src="//upload.wikimedia.org/wikipedia/commons/thumb/2/24/Wikinews-logo.svg/70px-Wikinews-logo.svg.png"/>
<br/><small><a href="//pt.wikinews.org/wiki/Página_principal">Wikinotícias</a></small>
        </th>
        <th>
<img src="http://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Wikiversity-logo.svg/60px-Wikiversity-logo.svg.png"/>
<br/><small><a href="//pt.wikiversity.org/wiki/Página_principal">Wikiversidade</a></small>
        </th>
        <th>
<img src="//upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Wikiquote-logo.svg/45px-Wikiquote-logo.svg.png"/>
<br/><small><a href="//pt.wikiquote.org/wiki/Página_principal">Wikiquote</a></small>
        </th>
        <th>
<img src="//upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Wikisource-logo.svg/50px-Wikisource-logo.svg.png"/>
<br/><small><a href="//pt.wikisource.org/wiki/Página_principal">Wikisource</a></small>
        </th>
        <th>
<img src="//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Wikivoyage-logo.svg/50px-Wikivoyage-logo.svg.png"/>
<br/><small><a href="//pt.wikivoyage.org/wiki/Página_principal">Wikivoyage</a></small>
        </th>
    </tr>
    <tr>
        <th>Primeira edição</th>
        <td>{{ time_ptwiki |safe }}</td>
        <td>{{ time_ptwikibooks |safe }}</td>
        <td>{{ time_ptwiktionary |safe }}</td>
        <td>{{ time_ptwikinews |safe }}</td>
        <td>{{ time_ptwikiversity |safe }}</td>
        <td>{{ time_ptwikiquote |safe }}</td>
        <td>{{ time_ptwikisource |safe }}</td>
        <td>{{ time_ptwikivoyage |safe }}</td>
    </tr>
    <tr>
        <th>Edições totais</th>
        <td><a href="//pt.wikipedia.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{user|replace(" ", "_")}}">{{ total_ptwiki }}</a></td>
        <td><a href="//pt.wikibooks.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{user|replace(" ", "_")}}">{{ total_ptwikibooks }}</a></td>
        <td><a href="//pt.wiktionary.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{user|replace(" ", "_")}}">{{ total_ptwiktionary }}</a></td>
        <td><a href="//pt.wikinews.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{user|replace(" ", "_")}}">{{ total_ptwikinews }}</a></td>
        <td><a href="//pt.wikiversity.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{user|replace(" ", "_")}}">{{ total_ptwikiversity }}</a></td>
        <td><a href="//pt.wikiquote.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{user|replace(" ", "_")}}">{{ total_ptwikiquote }}</a></td>
        <td><a href="//pt.wikisource.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{user|replace(" ", "_")}}">{{ total_ptwikisource }}</a></td>
        <td><a href="//pt.wikivoyage.org/wiki/Especial:Contribui%C3%A7%C3%B5es/{{user|replace(" ", "_")}}">{{ total_ptwikivoyage }}</a></td>
    </tr>
    <tr>
        <th>Edições no domínio principal</th>
        <td>{{ main_ptwiki }}</td>
        <td>{{ main_ptwikibooks }}</td>
        <td>{{ main_ptwiktionary }}</td>
        <td>{{ main_ptwikinews }}</td>
        <td>{{ main_ptwikiversity }}</td>
        <td>{{ main_ptwikiquote }}</td>
        <td>{{ main_ptwikisource }}</td>
        <td>{{ main_ptwikivoyage }}</td>
    </tr>
    <tr>
        <th>Páginas criadas no domínio principal</th>
        <td>{{ created_ptwiki }}</td>
        <td>{{ created_ptwikibooks }}</td>
        <td>{{ created_ptwiktionary }}</td>
        <td>{{ created_ptwikinews }}</td>
        <td>{{ created_ptwikiversity }}</td>
        <td>{{ created_ptwikiquote }}</td>
        <td>{{ created_ptwikisource }}</td>
        <td>{{ created_ptwikivoyage }}</td>
    </tr>
    <tr>
        <th>Ficheiros carregados<sup><sub>*</sub></sup></th>
        <td>{{ uploads_ptwiki }}</td>
        <td>{{ uploads_ptwikibooks }}</td>
        <td>{{ uploads_ptwiktionary }}</td>
        <td>{{ uploads_ptwikinews }}</td>
        <td>{{ uploads_ptwikiversity }}</td>
        <td>{{ uploads_ptwikiquote }}</td>
        <td>{{ uploads_ptwikisource }}</td>
        <td>{{ uploads_ptwikivoyage }}</td>
    </tr>
    <tr>
        <th>Direito ao voto</th>
        <td>{{ vote_ptwiki |safe }}</td>
        <td>{{ vote_ptwikibooks |safe }}</td>
        <td>{{ vote_ptwiktionary |safe }}</td>
        <td>{{ vote_ptwikinews |safe }}</td>
        <td>{{ vote_ptwikiversity |safe }}</td>
        <td>{{ vote_ptwikiquote |safe }}</td>
        <td>{{ vote_ptwikisource |safe }}</td>
        <td>{{ vote_ptwikivoyage |safe }}</td>
    </tr>
    <tr>
        <th>Administrador</th>
        <td>{{ sysop_ptwiki |safe }}</td>
        <td>{{ sysop_ptwikibooks |safe }}</td>
        <td>{{ sysop_ptwiktionary |safe }}</td>
        <td>{{ sysop_ptwikinews |safe }}</td>
        <td>{{ sysop_ptwikiversity |safe }}</td>
        <td>{{ sysop_ptwikiquote |safe }}</td>
        <td>{{ sysop_ptwikisource |safe }}</td>
        <td>{{ sysop_ptwikivoyage |safe }}</td>
    </tr>
    <tr>
        <th>Outros grupos</th>
        <td>{{ others_ptwiki |safe }}</td>
        <td>{{ others_ptwikibooks |safe }}</td>
        <td>{{ others_ptwiktionary |safe }}</td>
        <td>{{ others_ptwikinews |safe }}</td>
        <td>{{ others_ptwikiversity |safe }}</td>
        <td>{{ others_ptwikiquote |safe }}</td>
        <td>{{ others_ptwikisource |safe }}</td>
        <td>{{ others_ptwikivoyage |safe }}</td>
    </tr>
</table>
<br/>
<h3>Projetos globais</h3>
<table class="wikitable" style="margin-top:0">
    <tr>
        <td style="border:0; background-color:white"></td>
        <th>
<img src="//upload.wikimedia.org/wikipedia/commons/thumb/3/39/Commons-logo.png/50px-Commons-logo.png"/>
<br/><small><a href="//commons.wikimedia.org/wiki/Pagina_principal">Commons</a></small>
        </th>
        <th style="padding-left:1px; padding-right:1px">
<img style="margin:10px 0 10px" src="//upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Wikidata-logo.svg/80px-Wikidata-logo.svg.png"/>
<br/><small><a href="//www.wikidata.org/wiki/Wikidata:Página_principal">Wikidata</a></small>
        </th>
        <th>
<img src="http://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Wikispecies-logo.png/50px-Wikispecies-logo.png"/>
<br/><small><a href="//species.wikimedia.org/wiki/Página_principal">Wikispecies</a></small>
        </th>
    </tr>
    <tr>
        <th>Primeira edição</th>
        <td>{{ time_commonswiki |safe }}</td>
        <td>{{ time_wikidatawiki |safe }}</td>
        <td>{{ time_specieswiki |safe }}</td>
    </tr>
    <tr>
        <th>Edições totais</th>
        <td><a href="//commons.wikimedia.org/wiki/Special:Contributions/{{user|replace(" ", "_")}}">{{ total_commonswiki }}</a></td>
        <td><a href="//www.wikidata.org/wiki/Special:Contributions/{{user|replace(" ", "_")}}">{{ total_wikidatawiki }}</a></td>
        <td><a href="//species.wikimedia.org/wiki/Special:Contributions/{{user|replace(" ", "_")}}">{{ total_specieswiki }}</a></td>
    </tr>
    <tr>
        <th>Edições no domínio principal</th>
        <td>{{ main_commonswiki }}</td>
        <td>{{ main_wikidatawiki }}</td>
        <td>{{ main_specieswiki }}</td>
    </tr>
    <tr>
        <th>Páginas criadas no domínio principal</th>
        <td>{{ created_commonswiki }}</td>
        <td>{{ created_wikidatawiki }}</td>
        <td>{{ created_specieswiki }}</td>
    </tr>
    <tr>
        <th>Ficheiros carregados<sup><sub>*</sub></sup></th>
	<td><a href="//commons.wikimedia.org/w/index.php?title=Special:ListFiles/{{user|replace(" ", "_")}}&ilshowall=1">{{ uploads_commonswiki }}</a></td>
        <td>{{ uploads_wikidatawiki }}</td>
        <td>{{ uploads_specieswiki }}</td>
</table>
<p style="font-size:80%">* Por motivos técnicos, só são contados os carregamentos que são a versão atual do ficheiro.</p>
<br/>
<table style="margin: 4em auto 15em auto;">
  <tr>
    <td>Usuário:</td>
    <td><input id="user" type="text" onkeypress="return enter(event, this, 'Usuário:')"/></td>
  </tr>
</table>
{{ error |safe }}{% endblock %}
'''

def main(user=None):
    # 'nome da wiki no banco de dados': (tempo-voto, edições-voto, tempo-administrador, edições-administrador, outro-nome, outro-tempo, outro-edições)
    ptwikis = {'ptwiki': (90, 300, 182, 2000, 'eliminador', 182, 1000),
               'ptwikibooks': (30, 50),
               'ptwikiversity': (45, 0),
               'ptwiktionary': (30, 200, 30, 100),
               'ptwikinews': (30, 50),
               'ptwikiquote': (30, 100),
               'ptwikisource': (45, 100),
               'ptwikivoyage': None,
               'commonswiki': None,
               'wikidatawiki': None,
               'specieswiki': None}
    groups = {'autoreviewer': 'autorrevisor', 'rollbacker': 'reversor', 'bureaucrat': 'burocrata', 'checkuser': 'verificador' ,'oversight': 'supervisor',
              'reviewer': 'revisor', 'import': 'importador'}
    uploads = {'ptwiki': 0, 'commonswiki': 0}
    response = {}
    user = user.replace(u'_', u' ')
    for wiki in ptwikis:
        c = conn(wiki)
        if not c:
            response[wiki] = {'time': u'Erro', 'total': u'?', 'main': u'?', 'created': u'?', 'vote': u'', 'sysop': u'', 'others': u''}
            continue
        #Consulta edições totais, páginas criadas e primeira edição, separando em domínio principal (main) e outros domínios (others)
        c.execute('''SELECT
 (CASE page_namespace WHEN 0 THEN "main" ELSE "others" END) AS namespace,
 COUNT(*),
 SUM(CASE WHEN rev_parent_id = 0 AND page_is_redirect = 0 THEN 1 ELSE 0 END),
 MIN(rev_timestamp)
 FROM revision_userindex
 FULL JOIN page
 ON page_id = rev_page
 WHERE rev_user != 0 AND rev_user_text = ?
 GROUP BY namespace''', (user,))
        r = c.fetchall()
        if not r:
            response[wiki] = {'time': u'Nunca editou', 'total': u'0', 'main': u'0', 'created': u'0', 'vote': u'—', 'sysop': u'—', 'others': u'—', 'uploads': u'0'}
            continue
        c.execute('SELECT ug_group FROM user LEFT JOIN user_groups ON user_id = ug_user WHERE user_name = ?', (user,))
        g = c.fetchall()
        u = None
        if wiki in uploads:
            c.execute('SELECT COUNT(*) FROM image WHERE img_user_text = ?', (user,))
            u = c.fetchall()

        g = g and [i in groups and groups[i] or i for i in map(lambda i:i[0], g) if i] or []
        u = u and int(u[0][0]) or u'0'
        # Tempo desde a primeira edição
        t = len(r) == 2 and min(r[0][3], r[1][3]) or r[0][3]
        days = (date.today() - date(int(t[0:4]), int(t[4:6]), int(t[6:8]))).days
        wikitime = u'{}/{}/{}<br />{}'.format(t[6:8], t[4:6], t[0:4], days >= 365 and (days/365 > 1 and str(days/365) + ' anos' or '1 ano')  or
                   days == 1 and '1 dia' or str(days) + ' dias')
        # Edições totais
        total = len(r) == 2 and r[0][1] + r[1][1] or r[0][1]
        # Edições e páginas criadas no domínio principal
        main, created = r[0][0] == u'main' and r[0][1:3] or len(r) == 2 and r[1][1:3] or [0,0]
        # Direito ao voto
        vote = ptwikis[wiki] and (days >= ptwikis[wiki][0] and (main >= ptwikis[wiki][1] and u'<span style="color:#080"><b>Sim</b></span>' or
               u'<span style="color:#800">Não</span><br/><small>menos de {} edições</small>'.format(ptwikis[wiki][1])) or
               u'<span style="color:#800">Não</span><br/><small>menos de {} dias{}</small>'.format(ptwikis[wiki][0],
               main < ptwikis[wiki][1] and u' e de {} edições'.format(ptwikis[wiki][1]) or u'')) or u'—'
        # Administrador
        sysop = 'sysop' in g and u'<span style="color:#080"><b>É administrador</b></span>' or ptwikis[wiki] and len(ptwikis[wiki]) > 2 and (
                days >= ptwikis[wiki][2] and (main >= ptwikis[wiki][3] and u'Pode candidatar-se' or
                u'<span style="color:#800">Não pode</span><br/><small>menos de {} edições</small>'.format(ptwikis[wiki][3])) or
                u'<span style="color:#800">Não pode</span><br/><small>menos de {} dias{}</small>'.format(ptwikis[wiki][2],
                main < ptwikis[wiki][1] and u' e de {} edições'.format(ptwikis[wiki][1]))) or u'—'
        # Outros direitos
        others = ptwikis[wiki] and len(ptwikis[wiki]) == 7 and 'sysop' not in g and ptwikis[wiki][4] not in g and (days >= ptwikis[wiki][5] and
                (main >= ptwikis[wiki][6] and u'Pode candidatar-se a {}'.format(ptwikis[wiki][4]) or
                u'<span style="color:#800">Não pode candidatar-se a {}</span><br/><small>menos de {} edições</small>'.format(ptwikis[wiki][4], ptwikis[wiki][6])) or
                u'<span style="color:#800">Não pode candidatar-se a {}</span><br/><small>menos de {} dias{}</small>'.format(ptwikis[wiki][4], ptwikis[wiki][5],
                total < ptwikis[wiki][1] and u' e de {} edições'.format(ptwikis[wiki][6]))) or None
        others = g and u'<br />'.join((others and [others] or []) + [u'<span style="color:#080"><b>{}</b></span>'.format(i) for i in g if i != 'sysop']) or others or u'—'
        response[wiki] = {'time': wikitime, 'total': str(total), 'main': str(main), 'created': str(created), 'vote': vote, 'sysop': sysop, 'others': others, 'uploads': u}
    variables = dict([('{}_{}'.format(item, wiki), response[wiki][item])for wiki in response for item in response[wiki]])
    variables['user'] = user
    return render_template_string(page, title=u'Edições e grupos de ' + user, **variables)
