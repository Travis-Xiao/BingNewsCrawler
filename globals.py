import hashlib
import threading
import worker
import re
import string
import thread_pool

# url to search news
bing_news_base = "http://www.bing.com/news/search?q="
# url to get current trends
bing_hint_request_url = "http://api.bing.com/qsonhs.aspx?" \
	"FORM=ASAPIW&mkt=en-US&type=cb&cb=sa_inst.apiCB&cp=0&q=&o=l+a+hc+p"

bing_hint_request_params = {
	"FORM": "ASAPIW",
	"mkt": "en-US",
	"type": "cb",
	"cb": "sa_inst.apiCB",
	"cp": "0",
	"q": "",
	"o": "l a hc p"
}
m = hashlib.md5()

output_dir = "./Output/"

keyword_queue = set()

# store hashcode of title
covered_keyword = set()
# link_list = []
lock = threading.Lock()

# worker_captain = worker.WorkerCaptain()
pool = thread_pool.ThreadPool(10)

regex = re.compile('[%s]+' % re.escape(string.punctuation))

max_search_thread = 10
max_crawler = 10