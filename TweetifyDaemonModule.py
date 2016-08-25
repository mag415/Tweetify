# TweetifyDaemonModule.py
# Marco Garcia

import datetime, time
import re
import TwythonModule
from mpd import MPDClient
import LcdWriter

pi_twitter_account = "PidoraBox"

class TweetifyDaemonModule():
	def __init__(self):
		self.client = MPDClient()

                # Tweet info
		self.sender = ""
		self.hashtag = ""

                # Now playing info
                self.artist = ""
                self.album = ""
                self.song = ""
                
# Connection functions
	def start_mpd(self):
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		print "Starting PidoraBox!"
                self.check_mpd_connection()

                print self.client.commands()
                print self.client.notcommands()
                print self.client.tagtypes()

                self.play_song("diamonds future")
                #print self.client.find("any", "tupac")
                #self.client.add("spotify:artist:3TVXtAsR1Inumwj472S9r4")
                #self.client.setvol(100)
                #self.client.play()
                #print self.client.status()
                #self.client.next()
                #print self.client.playlist()
                self.client.play()
		TwythonModule.send_tweet("Starting PidoraBox!" + " (" + st + ")")
		TwythonModule.start_twitter_listener(self)

        def check_mpd_connection(self):
                try :
                        self.client.ping()
                except :
                        self.client.timeout = 30	# network timeout in seconds (floats allowed), default: None
                        self.client.connect("localhost", 6600)	# connect to localhost:6600
                        print "Connecting to MPD!"
                        
	def close_mpd(self):
		client.close()	# send the close command
		client.disconnect()

	def parse_tweet(self, tweet):
		print 'parsing tweet: ', tweet
		scrubbedtweet = tweet.replace('@'+TwythonModule.pi_twitter_account, "")
		print scrubbedtweet

		if not self.hashtag :
			print 'didn\'t find command'
			self.play_song(scrubbedtweet)
		else :
			print 'found command: ', self.hashtag
			self.mpd_commands(self.hashtag)

	# Controlling playback
        def update_now_playing(self) :
                now_playing = self.client.currentsong()
                print now_playing
                if now_playing["artist"] :
                        self.artist = now_playing["artist"]
                if now_playing["album"] :
                        self.album = now_playing["album"]
                if now_playing["title"] :
                        self.song = now_playing["title"]
                lcd = LcdWriter.LcdWriter()
                lcd.lcd_write_rows("Now Playing...",self.song,self.artist,self.album)
                
        def check_if_artist(self, file_name) :
                if "artist" in file_name :
                        return True
                else :
                        return False

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

	def play_song(self, searchtext):
                print self.client.currentsong()
                self.check_mpd_connection()
		print "calling play_song"
		print "searching for : ", searchtext
                
		results = self.client.search("any", searchtext)
                print "results : ", results
		
		first_file = results[0]["file"]
                
		print "found file: ", first_file

                if self.check_if_artist(first_file) :
                   print "clearing playlist"
                   self.client.clear()
		
		self.client.add(first_file)
		self.client.play()
		self.update_now_playing()

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
		TwythonModule.send_tweet("@" + self.sender + " you sent an invalid command (" + command + ")")
