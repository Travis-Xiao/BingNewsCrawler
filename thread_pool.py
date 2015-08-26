# from Emilio Monti

from Queue import Queue
from threading import Thread


class Worker(Thread):
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks
		self.deamon = True
		self.start()

	def run(self):
		while True:
			fun, args, kargs = self.tasks.get()
			try:
				fun(*args, **kargs)
			except Exception, e:
				print e

			self.tasks.task_done()


class ThreadPool(object):
	def __init__(self, num_threads):
		self.tasks = Queue(num_threads)
		for _ in range(num_threads):
			Worker(self.tasks)

	def add_task(self, func, *args, **kargs):
		self.tasks.put((func, args, kargs))

	def wait_completion(self):
		self.tasks.join()


if __name__ == '__main__':
	from random import randrange
	delays = [randrange(1, 10) for i in range(20)]

	from time import sleep
	def wait_delay(d):
		print 'sleeping for (%d) sec' % d
		sleep(d)

	pool = ThreadPool(10)

	for i, d in enumerate(delays):
		print "%.2f%c" % ((float(i)/ float(len(delays))) * 100.0, '%')

		pool.add_task(wait_delay, d)

	pool.wait_completion()
	print "completed"