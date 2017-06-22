import gensim, logging, os, csv

def read(dirname,str):
        for fname in os.listdir(dirname):
            first = True
            loc =0
            with open(dirname+ "/"+fname,'r') as csvfile:
                reader = csv.reader(csvfile,dialect='excel',delimiter=',',quotechar='\"')
                try:
                    for row in reader :
                        if first:
                            loc = row.index(str)
                            first = False
                        else:
                            yield row[loc]                            
                except:
                    print (fname + " has an error")
                csvfile.close()

