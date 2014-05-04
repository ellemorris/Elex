import feedparser
import urllib2
import sqlite3 as lite
import sys

#create table, given category
def APIcall(cat):
	url = 'http://export.arxiv.org/api/query?search_query=cat:'+ cat + '&max_results=100'
	data = urllib2.urlopen(url).read()
	d =  feedparser.parse(data)
	
	#create table
	con=lite.connect('test.db')
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS articles")
	cur.execute("CREATE TABLE articles(id TEXT, category TEXT, title TEXT, summary TEXT, author TEXT)")

	#populate table
	for i in range(len(d['entries'])):
		cur.execute('''INSERT INTO articles(id, category, title, summary, author)\
			VALUES (?,?,?,?,?);''', (d.entries[i].id, cat, d.entries[i].title, d.entries[i].summary, d.entries[i].author))
	con.commit()
	
	#retrieve data from table
	cur.execute('SELECT id, category, title, summary, author FROM articles WHERE category=(?)', (cat,))
	rows = cur.fetchall()
	con.close()
	return rows

#look at table for specific category
def retrieveRows (cat):
	rows = APIcall(cat)
	for row in rows:
		print row

#get column names
def colNames():
	con=lite.connect('test.db')
	cur = con.cursor()
	cur.execute('PRAGMA table_info(articles)')
	cols = cur.fetchall()
	for c in cols:
		print c[0], c[1], c[2]
	con.close()

#retrieveRows('q-fin.ST')
#retrieveRows('cs.MM')

