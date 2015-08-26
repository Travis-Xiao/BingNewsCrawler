# from threading import Thread
import threading
from time import sleep
import re
import string

lock = threading.Lock()


def function01(arg,name):
	# for i in range(arg):
	#     # print(name,'i---->',i,'\n')
	#     # print (name,"arg---->",arg,'\n')
	#     sleep(1)
	global lock
	lock.acquire()
	print name
	sleep(3)
	lock.release()
	return name


def test01():
	thread1 = threading.Thread(target = function01, args = (10,'thread1', ))
	thread1.start()
	thread2 = threading.Thread(target = function01, args = (10,'thread2', ))
	thread2.start()
	print thread1.join()
	print thread2.join()
	print ("thread finished...exiting")

# test01()

# import globals
#
# globals.covered_keyword.add("asdfsadf")
#
# print globals.covered_keyword
#
# new_set = set("asfad")
# # globals.covered_keyword = globals.covered_keyword.union(new_set)
# globals.covered_keyword.intersection(new_set)
#
# print globals.covered_keyword
#
# print set("agf asdf ag sd".split(' '))
#
# d = []
# d.append("asgfag")
# print d

# s = "http://blog.cnfol.com/i6rapple8/article/30612564.html"
# regex = re.compile('[%s]+' % re.escape(string.punctuation))
# s = regex.sub('_', s)
# print s

