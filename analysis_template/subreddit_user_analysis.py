# Import useful mathematical libraries
import numpy as np
import pandas as pd
import glob, csv

# Import useful Machine learning libraries
import gensim

# Import utility files
from utils import read_df, remove_links, clean_sentence, save_object, load_object

model_name = "example1"

import os
directories = ['objects', 'objects/subreddit_user_analysis']
for dirname in directories:
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
# Get the data from the csv, indexed by name of the author MAKE SURE author is in column
# index 2 (position 3), which is standard in BigQuery data
# This skips over deleted authors to save time and because those authors aren't valid for
# analysis, as their posts cannot be differentiated

dirname = 'data'
extension = "/*.csv"

df = pd.DataFrame()
df_list =[]
fnames = glob.glob(dirname + extension)
for fname in fnames:
    df_chunks = pd.read_csv(fname, header = 0, index_col = 2, iterator = True, chunksize=1000000)
    df = pd.concat([chunk[chunk.index != '[deleted]'] for chunk in df_chunks])
    df = df[df.subreddit.notnull()]
    df_list.append(df)
df = pd.concat(df_list)

# save the data frame of posts
save_object(df, 'objects/subreddit_user_analysis/', model_name + "-posts_dataframe")

# create a list of all authors
authors = []
author_frequency = []
for author in df.index:
    if not (author in authors):
        authors.append(author)
        author_frequency.append(1)
    else:
        author_frequency[authors.index(author)] += 1

# create a list of author subreddit counts
author_subreddit_counts = []
total_subreddit_count = []
# iterate through the authors
for author in authors:
    subreddits = []
    subreddit_count = []
    sub = []
    # find posts from that author in dataframe
    for i in range(len(df.loc[[author]])):
        # if this is the author's first post in the subreddit, add the subreddit name to subreddits list, and add one to the occcurces
        if not (df.loc[[author]].iloc[[i][0]].subreddit in subreddits):
            subreddits.append(df.loc[[author]].iloc[[i][0]].subreddit)
            subreddit_count.append(1)
        # else, add one to the subreddit's occurences at the subreddits index within subreddit count
        else:
            subreddit_count[subreddits.index(df.loc[[author]].iloc[[i][0]].subreddit)] += 1
    # after going through all the data, create a list of lists, which contain a subreddit and its occurence
    for i in range(len(subreddits)):
        sub.append([subreddits[i],subreddit_count[i]])
    # append this list to the author_subreddits list
    author_subreddit_counts.append(sub)
    
# save array of author counts
save_object(author_subreddit_counts, 'objects/subreddit_user_analysis/', model_name + "-author_subreddit_counts")

# create lists for subreddits, subreddit totals
subreddits = []
subreddit_post_totals = []
# iterate through the list of lists of lists to find all the occurences of a subreddit
for i in range(len(author_subreddit_counts)):
    # if a new subreddit is found, append it to all_subreddits, and add its occurences to the correct position in total_posts
    # if it has already been found, add its occurences from that user tothe correct position in total_posts
    for j in range(len(author_subreddit_counts[i])):
        if not(author_subreddit_counts[i][j][0] in subreddits):
            subreddits.append(author_subreddit_counts[i][j][0])
            subreddit_post_totals.append(author_subreddit_counts[i][j][1])
        else:
            subreddit_post_totals[subreddits.index(author_subreddit_counts[i][j][0])] += author_subreddit_counts[i][j][1]

# sort the subreddits and their post totals
subreddit_post_totals, subreddits  = (list(t) for t in zip(*sorted(zip(subreddit_post_totals, subreddits), reverse = True))) 

# find percentage of authors who post in each subreddit
# create list that holds the number of authors that post in each subreddit, ordered by subreddit
num_authors_in_subreddits = []
for i in range(len(subreddits)):
    num_authors_in_subreddits.append(0)
# update the list with occurences
for i in range(len(author_subreddit_counts)):
    for j in range(len(author_subreddit_counts[i])):
        num_authors_in_subreddits[subreddits.index(author_subreddit_counts[i][j][0])] += 1

# open output file with header
csvfile = open("subreddit_user_analysis.csv", "a")
writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
writer.writerow("Pecentage of Users posting in each Subreddit:")

# print percentages of users in each subreddit present
for subreddit in subreddits:
    writer.writerow([subreddit,str(num_authors_in_subreddits[subreddits.index(subreddit)]/len(authors))])