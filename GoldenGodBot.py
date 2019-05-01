import praw
import GGBconfig
import time
import datetime
import os
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getQuote():
    quote = []

    for line in open('quotes.txt', 'r'):
        quote.append(line.strip().split('>')) 

    return str(*random.choice(quote))

def bot_login():
	print "Logging in..."
	r = praw.Reddit(username = GGBconfig.username,
				password = GGBconfig.password,
				client_id = GGBconfig.client_id,
				client_secret = GGBconfig.client_secret,
				user_agent = "Golden God")
	print "Logged in!"
	print "\n"
        r.redditor('Asterlux').message('Golden God!',"Active")
	return r

def run_bot(r, comments_replied_to):
	quoteSent = ""
	subreddit = r.subreddit('IASIP')
	#for comment in r.subredditIP').comments(limit=200):
        for comment in subreddit.stream.comments(pause_after=-1):
		if "golden god" in comment.body.lower() and comment.id not in comments_replied_to and comment.author != r.user.me():
			quoteSent = getQuote()
			try:
			    r.redditor('Asterlux').message('Golden God!',comment.permalink)
			    comment.reply(quoteSent)
			except Exception as e:
			    print "Reply error: "
			    print str(e)
                        now = datetime.datetime.now()
			print "----------------"
			print str(now)
			print "\n"
			print comment.body
			print "\n"
			print "\n"
			print quoteSent
			print "----------------"
			comments_replied_to.append(comment.id)
			with open ("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")

	#time.sleep(10)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to


r = bot_login()
comments_replied_to = get_saved_comments()

while True:
    try:
        run_bot(r, comments_replied_to)
    except Exception as e:
        print "Error: " + str(e)
        time.sleep(100);
