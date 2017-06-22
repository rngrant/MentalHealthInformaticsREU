import gensim, logging, os, csv
import csvRead

# Get the data from the csv
sentences = csvRead.read('data',"selftext")

# construct and save a basic model
model = gensim.models.Word2Vec([s.split() for s in sentences])
model.save('models/basicModel')
