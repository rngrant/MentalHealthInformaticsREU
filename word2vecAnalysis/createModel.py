import gensim, logging, os, csv
import dataUtils

# Get the data from the csv
sentences = dataUtils.read('data',"selftext")

# construct and save a basic model
model = gensim.models.Word2Vec([dataUtils.cleanSentence(s).split() for s in sentences],min_count =10, sg=1, size =100)
model.save('models/basicModel.model')
