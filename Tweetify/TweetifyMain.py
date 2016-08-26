# TweetifyMain.py
# Marco Garcia

import TweetifyStreamingModule
import TweetifyDaemonModule
import LcdWriter

tweetifydaemonmodule = TweetifyDaemonModule.TweetifyDaemonModule()
tweetifydaemonmodule.start_mpd()