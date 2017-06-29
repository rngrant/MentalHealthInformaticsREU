import gensim
import dataUtils
import numpy as np
from scipy.sparse import dok_matrix

# Get post's text
sentenceStream = dataUtils.read('data',["title","selftext"])
posts = [dataUtils.cleanSentence(s).split() for s in sentenceStream]

# Load model
model = gensim.models.Word2Vec.load('models/model1.model')

# Create vocab list
vocab_list = list(model.wv.vocab)

cut_words =[]

# Create sparse matrix
num_posts = len(posts)
num_words = len(vocab_list)
postByWordMat = dok_matrix((len(posts),len(vocab_list)))

for i in range(len(posts)):
    print(i)
    for word in posts[i]:
        try:
            postByWordMat[i,vocab_list.index(word)]+=1
        except:
            cut_words.append(word)
dataUtils.save_object(postByWordMat,'matrix/','matrix')
dataUtils.save_object(cut_words,'words/','words')

