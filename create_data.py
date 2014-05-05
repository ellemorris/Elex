import sqlite3 as lite
import re
import nnmf
import numpy as np 
import matplotlib.pyplot as plt
import nearestneighbour as nn

def removeNewLines(text):
	return re.sub('\n',' ',text)

def getWords(text):
    words = re.compile('\w+').findall(text)
    return [w.lower() for w in words]

#This function connects to our database, by default test.db
#It then proceeds to create 3 objects
#A list of articles
#A dictionary of words and their frequencies across the entire corpus of abstracts
#A list of dictionaries of word their frequencies in each abstract
def makeFeatures(db='test.db', table="articles"):
	con=lite.connect(db)
	cur = con.cursor()
	cur.execute("SELECT * FROM " + table)
	rows = cur.fetchall()


	word_dictionary = {}
	article_words = []
	paper_titles = []

	counter = 0
	for row in rows:
		abstract_text = removeNewLines(row[3])
		abstract_text = getWords(abstract_text)
		
		paper_titles.append(row[2])
		article_words.append({})

		for word in abstract_text:
			if word in word_dictionary.keys():
				word_dictionary[word] += 1
			else:
				word_dictionary[word] = 1

			if word in article_words[counter].keys():
				article_words[counter][word] += 1
			else:
				article_words[counter][word] = 1
		
		counter += 1
	return word_dictionary, article_words, paper_titles

#This function is based on Segarin's code from his book
#We have a dictionary of all the words (across all abstracts) and their frequencies
#We also have a list of dictionaries for each specific abstract
#We need to create a 'master' matrix that includes all the words possible
#Naturally, if a word didn't appear in an abstract's dictionary, 
#its cell in the master matrix should be equal to zero
def makematrix(allw,articlew):
	 wordvec=[]
	 
	 # Only take words that are common but not too common
	 # We don't want to include things like "the" or "which"
	 for w,c in allw.items( ):
	 	if c>6 and c<len(articlew)*0.6:
	 		wordvec.append(w)
	 # Create the word matrix
	 l1=[[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
	 return l1,wordvec

#This is our main function. It takes an article title, and n
#new articles to recommend...
#It also takes nofeatures - the number of features/topics to create
#As well as max_iter - the number of multiplications to do
def recommend(article, n, nofeatures, max_iter=50):
	#Factorize the matrix, make features
	word_dictionary, article_words, paper_titles = makeFeatures()
	wordmatrix,wordvec = makematrix(word_dictionary, article_words)

	plt.plot(sorted(word_dictionary.values()))
	plt.savefig("WordFrequencies.png")

	w,h = nnmf.factorize(np.matrix(wordmatrix), nofeatures, max_iter)

	print "Recommendations for article: "
	print article
	print "-----------------------------"
	tofind = unicode(paper_titles.index(article))
	nearest = nn.findnearest(w[tofind,:], w, paper_titles, 1, 0)
	nn.printnearest(nearest, 5)


#The method of printing is borrowed from Segarin
#this function is useful for looking under the hood of the factorization
#it displays the top words that make up a feature from the H matrix
#as well as the top abstracts that fit into a feature from the W matrix 
def visualizeFactorization(nofeatures=5, max_iter=10):
	word_dictionary, article_words, paper_titles = makeFeatures()
	wordmatrix,wordvec = makematrix(word_dictionary, article_words)
	w,h = nnmf.factorize(np.matrix(wordmatrix), nofeatures, max_iter)


	toppatterns=[[] for i in range(len(paper_titles))]
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
		
		print "----------------------------------------"
		print "Features/Topic Found"
		print str(i) + str(n)

		print "Top 3 Articles Closest Matching Feature/Topic"
		flist=[]
		for j in range(len(paper_titles)):
			# Add the article with its weight
			flist.append((w[j,i],paper_titles[j]))
			toppatterns[j].append((w[j,i],i,paper_titles[j]))
			# Reverse sort the list
		flist.sort()
		flist.reverse()
		# Show the top 3 art
		for f in flist[0:5]:
			print f



#recommend('The Evolution of Market Efficiency and Its Periodicity: A Non-Bayesian\n  Time-Varying Model Approach', 5)
#visualizeFactorization(5, 50)

recommend('Market panic on different time-scales', 5, 30)

