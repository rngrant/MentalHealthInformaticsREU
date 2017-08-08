import bz2
import urllib.request
import os
import csv
import json
import datetime

# define user_agent so http request is not denied
user_agent = 'Chrome'
headers={'User-Agent':user_agent}

months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

# prompt user for information
startyear = input('Start year: ')
endyear = input('End year: ')
text = input('Posts or Comments? (p/c): ').lower()
allUserPosts = input('User Posts from All of Reddit? (y/n): ').lower()

if text == 'p':
	file = 'fields.csv'
elif text == 'c':
	file = 'commentFields.csv'
else:
	print('Error, invalid Posts/Comments input')
	exit(1)

if (allUserPosts != 'y') and (allUserPosts != 'n'):
	print('Error, invalid User Posts input')

subreddits =[]
try:
    subreddits_file = open('subreddits.csv', 'r')
except:
    print('Error: Could not open subreddits.csv')
    exit(2)
subreddit_reader = csv.reader(subreddits_file,delimiter=',', quotechar='\"')
for subreddits_list in subreddit_reader:
    subreddits = subreddits_list

# open 'fields.csv' or 'commentFields.csv' and read as a csv, otherwise return an error
try:
    fields_file = open(file, 'r')
except:
    print('Error: Could not open fields file')
    exit(2)

# if fields.csv exists, enter
fields_reader = csv.reader(fields_file, delimiter=',', quotechar='\"')
for words in fields_reader:
    fields = words

# create a log file to write program output
with open("log.txt", "a") as f:
	f.write("NEW RUN: Time: " + str(datetime.datetime.now()) + ", Start Year: " + startyear + ", End Year: " + endyear + ", Text: " + text + ", All User Posts: " + allUserPosts + "\n")

# define a function that will read a JSONLines file with fields from fields.txt
def parsejson(infile, suffix, subreddits, fields):
	# open csv output files, with the given suffix
    csvfiles = []
    writers  = []
    users = []
    for i in range(len(subreddits)):
        csvfile = open(subreddits[i] + "_" + suffix, 'w')
        writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        csvfiles.append(csvfile)
        writers.append(writer)
        users.append([])
    # check to see if json has key, if not, return empty string
    def getValue(key, submission):
        if key in submission:
            return submission[key]
        return ""

	# open jsonlines file, iterate through each line, which is a json object,
    with open(infile) as f:
    	# write a row of headings
        for writer in writers:            
            writer.writerow(fields)
        for line in f:
        	# try to load an object from line, otherwise print error and move on
                # load object in current line as submission
            submission = (json.loads(line))
                # if object is of desired subreddit, then load its contents into csv
            # if the user required all user posts, find all users within a particular subreddit
            if allUserPosts == 'y':
            	for i in range(len(subreddits)):
            		if getValue('subreddit', submission) == subreddits[i]:
            			users[i].append(getValue('author', submission))
            	# write all posts by those particular users
            	for i in range(len(subreddits)):
            		if getValue('author', submission) in users[i]:
            			writers[i].writerow(list(map(lambda field: getValue(field,submission),fields)))
            # else, if object is of desired subreddit, then load its contents into csv
            elif allUserPosts == 'n':
            	for i in range(len(subreddits)):
            		if getValue('subreddit', submission) == subreddits[i]:
            			writers[i].writerow(list(map(lambda field: getValue(field,submission),fields)))
    # close files
    for csvfile in csvfiles:
    	csvfile.close()


# repeat over how many years user desires
for year in range(int(startyear), int(endyear) + 1):
    for month in months:
    	# create file name from year according to download format from https://files.pushshift.io
    	if text == 'p':
    		file_name = "RS_" + str(year) + "-" + month + ".bz2"
    		# create url to download file
    		file_url = "http://files.pushshift.io/reddit/submissions/" + file_name
    	elif text == 'c':
    		file_name = "RC_" + str(year) + "-" + month + ".bz2"
    		# create url to download file
    		file_url = "http://files.pushshift.io/reddit/comments/" + file_name
    	# create output file in format year-month.csv
    	if allUserPosts == 'y':
    			csvfile = str(year) + "-" + month + "-" + text + '-U' + ".csv"
    	csvfile = str(year) + "-" + month + "-" + text + ".csv"
    	
    	# request the file from the current year and month
    	request = urllib.request.Request(file_url, None, headers)
    	response = urllib.request.urlopen(request)
    	# try to decompress and write the data into a temp file, if it exists(some data from 2006 and 2007 is missing)
    	try:
    		# decompress data
    		try:
    			data = bz2.decompress(response.read())
    		except:
    			with open("log.txt", "a") as f:
    				f.write("Reddit data for the month: " + month + " and year: " + str(year) + " is missing." + "\n")
    		# write into "temp" file which is overwritten for each month to save memory
    		with open("temp", "wb") as code:
    			code.write(data)
    		# call parsejson function to go through the decompressed file and select the desired fields from the desired subreddit
    		parsejson("temp", csvfile, subreddits, fields)
    	# if data is missing, print year and month of missing data
    	except:
    		with open("log.txt", "a") as f:
    			f.write("Error processing Reddit data for the month: " + month + " and year: " + str(year) + "\n")

# remove temp file
if os.path.isfile("temp"):
	os.remove("temp")
# write lines to log file to separate runs
with open("log.txt", "a") as f:
	f.write("\n\n\n")