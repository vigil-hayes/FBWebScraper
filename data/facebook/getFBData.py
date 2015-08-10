# Facebook contests
import requests
import re
import json
import csv
import sys
import subprocess
TOKEN="786517178131951|0VSgFwHkhn1yCC50vtQvR1X8A8o"
TIME="1438281890"
post_comments = {}
like_users= []
post_urls = []
# Get a list of page ids
def get_ids(infile):
	print("In get_ids")
        pages=[]
        with open(infile, 'rt') as csvfile:
                csvreader = csv.reader(csvfile, delimiter="\t")
                for row in csvreader:
                        pages.append(row[0])
        return pages

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def get_comments(post_id):
	print("In get_comments")
	url = 'https://graph.facebook.com/%s/comments' % post_id
	parameters = {'access_token': TOKEN}
	r = requests.get(url, params = parameters)
	result = json.loads(r.text)
	comments=result['data']
	comment_count = 0
	while True:
		try:
			if len(comments) == 0:
				break
			for c in comments:
				print("comment = %" % c)
				comment_count += 1
				cid = str(c['id'])
				c_createdat = str(c['created_time'])
				cuid = str(c['from']['id'])
				clikes = str(c['like_count'])
				try:
					message = strip_non_ascii(str(c['message']))
					message = re.sub('[\t\n\r]', ' ', message)
				except Exception:
					print("NO MESSAGE!")
					message = "NONE"
				post_comments["%s\t%s" % (post_id,cid)] = "%s\t%s\t%s\t%s" % (c_createdat, cuid, clikes, message)
				r = requests.get(comments['paging']['after'])
			result = json.loads(r.text)
			comments = result['data']	
			print(comments)		
		except KeyError:
			break
	return comment_count

def get_post_data(post, pid):
	print("In get_post_data")
	try:
		comment_count = 0
		post_id=str(post['id'])
		created_at=str(post['created_time'])
		if 'type' in post:
			post_type = str(post['type'])
		else:
			post_type = "NONE"
		if 'status_type' in post:
			status_type = str(post['status_type'])
		else:
			status_type = "NONE"
		try:
			if 'message' in post:
				caption=strip_non_ascii(str(post['message']))
				caption=re.sub('[\t\n\r]', ' ', caption)
			else:
				caption="NONE"
		except Exception:
			caption="NONE"
		if 'shares' in post:
			shares = str(post['shares']['count'])
		else:
			shares = 0
		try:
			if 'link' in post:
				link = str(post['link'])
			else:
				link = "NONE"
		except Exception:
			link = "NONE"
		like_count = 0
		if 'likes' in post:
			likes=post['likes']['data']
			for l in likes:
				like_count+=1
				like_users.append("%s\t%s" % (post_id, str(l['id'])))
		comment_count=get_comments(post_id)	
	except Exception as e:
		count=0
	with open("07312015/%s_post_info.csv" % pid, 'ab') as out:
		out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (created_at, post_id, post_type, status_type, like_count, comment_count, shares, link, caption))

def get_posts(page_id, pid):
	""" 
       	Returns the number of likes common to a post and the page
	"""
	print("In get_posts")
	count_likes = 0 
	url = 'https://graph.facebook.com/%s/feed?until=%s' % (page_id,TIME) 
	parameters = {'access_token': TOKEN}
	r = requests.get(url, params = parameters)
	result = json.loads(r.text)
	print(result)
	if 'data' in result:
		posts = result['data']
	else:
        	return
	while True:
		try:
			for post in posts:
				print(post)
				get_post_data(post, pid)
			r = requests.get(result['paging']['next'], params=parameters)
			result = json.loads(r.text)
			posts = result['data']
		except KeyError:
			break

def get_page_info(page_id):
    """ 
        Returns the number of likes common to a post and the page
    """
    print("In get_page_info")
    url = 'https://graph.facebook.com/%s' % (page_id) 
    parameters = {'access_token': TOKEN}
    r = requests.get(url, params = parameters)
    result = json.loads(r.text)
    if 'id' in result:
        pid = str(result['id'])
    else:
        pid = page_id
    if 'category' in result:
        category = str(result['category'])
    else:
        category = "NONE"
    try:
        if 'about' in result:
    	    about = strip_non_ascii(str(result['about']))
        else:
            about = "NONE"
    except Exception as e:
        about = "NONE"
    try:
        if 'description' in result:
            description = strip_non_ascii(str(result['description']))
        else:
            description = "NONE"
    except Exception as e:
        description = "NONE"

    if 'likes' in result:
        likes = str(result['likes'])
    else:
        likes = 0
    if 'release_date' in result:
        created_at = str(result['release_date'])
    else:
        created_at = "NONE"
    if 'website' in result:
        website = str(result['website'])
    else:
        website = "NONE"
    with open("07312015/%s_page_info.csv" % (pid), 'ab') as out:
        out.write("%s\t%s\t%s\t%s\t%s\t%s\%s\n" % (pid, created_at, category, likes, website, about, description))
    return pid

# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID     = '786517178131951'
FACEBOOK_APP_SECRET = '2e3f91a3f34407fbced1566ee276505c'
page_ids = []

if __name__ == '__main__':
# Read in data
# Look at the posts
	print("Starting program")
	idfile = "fm_fb_id.csv"
	#idfile = "nv1.csv"
	page_ids = get_ids(idfile)

	for page in page_ids:
		pid=get_page_info(page)
		get_posts(page, pid)  
		with open("07312015/%s_like_info.csv" % (pid), 'ab') as out:
			for l in like_users:
				out.write("%s\n" % l)
			like_users=[]
		with open("07312015/%s_comment_info.csv" % (pid), 'ab') as out:
                	for c in post_comments.keys():
                        	out.write("%s\t%s\n" % (c, post_comments[c]))
		post_comments = {}
	#sys.exit(0) 
