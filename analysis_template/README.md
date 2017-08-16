# Analysis Template

This directory contains iPython jupyter notebooks which offer an interactive experience to analyze the subreddit data.
To run these, first install jupyter onto the machine with which you will be analyzing the data.
You can install Python 3.6 and jupyter notebooks easily by using anaconda. A download can be found here: https://www.continuum.io/downloads/

## Running the Code

To begin analyzing the data, open a terminal, then navigate to the directory containing these files which can be obtained via github at https://github.com/pages0/MentalHealthInformaticsREU.git
Once at the directory, run the following line of code:

`jupyter notebook`

This should open a window in your browser with a file system.

We are now ready to process the collected data.

### Initialize_models.ipynb

This notebook creates the Word2Vec language model from the posts concentrated in the 'data' directory. To run it, simply change the model_name to an appropriate name.
Then, click on the first cell in the notebook, where all the import statements are listed, then clikc the 'Run' arrow in the toolbar or press 'Shift' + 'Enter' to execute a cell.
Continue this process until the last cell has been queued to run. This creates and saves a Word2Vec model along with doing some basic tests. It also creates matricies of Posts and Words,
and creates clusters of words.

### word2vec_analysis.ipynb

To run this notebook, follow the same process as the last one, and be sure to change the model_name to the same one as you chose in Initialize_models.py.
This notebook looks at the quality of the words by finding nearest words and performing analogical reasoning and vector algebra to evaluate the quality of the model.

### text_analysis.ipynb
Again, follow the same general procedure. From this notebook forward, it will be assumed that you change model_name to the appropriate model name.
This notebook calculates statistics on the number of users, posts, and words in the data set.

### Cluster_analysis.ipynb
This notebook attempts to help visualize the clusters created by using Multi-Dimensional Scaling (MDS) to reduce the 300 dimensions into 2, visual dimensions.

### Post_cluster_analysis.ipynb
This creates clusters of posts to find similar sets of posts based on both the features (words) and clusters they contained.

### Association_analysis.ipynb
This creates association rules between the clusters.

### Subreddit_user_analysis.ipynb
This notebook filters out '[deleted]' users and calculates percentages of users posting within each subreddit present in the dataset.

### Subreddit_post_analysis.ipynb
This notebook does not filter out '[deleted]' users, and instead calculates the percentages of posts in each subreddit present in the dataset.

Script options of the subreddit user/post analysis are available if you wish to run the code on a server, as the datasets can be quite large and these calculations may take a qhile to complete.
