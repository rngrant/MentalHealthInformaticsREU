# Import useful mathematical libraries
import numpy as np
import pandas as pd
import glob, csv

# Import useful Machine learning libraries
import gensim

# Import utility files
from utils import read_df, remove_links, clean_sentence, save_object, load_object

# set the model name
model_name = "example1"

# set the folder for saved objects
import os
directories = ['objects', 'objects/subreddit_post_analysis']
for dirname in directories:
    if not os.path.exists(dirname):
        os.makedirs(dirname)

# Get the data from the csv, indexed by name of the author MAKE SURE author is in column index 2 (position 3)
# This saves each csv month into an individual dataframe, to be referenced later
dirname = 'data'
extension = "/*.csv"
file_count = 0
df = pd.DataFrame()
df_list =[]
fnames = glob.glob(dirname + extension)

# create a variable to hold subreddits and their post counts, and the total number of posts
subreddits = []
subreddit_counts = []
sum_posts = 0
sum_deleted_posts = 0

# iterate through each data frame and update statistics
for fname in fnames:
    df = pd.read_csv(fname, header=0, index_col = 2)
    df = df[df.subreddit.notnull()]
    sum_posts += len(df)
    sum_deleted_posts += len(df.loc[['[deleted]']])
    # iterate through each dataframe to analze the percentages of posts
    for j in range(len(df)):
        if not (df.iloc[j].subreddit in subreddits):
            subreddits.append(df.iloc[j].subreddit)
            subreddit_counts.append(1)
        else:
            subreddit_counts[subreddits.index(df.iloc[j].subreddit)] += 1


# sort the subreddits and counts by highest percentage
subreddit_counts, subreddits = (list(t) for t in zip(*sorted(zip(subreddit_counts, subreddits), reverse=True)))

# save subreddit_counts and subreddits
save_object(subreddit_counts, 'objects/subreddit_post_analysis/', model_name + "-subreddit_counts")
save_object(subreddits, 'objects/subreddit_post_analysis/', model_name + "-subreddits")

# open output file with header
csvfile = open("subreddit_post_analysis.csv", "a")
writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
writer.writerow("Pecentage of Posts in each Subreddit:")

# print the percentages of posts in each subreddit present
for subreddit in subreddits:
    writer.writerow([subreddit, str(subreddit_counts[subreddits.index(subreddit)]*100/sum_posts)])
# print total statistics
writer.writerow(["Total Number of Posts", str(sum_posts)])
writer.writerow(["Total Number of Posts After Deletion", str(sum_posts - sum_deleted_posts)])