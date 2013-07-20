# -*- coding: utf-8  -*-
"""
Script para consultas ao banco de dados
"""
import os, oursql
from datetime import date

def template(page, args=[]):
    functions = {u'Usuário': 'EditsAndRights(*args)',
                 u'Patrulhamento_de_IPs': 'ippatrol()',
                 u'Filtros': u'filterActions()'}
    if page in functions:
        return eval(functions[page])
    else:
        return {}

def conn(wiki):
    try:
        connection = oursql.connect(db=wiki + '_p', host=wiki + '.labsdb', read_default_file=os.path.expanduser('~/replica.my.cnf'))
        return connection.cursor()
    except:
        return False

def EditsAndRights(user):
    """
    Consulta as edições de usuários em todas os projetos lusófonos
    """
    # 'nome da wiki no banco de dados': (tempo-voto, edições-voto, tempo-administrador, edições-administrador, outro-nome, outro-tempo, outro-edições)
    ptwikis = {'ptwiki': (90, 300, 182, 2000, 'eliminador', 182, 1000),
               'ptwikibooks': (30, 50),
               'ptwikiversity': (45, 0),
               'ptwiktionary': (30, 200, 30, 100),
               'ptwikinews': (30, 50),
               'ptwikiquote': (30, 100),
               'ptwikisource': (45, 100),
               'ptwikivoyage': None}
    groups = {'autoreviewer': 'autorrevisor', 'rollbacker': 'reversor', 'bureaucrat': 'burocrata', 'checkuser': 'verificador' ,'oversight': 'supervisor',
              'reviewer': 'revisor', 'import': 'importador'}
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
 SUM(page_is_new),
 MIN(rev_timestamp)
 FROM revision_userindex
 FULL JOIN page
 ON page_id = rev_page
 WHERE rev_user_text = ?
 GROUP BY namespace''', (user,))
        r = c.fetchall()
        if not r:
            response[wiki] = {'time': u'Nunca editou', 'total': u'0', 'main': u'0', 'created': u'0', 'vote': u'—', 'sysop': u'—', 'others': u'—'}
            continue
        c.execute('SELECT ug_group FROM user LEFT JOIN user_groups ON user_id = ug_user WHERE user_name = ?', (user,))
        g = c.fetchall()
        g = g and [i in groups and groups[i] or i for i in map(lambda i:i[0], g) if i] or []
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
               main < ptwikis[wiki][1] and u' e de {} edições'.format(ptwikis[wiki][1]))) or u'—'
        # Administrador
        sysop = 'sysop' in g and u'<span style="color:#080"><b>É administrador</b></span>' or ptwikis[wiki] and len(ptwikis[wiki]) > 2 and (
                days >= ptwikis[wiki][2] and (main >= ptwikis[wiki][3] and u'Pode candidatar-se' or
                u'<span style="color:#800">Não pode</span><br/><small>menos de {} edições</small>'.format(ptwikis[wiki][3])) or
                u'<span style="color:#800">Não pode</span><br/><small>menos de {} dias{}</small>'.format(ptwikis[wiki][2],
                main < ptwikis[wiki][1] and u' e de {} edições'.format(ptwikis[wiki][1]))) or u'—'
        # Outros direitos
        others = ptwikis[wiki] and len(ptwikis[wiki]) == 7 and 'sysop' not in g and ptwikis[wiki][4] not in g and (days >= ptwikis[wiki][2] and
                (main >= ptwikis[wiki][3] and u'Pode candidatar-se a {}'.format(ptwikis[wiki][4]) or
                u'<span style="color:#800">Não pode candidatar-se a {}</span><br/><small>menos de {} edições</small>'.format(ptwikis[wiki][4], ptwikis[wiki][6])) or
                u'<span style="color:#800">Não pode candidatar-se a {}</span><br/><small>menos de {} dias{}</small>'.format(ptwikis[wiki][4], ptwikis[wiki][5],
                total < ptwikis[wiki][1] and u' e de {} edições'.format(ptwikis[wiki][6]))) or None
        others = g and u'<br />'.join((others and [others] or []) + [u'<span style="color:#080"><b>É {}</b></span>'.format(i) for i in g if i != 'sysop']) or others or u'—'
        response[wiki] = {'time': wikitime, 'total': str(total), 'main': str(main), 'created': str(created), 'vote': vote, 'sysop': sysop, 'others': others}
    variables = dict([('{}_{}'.format(item, wiki), response[wiki][item])for wiki in response for item in response[wiki]])
    variables['user'] = user
    return variables

def ippatrol():
    c = conn('ptwiki')
    if c:
        c.execute('''SELECT
 SUBSTR(rc_timestamp, 1, 10) AS HORA,
 COUNT(*),
 SUM(rc_patrolled)
 FROM recentchanges
 WHERE rc_namespace = 0 AND rc_user = 0 AND rc_type != 5
 GROUP BY HORA
 ORDER BY rc_id DESC
 LIMIT 168''')
        r = c.fetchall()
        r = {'iphquery': ','.join([(x in r[6::6] and '\n[{},{},{}]' or '[{},{},{}]').format(*x) for x in r])}
    else:
        r = {}
    return r

def filterActions():
    c = conn('ptwiki')
    if c:
        c.execute('''SELECT
 afl_filter,
 SUM(CASE WHEN afl_actions = '' THEN 1 ELSE 0 END),
 SUM(CASE WHEN afl_actions = 'warn' THEN 1 ELSE 0 END),
 SUM(CASE WHEN afl_actions = 'tag' THEN 1 ELSE 0 END),
 SUM(CASE WHEN afl_actions = 'disallow' THEN 1 ELSE 0 END)
 FROM abuse_filter_log
 WHERE afl_timestamp > DATE_FORMAT(SUBDATE(NOW(), INTERVAL 30 DAY), '%Y%m%d%H%i%s')
 GROUP BY afl_filter
 ORDER BY CAST(afl_filter AS INT)''')
        r = c.fetchall()
        r = [map(int, f) for f in r]
        r = {'filters': r, 'max': max(map(max, r))}
    else:
        r = {}
    return r
