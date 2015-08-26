import urllib2
import urllib
import globals
import re
from pyquery import PyQuery


def process_url(url):
	# generate unique file name for storage
	url_unquoted = urllib2.unquote(url.decode('utf8'))
	globals.m.update(url_unquoted)
	url_unquoted = globals.regex.sub(' ', url_unquoted)
	url_unquoted = url_unquoted.replace(' ', '_')
	storage_file = globals.m.hexdigest()[:6] + "_" + url_unquoted + ".html"
	urllib.urlretrieve(url, globals.output_dir + storage_file)


def extract_links(page):
	d = PyQuery(page)
	links = d('.newstitle>a')
	entries = []

	for link in links:
		link = PyQuery(link)
		# get title and link from html
		title = link.text().encode("utf-8")
		link = link.attr('href')
		entries.append((title, link))

	return entries


def extract_hints(page):
	tag_pattern = re.compile('"Txt":"[a-zA-Z0-9 ]+"')
	raw_hints = tag_pattern.findall(page)
	hints = []

	# print hints
	for hint in raw_hints:
		trimmed_hint = hint.replace('"Txt":"', '').replace('"', '')
		hints.append(trimmed_hint)

	return hints
