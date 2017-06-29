import gensim, logging, os, csv
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

# Takes a string and returns a cleaned version                
def cleanSentence(sentence):
    # remove deleted sentences
    if sentence == "[deleted]":
        return ""
    else:
        # remove case
        sentence = sentence.lower()
        # remove special characters
        exclude = ",.;:)([]0123456789/?*$\"!~\n^"
        return ''.join(ch for ch in sentence if ch not in exclude)


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

