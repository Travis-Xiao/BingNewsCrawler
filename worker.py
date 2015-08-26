import urllib2
import urllib
import globals
import threading


__author__ = 'Travis'




class WorkerCaptain:
	whipping = False

	def __init__(self):
		pass

	def whip(self):
		self.whipping = True
		while len(globals.link_list) != 0:
			globals.lock.acquire()
			thread = threading.Thread(target=worker, args=(globals.link_list.pop(), ))
			globals.lock.release()
			thread.start()
			print "whipping..."

		self.whipping = False

	def is_whipping(self):
		return self.whipping
