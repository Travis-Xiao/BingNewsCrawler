import requests
import threading
import re
import os
from globals import *
import procedure


manager_running = False


def seeding():
	# global keyword_queue
	r = requests.get(bing_hint_request_url, bing_hint_request_params)
	page = r.text

	hints = procedure.extract_hints(page)

	for hint in hints:
		keyword_queue.add(hint)
		m.update(hint)
		covered_keyword.add(m.hexdigest())


def search(keyword):
	request = bing_news_base + keyword.replace(' ', '+')
	r = requests.get(request)
	page = r.text
	
	entries = procedure.extract_links(page)

	lock.acquire()

	for title, link in entries:
		print title.decode("utf8")
		m.update(title)
		title_hashcode = m.hexdigest()

		if title_hashcode in covered_keyword:
			continue

		keyword_queue.add(title)
		covered_keyword.add(title_hashcode)
		pool.add_task(procedure.process_url, link)
	lock.release()

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
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	seeding()
	# print keyword_queue
	process()
