import bz2
import urllib.request
import os
import csv
import sys
import json

# define user_agent so http request is not denied
user_agent = 'Chrome'
headers={'User-Agent':user_agent}

months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

# prompt user for information
subreddit = input("Subreddit: ")
startyear = input("Start year: ")
endyear = input("End year: ")
fields_file = input("Name of file with fields: ")

# open fields_file and read as a csv, then set contents equal to fields array
fields_file = open(fields_file, 'r')
reader = csv.reader(fields_file, delimiter=',', quotechar='\"')
for words in reader:
    fields = words

# define a function that will read a JSONLines file with fields from fields.txt
def parsejson(infile, outfile, subreddit, fields):
       
       # open csv output file, named outfile
       csvfile = open(outfile, 'w')
       writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)

       # check to see if json has key, if not, return empty string
       def getValue(key, submission):
              if key in submission:
                     return submission[key]
              return ""

       # open jsonlines file, iterate through each line, which is a json object,
       with open(infile) as f:
              # write a row of headings
              writer.writerow(fields)
              for line in f:
                     # load object in current line as submission
                     submission = (json.loads(line))
                     # if object is of desired subreddit, then load its contents into csv
                     if getValue('subreddit', submission) == subreddit:
                            writer.writerow(list(map(lambda field: getValue(field,submission),fields)))
       # close files
       csvfile.close()

# repeat over how many years user desires
for year in range(int(startyear), int(endyear) + 1):
    for month in months:
        string = "RS_" + str(year) + "-" + month + ".bz2"
        csvfile = str(year) + "-" + month + ".csv"
        file_url = "http://files.pushshift.io/reddit/submissions/" + string

        request = urllib.request.Request(file_url,None,headers) #The assembled request
        response = urllib.request.urlopen(request)
        try:
            data = bz2.decompress(response.read())
        
            with open("temp", "wb") as code:
                code.write(data)

            parsejson("temp", csvfile, subreddit, fields)
        except:
            print("Reddit data for the year: "+ str(year) + " and month: " + month + " is missing.")

# remove temp file
os.remove("temp")
