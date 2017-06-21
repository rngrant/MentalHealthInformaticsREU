# Reddit Scraper overview

The files in this directory are used to aquire
and parse past reddit data. The data is aquired from
http://files.pushshift.io/ in line delimited JSON format,
and is parsed to a CSV containing selected fields from a
specific subreddit. This program returns entire years of data, 
from which one can select the data one needs.

To run this program, one needs at least 20 GB of ram, as the
decompressed files reach up to 18 GB in size. One can do this
while running an ec2 instance on Amazon Web Services for a few
hours.
