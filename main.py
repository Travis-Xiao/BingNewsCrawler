import requests
import threading
from pyquery import PyQuery
import re
from globals import *


manager_running = False


def seeding():
	# global keyword_queue
	r = requests.get(bing_hint_request_url, bing_hint_request_params)
	page = r.text
	tag_pattern = re.compile('"Txt":"[a-zA-Z0-9 ]+"')
	hints = tag_pattern.findall(page)
	# print hints
	for hint in hints:
		trimmed_hint = hint.replace('"Txt":"', '').replace('"', '')
		keyword_queue.add(trimmed_hint)

		m.update(trimmed_hint)
		covered_keyword.add(m.hexdigest())


def search(keyword):
	request = bing_news_base + keyword.replace(' ', '+')
	r = requests.get(request)
	page = r.text
	# print page.encode("utf-8")
	d = PyQuery(page)
	links = d('.newstitle>a')
	# print links

	extend_keyword_link = []
	extend_keyword_hashcode = []
	extend_link_list = []

	for link in links:
		link = PyQuery(link)
		# get title and link from html
		title = link.text().encode("utf-8")
		link = link.attr('href')
		print title
		m.update(title)
		extend_keyword_hashcode.append(m.hexdigest())
		extend_link_list.append(link)
		extend_keyword_link.append(title)

	lock.acquire()
	for i in range(len(extend_keyword_link)):
		# if the keyword has already been processed
		if extend_keyword_hashcode[i] in covered_keyword:
			continue
		keyword_queue.add(extend_keyword_link[i])
		covered_keyword.add(extend_keyword_hashcode[i])
		link_list.append(extend_link_list[i])
	lock.release()

	if not worker_captain.is_whipping():
		worker_captain.whip()

	if not manager_running:
		process()

def process():
	global manager_running
	manager_running = True
	print "manager thread starting..."
	while len(keyword_queue) != 0:
		# TODO
		# assign to an isolated worker
		lock.acquire()
		thread = threading.Thread(target=search, args=(keyword_queue.pop(), ))
		lock.release()
		thread.start()

	manager_running = False
	print "manager thread exiting..."

if __name__ == "__main__":
	seeding()
	print keyword_queue
	process()
