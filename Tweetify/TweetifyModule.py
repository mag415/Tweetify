# TweetifyModule.py
# Marco Garcia

import TweetifyStreamingModule
import ConfigParser
from twython import Twython

config = ConfigParser.ConfigParser()
config.read('TweetifyConfig.ini')

ConsumerKey = config.get('Twitter','ConsumerKey')
ConsumerSecret = config.get('Twitter','ConsumerSecret')
AccessKey = config.get('Twitter','AccessKey')
AccessSecret = config.get('Twitter','AccessSecret')
TwitterAccount = config.get('Twitter','TwitterAccount')

twitter = Twython(ConsumerKey,ConsumerSecret,AccessKey,AccessSecret)

def start_twitter_listener(tweetifydaemonmodule):
	print "Waiting for tweets to ", TwitterAccount, "..."

	stream = TweetifyStreamingModule.TweetifyStreamingParser(ConsumerKey,ConsumerSecret,AccessKey,AccessSecret, tweetifydaemonmodule) 
	stream.statuses.filter(track=TwitterAccount)

def send_tweet(text):
	print "sending tweet: ", text
	twitter.update_status(status=text)
