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

	for link, title in entries:
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
		pool.add_task(procedure.process_url, extend_link_list[i])
		# link_list.append(extend_link_list[i])
	lock.release()

	# if not worker_captain.is_whipping():
	# 	worker_captain.whip()

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
	print keyword_queue
	process()
