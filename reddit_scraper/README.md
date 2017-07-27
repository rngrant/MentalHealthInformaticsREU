# Reddit Scraper overview

The files in this directory are used to aquire
and parse past reddit data. The data is aquired from
http://files.pushshift.io/ in line delimited JSON format,
and is parsed to a CSV containing selected fields from specific
subreddits. The fields for submissions should be specified in 'fields.csv',
the fields for comments should be specified in 'commentFields.csv', and 
subreddits should be specified in 'subreddits.csv'.
This program returns entire years of data, from 
which one can further filter the data one needs if neccessary.

If acquiring submissions, the program needs at least 20 GB of RAM, as the
decompressed files reach up to 18 GB in size. One can do this
while running an ec2 instance(t2.2xlarge) with 30GiB in EBS Storage.

If acquiring comments, the program will need more resources, as the files are larger.
We recommend about 60 GB of RAM and Storage, which can be achieved with an m4.4xlarge instance.

Tutorial:
Reddit Scraper Walkthrough
This is a walkthrough of our process of obtaining reddit archives on posts. A limitation of reddit is that they store a limited amount of posts on each subreddit, in the case of the subreddit SuicideWatch, only the past 1000 posts were available, which limited the data we could get through the use of the Reddit API. That being said, the Reddit API could be very useful if one needs very recent posts. Our exploration with that is described in a different document.

Getting Started

To run the python scraper, you will likely need to launch a virtual machine through some server. We used Amazon web services. To do this, you can create an amazon web services account, and create an EC2 instance. We recommend creating an Ubuntu 16.04 instance because it allows you to use Python 3.6 which we used to write the program. 

When setting up the instance, you will need to select an instance type that has at least 20 GB of  both RAM and storage, we would recommend the t2.2xlarge instance which provides 32 GiB of RAM, and ensuring that you have at least 30 GiB of storage.

Once these are selected, you can select ‘Review and Launch’, and Launch your instance. There will be a notification about security keys. If you have a key pair already made, feel free to use that, otherwise make a new key pair, and download it into the directory in which you wish to work.

Getting the code
The code is attached in this folder if you feel more comfortable downloading it from here and copying it into the correct directory

Our program is stored on GitHub, with which I will assume you are familiar. The link to the repository is the following: https://github.com/pages0/MentalHealthInformaticsREU.git

You can execute

git clone https://github.com/pages0/MentalHealthInformaticsREU.git

In the directory in which you wish to work, which should also have the key pair from amazon web services(keyname.pem). Once downloaded, you can move the reddit scraper files from the folder inmoreg
cd MentalHealthInformaticsREU/reddit_scraper
mv *  ../..
cd ../..
rm -r MentalHealthInformaticsREU
(respond ‘y’ without quotes to both prompts)
ls

Now, README.md, fields.csv, commentFields.csv, subreddits.csv, and redditscrape.py should all be in your directory with the key.pem file that you made. By running ls, you should have seen these files.

Running the Program
This program will download reddit archives from https://files.pushshift.io, then decompress them and iterate through the JSONLines format file while searching for the subreddit which you specify, and print the fields that you wish to obtain into a csv file, which can be easily viewed in an excel table.

First, begin by opening fields.csv, commentFields.csv, and subreddits.csv in a text editor, and changing any fields you wish to get your desired information. A list of most keys can be found in the README.md. If this is not sufficient, simply head to reddit.com in a web browser, then click on a post that leads to a reddit page with the post and the comments. After loading, simply type “.json” at the end of the address(after the last slash) to see the text file that the page displays, and from there you can see the key value pairs with keys such as “created_utc” or “selftext”. Use these key names in the same format that fields.csv has them. You can do a similar task for commentFields.csv. For subreddits.csv, type the name of the subreddit as it is found in the url of the subreddit you want. Ex: SuicideWatch,ptsd,depression,etc.

NOTE: Be sure that the keys and subreddit names are ONLY separated by commas, and do not have spaces, as seen above in the list of subreddits, otherwise you will not retrieve any usable data.

Then, going back to the command line, you must transfer these files over to the server you created. First you must obtain the public IP address of the instance you created. This can be found in the EC2 dashboard, by clicking running instances, and selecting your instance. The public IP address will be listed on the right side in the information window beneath the list of instances. Copy that address. Then in the command line execute

chmod 400 [key].pem
scp -i [key].pem redditscrape.py ubuntu@[public IP address]:~ 
scp -i [key].pem fields.csv ubuntu@[public IP address]:~ 
scp -i [key].pem commentFields.csv ubuntu@[public IP address]:~ 
scp -i [key].pem subreddits.csv ubuntu@[public IP address]:~ 

Where you replace [key] with the name of your key and [public IP address] with the public IP you copied earlier. Running chmod 400 changes the permissions on the key to make it more secure, and bypasses an error which may be raised when connecting to the virtual machine. REMEMBER to include the :~ at the end of the command or else you will get an error! This tells scp where to copy the file. If this command was successful then you should see a line with 100%, the file name, and other information. Then, we must connect to the ec2 instance, and download python3.6.

To connect to your instance, you will use ssh. You can connect to your virtual machine by running the following command

ssh -i [key].pem ubuntu@[public IP address]

Again, where you replace [key] with the name of the your key and [public IP address] with the public IP you copied earlier. If you ever receive an ‘error(publickey)’ error, then you or your key were in the wrong directory, or ‘ubuntu’ is misspelled. Upon success, you should see a different prompt at your command terminal, which will probably be green. Executing the following will ensure that the code we sent over is in the correct directory

ls 

The files present should be redditscrape.py, fields.csv, commentFields.csv, and subreddits.csv. To download python3.6, enter the following commands: NOTE: press enter at the prompt of the first command, and ‘y’ at the prompt of the third command

sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update 
sudo apt-get install python3.6

After this has been completed, you are are ready to run the code!

Simply run the program and answer the prompts, being sure to answer the prompts with correct spelling. Run by executing

python3.6 redditscrape.py
[Answer the prompts]
“Ctrl” + “Z”
bg
disown -h %1


The last three commands are very important to execute so that you can disconnect from the server and the process will continue to run. To check the status, simply execute ‘ps -ef’, and look for the python3.6 command. The program will search for ‘fields.csv and subreddits.csv’, so be sure to include it, otherwise it will exit with a message. To fetch only 1 year of data, enter start year and end year as the same year. NOTE: be sure to find out when your desired subreddit was created, as it may not have existed in all of reddit’s history, which would return no usable data for you.

Retrieving the data
Once a month is completed, which occurs if the next month’s csv has been created or the process ends, you will be able to retrieve completed data from the virtual machine. To do so, open a new terminal window on your local machine, and navigate to the directory which contains your [key].pem file using ‘ls’, which lists the contents of your directory, and cd [directory name], which moves you into a directory which is in your current directory. To go to the parent directory, execute ‘cd ..’. Again, you will need the public IP address of your instance. After navigating to the directory which has [key].pem in it, execute the following code to retrieve your data which is in the format year-month.csv:

mkdir RedditData
scp -i [key].pem ubuntu@[public IP address]:[year]-[month].csv RedditData

Repeat this for as many files as you have on the server, replacing [key] with the name of the private key you have, and [public IP address] with the public IP address you copied. You will also have to change the name of the file you are copying over for each month you want copied. For example, if I wanted to copy over the file from January 2006, I would use 2006-01.csv. This will copy files into a directory called RedditData(this also makes the ‘scp’ command easier since the destination path is very simple), from which you can easily access the data. If you like, you can use ‘ssh’ to get into the virtual machine and use the ‘rm [filename]’ command to free up space if you have a particularly large range of years of data.

This concludes this tutorial, and if you have any questions, feel free to contact my team at these emails: dkucher@umich.edu, grantrei@grinell.edu.


