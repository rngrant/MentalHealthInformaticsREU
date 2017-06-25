import gensim, logging, os, csv

# Helper function for reading from a directory of CSVs
# dirname: the name of the directory of CSVs
# key: The name of the variable to extract from the CSV
# returns a generator that returns the next string in the file
def read(dirname,key):
        for fname in os.listdir(dirname):
            first = True
            loc =0
            with open(dirname+ "/"+fname,'r') as csvfile:                
                reader = csv.reader(csvfile,dialect='excel',delimiter=',',quotechar='\"')
                try:
                    for row in reader :
                        # get the location the variable to extract
                        if first:
                            loc = row.index(key)
                            first = False
                        else:
                            yield row[loc]                            
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
