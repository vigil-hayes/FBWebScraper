import sys
import os
import csv
import re
from subprocess import call
from runspider import runspider

finalout=sys.argv[1]

def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def clean_string(string):
	string = strip_non_ascii(string)
	string = re.sub('[\t\n\r\\\/,.:;%&]',' ',string)
	string = re.sub('  ', ' ', string)
	return string

with open('../all_posts2.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter='\t')
	for row in csvreader:
		print(row)
		# Read in the URL
		url=row[7]
		if(url == "NONE" or ("facebook.com" in url)):
			continue
		print("URL = %s" % url)

		# Write it to a tmp file
		with open("/Users/spiderwoman/Dropbox/CitizenNet/facebook/facebook-sdk/incomplete_07312015/tutorial/url.tmp", 'w') as urlout:
			urlout.write(url)
			print("Wrote to url file")
		print("Before running the spider")

		try:
			# Call the scraper
			if(os.system("scrapy crawl dmoz --logfile=getcontent.log -o content.csv -t csv")):
				print("SCRAPY failed!")
			#call(["scrapy crawl dmoz","--logfile=getcontent.log","-o","content.csv","-t","csv"], shell=True)
			print("After running the spider")
			# Scraped successfully
			with open("/Users/spiderwoman/Dropbox/CitizenNet/facebook/facebook-sdk/incomplete_07312015/tutorial/content.csv", 'r') as contentfile:
				# Read in all the content and store it as one string
				contentreader = csv.reader(contentfile, delimiter="\t")
				content=""
				for line in contentreader:
					content+=" "
					content+=line[0]
				# Clean the string
				content=clean_string(content)
				print("CONTENT = %s" % content)

				# Write to file
				curline='\t'.join(row) + content + "\n"

				# Open the output file
				print("Write to output file")				
				with open("/Users/spiderwoman/Dropbox/CitizenNet/facebook/facebook-sdk/incomplete_07312015/tutorial/%s" % finalout, 'a') as outfile:
					outfile.write(curline)
			os.system("rm content.csv")
		except Exception as e:
			print("***EXCEPTION: %s ***" % e)
			continue
			
				
		 
