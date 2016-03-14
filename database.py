#! /usr/bin/python
# -*- coding: utf-8  -*-
"""
Script para consultas ao banco de dados
"""
import os
import oursql
from datetime import date

ns = {1: u'Discussão:',
      3: u'Usuário(a) Discussão:',
      2: u'Usuário(a):',
      5: u'Wikipédia Discussão:',
      4: u'Wikipédia:',
      7: u'Ficheiro Discussão:',
      6: u'Ficheiro:',
      9: u'MediaWiki Discussão:',
      8: u'MediaWiki:',
      447: u'Ensino Discussão:',
      446: u'Ensino:',
      711: u'TimedText talk:',
      710: u'TimedText:',
      102: u'Anexo:',
      103: u'Anexo Discussão:',
      100: u'Portal:',
      101: u'Portal Discussão:',
      104: u'Livro:',
      105: u'Livro Discussão:',
      11: u'Predefinição Discussão:',
      10: u'Predefinição:',
      13: u'Ajuda Discussão:',
      12: u'Ajuda:',
      15: u'Categoria Discussão:',
      14: u'Categoria:',
      829: u'Módulo Discussão:',
      828: u'Módulo:'}

def template(page, arg):
    functions = {u'Editor_Visual': visualeditor,
		 u'Interface_Movel': interfacemovel}
    if page in functions:
        return functions[page](arg)
    else:
        return {}

def conn(db, host=None):
    if not os.uname()[1].startswith('tools-webgrid'):
        # Não tentar acessar o bd fora do Labs
        return False
    wikis = {u'Wikipédia': 'ptwiki', u'Wikilivros': 'ptwikibooks', u'Wikiversidade': 'ptwikiversity', u'Wikcionário': 'ptwiktionary', u'Wikinotícias': 'ptwikinews',
             u'Wikiquote': 'ptwikiquote', u'Wikisource': 'ptwikisource', u'Wikivoyage': 'ptwikivoyage'}
    try:
	if host:
	    connection = oursql.connect(db=db, host=host, read_default_file=os.path.expanduser('~/replica.my.cnf'))
        else:
	    db = db in wikis and wikis[db] or db
            connection = oursql.connect(db=db + '_p', host=db + '.labsdb', read_default_file=os.path.expanduser('~/replica.my.cnf'))
        return connection.cursor()
    except:
        return False

def query(query, db='ptwiki', host=None, limit=200):
    corr = lambda i: type(i) == str and i.decode('utf-8') or type(i) == long and int(i) or i
    c = conn(db, host)
    if not c:
        print u'# Não foi possível conectar ao BD ' + db
        return False
    c.execute(query)
    r = c.fetchmany(limit)
    r = [tuple(corr(item) for item in linha) for linha in r]
    if len(r[0]) == 1:
        r = [l[0] for l in r]
    return r

def link(wiki):
    wikis = {u'Wikipédia': 'pt.wikipedia', u'Wikilivros': 'pt.wikibooks', u'Wikiversidade': 'pt.wikiversity', u'Wikcionário': 'pt.wiktionary', u'Wikinotícias': 'pt.wikinews',
	    u'Wikiquote': 'pt.wikiquote', u'Wikisource': 'pt.wikisource', u'Wikivoyage': 'pt.wikivoyage', u'metawiki': 'meta.wikimedia', u'commonswiki': 'commons.wikimedia'}
    link = wiki in wikis and wikis[wiki] or wiki[0:2] +u'.' + (wiki[2:] == u'wiki' and u'wikipedia' or wiki[2:])
    return link

def visualeditor(wiki=None):
    if not wiki:
        wiki = u'Wikipédia'
    c = conn(wiki)
    if c:
        c.execute('''SELECT
 SUBSTR(rc_timestamp, 1, 8) AS DIA,
 COUNT(*),
 SUM(CASE WHEN rc_user = 0 THEN 1 ELSE 0 END)
 FROM recentchanges
 INNER JOIN tag_summary
 ON rc_id = ts_rc_id
 WHERE ts_tags LIKE '%visualeditor%'
 GROUP BY DIA
 ORDER BY rc_id DESC''')
        r = c.fetchall()
        r = {'wiki': wiki, 'link': link(wiki), 'VEquery': [map(int, l) for l in r]}
    else:
        r = {}
    return r

def interfacemovel(wiki=None):
    if not wiki:
        wiki = u'Wikipédia'
    c = conn(wiki)
    if c:
        c.execute('''SELECT
 SUBSTR(rc_timestamp, 1, 8) AS DIA,
 COUNT(*),
 SUM(CASE WHEN rc_user = 0 THEN 1 ELSE 0 END)
 FROM recentchanges
 INNER JOIN tag_summary
 ON rc_id = ts_rc_id
 WHERE ts_tags LIKE '%mobile edit%'
 GROUP BY DIA
 ORDER BY rc_id DESC''')
        r = c.fetchall()
        r = {'wiki': wiki, 'link': link(wiki), 'IMquery': [map(int, l) for l in r]}
    else:
        r = {}
    return r
