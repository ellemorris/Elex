import sqlite3 as lite
import re
import nnmf
import numpy as np 

def removeNewLines(text):
	return re.sub('\n',' ',text)

def getWords(text):
    words = re.compile('\w+').findall(text)
    return [w.lower() for w in words]

con=lite.connect('test.db')
cur = con.cursor()
cur.execute("SELECT * FROM articles")
rows = cur.fetchall()


allwords = {}
summarywords = []
summaries = []

counter = 0
for row in rows:
	if row[2] in summaries: continue #remove duplicates

	summary = removeNewLines(row[3])
	summary = getWords(summary)

	summarywords.append({})

	summaries.append(row[2])

	for word in summary:
		allwords.setdefault(word, 0)
		allwords[word] += 1
		summarywords[counter].setdefault(word, 0)
		summarywords[counter][word] += 1

	counter += 1

print allwords

print summaries

def makematrix(allw,articlew):
	 wordvec=[]
	 # Only take words that are common but not too common
	 for w,c in allw.items( ):
	 	if c>6 and c<len(articlew)*0.6:
	 		wordvec.append(w)
	 # Create the word matrix
	 l1=[[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
	 return l1,wordvec

wordmatrix,wordvec = makematrix(allwords, summarywords)


w,h = nnmf.factorize(np.matrix(wordmatrix), pc=5, iter=30)
toppatterns=[[] for i in range(len(summaries))]
patternnames=[]

pc, wc = np.shape(h)
for i in range(pc):
	slist=[]
	# Create a list of words and their weights
	for j in range(wc):
		slist.append((h[i,j],wordvec[j]))
	# Reverse sort the word list
	slist.sort()
	slist.reverse()
	# Print the first six elements
	n=[s[1] for s in slist[0:10]]
	#print "Features"
	print str(i) + str(n)

	print "Articles"
	flist=[]
	for j in range(len(summaries)):
		# Add the article with its weight
		flist.append((w[j,i],summaries[j]))
		toppatterns[j].append((w[j,i],i,summaries[j]))
		# Reverse sort the list
	flist.sort()
	flist.reverse()
	# Show the top 3 art
	for f in flist[0:5]:
		print f


# import matplotlib.pyplot as plt

# print str(np.shape(w)[0])
# plt.scatter(np.array(w[:,2]),np.array(w[:,3]))
# plt.savefig("testplot.png")

