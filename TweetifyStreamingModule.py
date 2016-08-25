# TweetifyStreamingModule.py
# Marco Garcia

import re
from twython import TwythonStreamer
from twython import Twython

class TweetifyStreamingParser(TwythonStreamer):

	def __init__(self, CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET, TweetifyDaemonModule):
		self.tweetifydaemonmodule = TweetifyDaemonModule
		super(TwythonStreamParser, self).__init__(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

	def on_success(self, data):
		print data
		if 'text' in data:
			text = data['text'].encode('utf-8')
			print 'tweet: ', text
			self.tweetifydaemonmodule.sender = data['user']['screen_name'].encode('utf-8')
			print "sender: ", self.tweetifydaemonmodule.sender
			if len(data['entities']['hashtags']) > 0 :
				self.tweetifydaemonmodule.hashtag = data['entities']['hashtags'][0]['text'].encode('utf-8')
			else :
				self.tweetifydaemonmodule.hashtag = ""
			print "hashtag: ", self.tweetifydaemonmodule.hashtag
			self.tweetifydaemonmodule.parse_tweet(text)

	def on_error(self, status_code, data):
		print status_code