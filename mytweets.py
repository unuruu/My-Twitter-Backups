# mytweets.py - Creates an archive of your tweets as a Git repo
# Sankha Narayan Guria <sankha93@gmail.com>

import sys, httplib, os.path, json, subprocess

con = httplib.HTTPConnection("api.twitter.com")

def getTweets(num):
	request = "";
	if(num == -1):
		request = "/1/statuses/user_timeline.json?screen_name=" + sys.argv[1] + "&count=200&include_rts=1&trim_user=1"
	else:
		request = "/1/statuses/user_timeline.json?screen_name=" + sys.argv[1] + "&count=200&include_rts=1&trim_user=1&since_id=" + num
	return doRequest(request)

def doRequest(request):
	con.request("GET", request)
	r = con.getresponse()
	return json.load(r)

def processTweets(obj):
	if(len(obj) == 200):
		maxid = (obj[-1])['id'] - 1
		if(tweet_id == -1):
			request = "/1/statuses/user_timeline.json?screen_name=" + sys.argv[1] + "&count=200&include_rts=1&trim_user=1&max_id=" + str(maxid)
		else:
			request = "/1/statuses/user_timeline.json?screen_name=" + sys.argv[1] + "&count=200&include_rts=1&trim_user=1&max_id=" + str(maxid) + "&since_id=" + tweet_id
		processTweets(doRequest(request))
		
	for tweet in reversed(obj):
		f = open("tweet_id",'w')
		f.write(tweet['id_str'])
		f.close()
		subprocess.call(["git", "add", "."])
		subprocess.call(["git", "commit", "--date", tweet['created_at'], "-m", tweet['text']])

if len(sys.argv) > 1:
	if(os.path.exists("tweet_id")):
		tweet_id = open("tweet_id", 'r').read()
	else:
		tweet_id = -1
	processTweets(getTweets(tweet_id))
else:
	print("Usage: python mytweets.py username")
