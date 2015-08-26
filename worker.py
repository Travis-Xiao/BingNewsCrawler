import urllib2
import urllib
import globals
import threading


__author__ = 'Travis'


def worker(url):
	# generate unique file name for storage
	url_unquoted = urllib2.unquote(url.decode('utf8'))
	globals.m.update(url_unquoted)
	url_unquoted = globals.regex.sub(' ', url_unquoted)
	storage_file = globals.m.hexdigest()[:6] + "_" + url_unquoted + ".html"
	urllib.urlretrieve(url, globals.output_dir + storage_file)


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
