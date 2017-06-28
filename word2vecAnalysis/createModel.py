import gensim, logging, os, csv
import dataUtils

# Get the data from the csv
sentenceStream =dataUtils.read('data',["title","selftext"])
sentences = [dataUtils.cleanSentence(s).split() for s in sentenceStream]

# construct and save a basic model
# model = gensim.models.Word2Vec(sentences,min_count =10,
#                                sg=1, size =300,window=5,hs=1)
# model.save('models/basicModel.model')

#construct and save usage model
# bigram_transformer = gensim.models.Phrases(sentences)
# Using phrase transformation
# model = gensim.models.Word2Vec(bigram_transformer[sentences],min_count =10,
#                               sg=1, size =300,window=5,hs=1)
model = gensim.models.Word2Vec(sentences,min_count =10,
                               sg=1, size =300,window=5,hs=1)
model.save('models/model1.model')
