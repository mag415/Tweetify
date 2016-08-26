# TweetifyDaemonModule.py
# Marco Garcia

from mpd import MPDClient
import datetime, time, threading
import TweetifyModule
import spotipy
import LcdWriter
import ConsoleWriter
import imp

# check to see if we can write to lcd
try:
	imp.find_module('smbus')
	found = True
except ImportError:
	found = False
threadLock = threading.Lock()

if found: 
	output = LcdWriter.LcdWriter()
else:
	output = ConsoleWriter.ConsoleWriter()

class TweetifyDaemonModule():
	def __init__(self):
		self.client = MPDClient()
		self.spotipy = spotipy.Spotify()

		# Tweet info
		self.sender = ""
		self.hashtag = ""

		# Now playing info
		self.artist = ""
		self.album = ""
		self.song = ""

		self.send_message = False
		self.update_message_sleep = 6
				
# Connection functions
	def check_now_playing(self):
			while 1 :
					if self.send_message == True:
							self.send_message = False
							time.sleep(self.update_message_sleep)
					else :
							time.sleep(1)

					threadLock.acquire()
					if self.now_playing_changed():
							print "now playing changed"
							now_playing = self.client.currentsong()
							self.artist = now_playing['artist']
							self.album = now_playing['album']
							self.song = now_playing['title']
							self.update_now_playing()
					threadLock.release()

	def start_mpd(self):
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		print "Starting Tweetify!"
		self.write_message("Hi I'm Tweetify!", "I can play music for you.", "Tweet me at @TweetifyBox", "")
		self.check_mpd_connection()
		self.client.clear()
		self.play_song("jumpman")

		t = threading.Thread(target=self.check_now_playing, args=())
		t.daemon = True
		t.start()
				
		TweetifyModule.send_tweet("Starting Tweetify!" + " (" + st + ")")
		TweetifyModule.start_twitter_listener(self)

	def check_mpd_connection(self):
			try :
					self.client.ping()
			except :
					try :
							# network timeout in seconds (floats allowed), default: None
							self.client.timeout = 30
							# connect to localhost:6600
							self.client.connect("localhost", 6600)
							print "Connecting to MPD!"
					except:
							print "Connection failed!"

	def close_mpd(self):
		# send the close command
		client.close()
		client.disconnect()

# Helper functions
	def parse_tweet(self, tweet):
		print 'parsing tweet: ', tweet
		scrubbedtweet = tweet.replace('@'+TweetifyModule.pi_twitter_account, "")
		print scrubbedtweet

		if not self.hashtag :
			print 'didn\'t find command'
			self.play_song(scrubbedtweet)
		else :
			print 'found command: ', self.hashtag
			self.mpd_commands(self.hashtag)

	def now_playing_changed(self):
			now_playing = self.client.currentsong()
				
			if 'artist' in now_playing :
					if self.artist != now_playing['artist'] :
							return True

			if 'album' in now_playing :
					if self.album != now_playing['album'] :
							return True

			if 'title' in now_playing :
					if self.song != now_playing['title'] :
							return True
			return False

	def write_message(self, row1, row2, row3, row4) :
			self.send_message = True
			output.write(row1,row2,row3,row4)
		
	def update_now_playing(self) :
			now_playing = self.client.currentsong()
			output.write("Now Playing...",self.song,self.artist,self.album)
		
# Controlling playback
	def search_track(self, searchtext):
			self.write_message("Got tweet from ", self.sender, "Searching for track ", searchtext)
			results = self.spotipy.search(q='track:' + searchtext, limit=1, offset=0, type='track')

			items = results['tracks']['items']

			if len(items) > 0:
				track = items[0]
				print "Adding track ", track['name']
				self.client.add(track['uri'])
			else :
					print "No tracks for ", searchtext, " found"
				
	def mpd_commands(self, command):
		print "getting command: ", command
		switcher = {
			'play': self.play,
			'pause': self.pause,
			'next': self.next,
			'previous': self.previous,
			#'shuffle': self.shuffle,
			'setvolume': self.setvolume,
			'help': self.help }
		func = switcher.get(command, self.unknowncommand)
		return func()

	def play_song(self, searchtext):
		self.check_mpd_connection()
		print "calling play_song"
		print "searching for : ", searchtext

		self.search_track(searchtext)
		#if self.client.status()['state'] != 'play' :
		self.client.play()

	def next(self):
		self.check_mpd_connection()
		print "calling next"
		self.client.next()

	def pause(self):
		self.check_mpd_connection()
		print "calling pause"
		self.client.pause()

	def play(self):
		self.check_mpd_connection()
		print "calling play"
		self.client.play()

	def previous(self):
		self.check_mpd_connection()
		print "calling previous"
		self.client.previous()

	def setvolume(self):
		self.check_mpd_connection()
		print "calling set volume"
		self.client.setvol(100)
	
	def help(self):
		print "sending help instructions"

	def unknowncommand(self, command):
		print "command ", command, " not known"
		TweetifyModule.send_tweet("@" + self.sender + " you sent an invalid command (" + command + ")")
