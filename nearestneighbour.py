import numpy as np 

def findnearest(feature_set, feature_loadings, article_names, n=1, use_log=1):
	distances = []
	counter = 0
	for i in feature_loadings:
		if use_log == 1:
			delta = (np.log(np.asarray(i)) - np.log(np.asarray(feature_set)))**2
		else:
			delta = ((np.asarray(i)) - (np.asarray(feature_set)))**2
		dist = delta.sum(axis=-1)
		distances.append((dist.tolist()[0], article_names[counter]))
		counter += 1
	distances.sort()

	return distances

def printnearest(nearest, n=5):
	counter = 1 
	for s in nearest[1:(n+1)]:
		print counter, s[1]
		counter += 1