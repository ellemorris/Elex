import feedparser
import urllib2
import sqlite3 as lite
import sys

url = 'http://export.arxiv.org/api/query?search_query=cat:q-fin.ST&max_results=5'
data = urllib2.urlopen(url).read()

d =  feedparser.parse(data)

# for entry in d.entries:
# 	print entry.id
# 	print entry.title
# 	print entry.summary
# 	print entry.author

#create table
con=lite.connect('test.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS qfin")
cur.execute("CREATE TABLE qfin(id TEXT, title TEXT, summary TEXT, author TEXT)")

#populate table
for i in range(len(d['entries'])):
	cur.execute('''INSERT INTO qfin(id, title, summary, author)\
		VALUES (?,?,?,?);''', (d.entries[i].id, d.entries[i].title, d.entries[i].summary, d.entries[i].author))
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
con.close()