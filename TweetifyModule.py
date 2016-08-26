# TweetifyModule.py
# Marco Garcia

import TwythonStreamModule
from twython import Twython

CONSUMER_KEY = 'OnGuo3ldYW7IB0jDInYG4lOCq'
CONSUMER_SECRET = 'fEId8XZxt35go1bzmeAmfhi8gcGF14J0mlgXGH4tOzVbGXFl1c'
ACCESS_KEY = '701452267841433600-sceZ1oM8LHK8MIkMVsjMLjTbEunmhFV'
ACCESS_SECRET = 'MIOaDJPslYOFYe6VA07r3j10IiPCpsFyEKKJ5t6kbkoUz'
pi_twitter_account = "PidoraBox"

twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

def start_twitter_listener(tweetifydaemonmodule):
	print "Waiting for tweets to ", pi_twitter_account, "..."

	stream = TweetifyStreamingModule.TweetifyStreamingParser(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET, tweetifydaemonmodule) 
	stream.statuses.filter(track=pi_twitter_account)

def send_tweet(text):
	print "sending tweet: ", text
	twitter.update_status(status=text)
