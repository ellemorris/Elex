from create_data import *
from call_api import *

##############################
# This is a sample file that will run our main function
# It will create a database (please make sure our files have permission to write to the directory this is in!)
# It will populate that database with 150 articles from two categories
# It will perform NNMF and print out the generated features and articles that
# fit most into those features
# Finally, it will generate 5 recomemndation for an arbitrary article title
##############################

#Only call these if you haven't already! otherwise your database is getting huge
#and you'll need a lot of computer power :)
APIcall("q-fin.ST", 150)
APIcall("cs.MM", 150)

#Extract 5 features, max 30 iterations - this can take a while on low spec PC...
visualizeFactorization(5, 30)

#Now generate 5 recommendations for following article .
# we want 5 recommendations, n=5
# we'll construct 5 features to get there, nofeatures = 5
# and we'll do 30 iterations - we can get much more accurate with more.. but the computing time grows 
recommend('The near-extreme density of intraday log-returns', n = 5, nofeatures = 5, 30)

