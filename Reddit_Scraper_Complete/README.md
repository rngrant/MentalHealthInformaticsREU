# Reddit Scraper overview

The files in this directory are used to aquire
and parse past reddit data. The data is aquired from
http://files.pushshift.io/ in line delimited JSON format,
and is parsed to a CSV containing selected fields from specific
subreddits. The fields should be specified in 'fields.csv', and 
subreddits should be specified in 'subreddits.csv'.
This program returns entire years of data, from 
which one can further filter the data one needs if neccessary.

To run this program, one needs at least 20 GB of RAM, as the
decompressed files reach up to 18 GB in size. One can do this
while running an ec2 instance on Amazon Web Services for a few
hours.
