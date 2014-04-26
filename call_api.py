import feedparser
import urllib

#url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
url = 'http://export.arxiv.org/api/query?search_query=cat:q-fin.ST&max_results=1'
data = urllib.urlopen(url).read()
d =  feedparser.parse(data)

for entry in d.entries:
	print entry.id
	print entry.title
	print entry.summary
	
