from datetime import datetime, timedelta
from taoyuan_aerotropolis.connect_mongo import *
from taoyuan_aerotropolis.aerotropolis_scrape import *

earliest = datetime.today() - timedelta(days=1)

if __name__ == "__main__":
	docs = UdnCollecting().collect_udn(earliest)
	insert_document2mongo(docs, "udn")

