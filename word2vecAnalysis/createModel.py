import gensim, logging, os, csv
import dataUtils

# Get the data from the csv
sentences = dataUtils.read('data',"selftext")

# construct and save a basic model
model = gensim.models.Word2Vec([dataUtils.cleanSentence(s).split() for s in sentences])
model.save('models/basicModel.model')
