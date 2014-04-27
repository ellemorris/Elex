import feedparser
import urllib2
import sqlite3 as lite
import sys

url = 'http://export.arxiv.org/api/query?search_query=cat:q-fin.ST&max_results=100'
data = urllib2.urlopen(url).read()
d =  feedparser.parse(data)

url2 = 'http://export.arxiv.org/api/query?search_query=cat:cs.MM&max_results=100'
data2 = urllib2.urlopen(url2).read()
d2 =  feedparser.parse(data2)

#create table
con=lite.connect('test.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS qfin")
cur.execute("CREATE TABLE qfin(id TEXT, title TEXT, summary TEXT, author TEXT)")

#create table
con=lite.connect('test.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS mm")
cur.execute("CREATE TABLE mm(id TEXT, title TEXT, summary TEXT, author TEXT)")

#populate table
for i in range(len(d['entries'])):
	cur.execute('''INSERT INTO qfin(id, title, summary, author)\
		VALUES (?,?,?,?);''', (d.entries[i].id, d.entries[i].title, d.entries[i].summary, d.entries[i].author))
con.commit()

#populate table
for i in range(len(d2['entries'])):
	cur.execute('''INSERT INTO mm(id, title, summary, author)\
		VALUES (?,?,?,?);''', (d2.entries[i].id, d2.entries[i].title, d2.entries[i].summary, d2.entries[i].author))
con.commit()

#get column names
cur.execute('PRAGMA table_info(qfin)')
cols = cur.fetchall()
for c in cols:
	print c[0], c[1], c[2]

#retrieve data from table
cur.execute("SELECT * FROM qfin")
rows = cur.fetchall()
for row in rows:
	print row

#retrieve data from table
cur.execute("SELECT * FROM mm")
rows2 = cur.fetchall()
for row in rows2:
	print row
con.close()