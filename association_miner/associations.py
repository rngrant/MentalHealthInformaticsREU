# Import useful mathematical libraries
import numpy as np
import pandas as pd
import sys

# Import useful Machine learning libraries
import gensim
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer

# Import utility files
from utils import save_object, load_object, make_post_clusters, make_clustering_objects
from orangecontrib.associate.fpgrowth import *

import os

def mine_associations(model_name,num_word_clusters,itemset_support,assoc_confidence):
    
    df = load_object('objects/', model_name + '-df')

    # Load Our Saved matricies
    PostsByWords = load_object('matricies/', model_name + "-PostsByWords")
    WordsByFeatures = load_object('matricies/', model_name + "-WordsByFeatures")

    # Generate the posts by Features matrix through matrix multiplication
    PostsByFeatures = PostsByWords.dot(WordsByFeatures)
    PostsByFeatures = np.matrix(PostsByFeatures)
    
    model = gensim.models.Word2Vec.load('models/' + model_name + '.model')

    vocab_list = sorted(list(model.wv.vocab))
    
    # Initialize a word clustering to use
    kmeans =  load_object('clusters/', model_name + '-words-cluster_model-' + str(num_word_clusters))
    
    clusters = make_clustering_objects(model, kmeans, vocab_list, WordsByFeatures)
    
    clusterWords = list(map(lambda x: list(map(lambda y: y[0] , x["word_list"])), clusters))
    
    countvec = CountVectorizer(vocabulary = vocab_list,
                               analyzer = (lambda lst:
                                           list(map((lambda s: s), lst))),
                               min_df = 0)

    # Make Clusters By Words Matrix
    ClustersByWords = countvec.fit_transform(clusterWords)
    
    # take the transpose of Clusters
    WordsByCluster = ClustersByWords.transpose()
    
    # Multiply Posts by Words by Words By cluster to get Posts By cluster
    PostsByClusters = PostsByWords.dot(WordsByCluster)

    print("finished setup")

    sorted_clusters = sorted(list(zip(clusters,range(len(clusters)))),key = (lambda x : x[0]['total_freq'])
)

    large_indicies = list(map(lambda x: x[1],sorted_clusters[-20:]))

    sorted_large_indicies = sorted(large_indicies, reverse =True)

    X = np.array(PostsByClusters.todense())

    for index in sorted_large_indicies:
        X = np.delete(X,index,1)

    print("finished filtering")
    sys.stdout.flush()
    itemset_path = model_name+'-itemset-'+str(itemset_support)+ '-'+str(num_word_clusters)

    if (os.path.isfile('itemsets/'+itemset_path)):
        itemsets = load_object('itemsets/',itemset_path)
    else:
        itemsets = dict(frequent_itemsets(X > 0, itemset_support/
100))
        save_object(itemsets,'itemsets/',itemset_path)
    print("loaded itemsets")
    sys.stdout.flush()

    assoc_rules = association_rules(itemsets, assoc_confidence/100)
    print("starting parsing rules")
    rules = [(P, Q, supp, conf, conf/(itemsets[P]/X.shape[0]))
             for P, Q, supp, conf in assoc_rules
             if len(Q) == 1 and len(P)==1]
    print("parsed rules")
    print("saving rules")
    sys.stdout.flush()
    save_object(rules,'association_rules/',model_name+'-assoc_rules-'+
                str(itemset_support)+'-' +
                str(assoc_confidence)+'-'+str(num_word_clusters))
    print("saved rules")
    sys.stdout.flush()

