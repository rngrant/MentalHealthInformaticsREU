import gensim, logging, os, csv, glob
import re
import pandas as pd
import pickle
"""
Helper function for reading from a directory of CSVs
dirname: the name of the directory of CSVs
key: The name of the variable to extract from the CSV
returns a generator that returns the next string in the file
"""
def read(dirname,keys):
        for fname in os.listdir(dirname):
            first = True
            locs =[]
            with open(dirname+ "/"+fname,'r') as csvfile:                
                reader = csv.reader(csvfile,dialect='excel',delimiter=',',quotechar='\"')
                try:
                    for row in reader :
                        # get the location the variable to extract
                        if first:
                            for key in keys:
                                locs.append(row.index(key))
                            first = False
                        else:
                            sentence =""
                            for loc in locs:
                                sentence=sentence+" "+row[loc]
                            yield sentence             
                except:
                    print (fname + " has an error")
                csvfile.close()

"""
  Helper function for reading from a directory of CSVs into a pandas dataframe    dirname: the name of the directory of CSVs
"""
def read_df(dirname):
    frame = pd.DataFrame()
    df_list =[]
    fnames = glob.glob(dirname + "/*.csv")
    for fname in fnames:
        df = pd.read_csv(fname,header=0)
        df_list.append(df)
    frame = pd.concat(df_list)
    return frame
        

# Takes a string and returns a cleaned version                
def cleanSentence(sentence):
    # remove deleted sentences
    if sentence == "[deleted]":
        return ""
    else:
        # remove case
        sentence = sentence.lower()
        # remove special characters
        exclude = "[•…“”\_\-,.;:\)\(\[\]0123456789/?&#%+@\\\=\*$\"!\r~\n\^]"
        temp = re.sub(exclude," ",sentence)
        return re.sub("[^a-z\ ]","",temp)
"""
    Takes a string and returns a version where all links have been
    replaced with the word link
"""
def remove_links(sentence):
    pattern="http://[^ \n\r]*"
    return re.sub(pattern," link ",sentence)


"""
Save and load utility files
Taken in part from:
https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file
"""
def save_object(obj,dir, name ):
    with open(dir + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_object(dir,name):
    with open(dir + name + '.pkl', 'rb') as f:
        return pickle.load(f)

