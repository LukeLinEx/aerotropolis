#coding:utf-8

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from taoyuan_aerotropolis.helpers import *


class TYCGCollecting(object):
    def __init__(self):
        pass

    @staticmethod
    def get_interested_content(content_url):
        content_soup = BeautifulSoup(requests.get(content_url).text)
        paras = content_soup.find_all("p")

        if interested_words_exist(paras):
            return "<br><br>".join([str(p) for p in paras])

    def collect_interested_news(self, start_date):
        url = "http://www.tycg.gov.tw/ch/home.jsp?intpage=&id=9&parentpath=0%2C1&qptdate={start_date}&showedate=&qdldate=&keyword=請輸入關鍵字&page=1&pagesize=311".format(
            start_date = str(start_date.date())
        )

        soup = BeautifulSoup(requests.get(url).text)
        lst = soup.find_all("tr", {"class": "list"})
        collection = []

        for item in lst:
            date_released = item.find("td", {"class":"post_date"}).text
            date_released = str2date(date_released)
            title = item.find("a", {"class":"list_a"}).get("title")

            content_url = url + "&" + item.find("a", {"class":"list_a"}).get("href")
            content = self.get_interested_content(content_url)
            if content:
                collection.append({
                    "title": title, "date_released": date_released, "url":content_url, "content": content
                })

        return collection


class UdnCollecting(object):
    def __init__(self):
        self.url = "https://udn.com/search/result/2/桃園航空城"
    
    @staticmethod
    def collect_meta(result):
        title = result.h2.text
        url_content = result.a.get("href")
        txt = result.span.text
        r = re.search("(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$", txt)
        date_released = datetime.strptime(r.group(), "%Y/%m/%d")

        return {
            "title": title, "url": url_content,
            "date_released": date_released
        }

    @staticmethod
    def get_content(content_url):
        content_txt = requests.get(content_url).text
        content_soup = BeautifulSoup(content_txt)
        lst = content_soup.find_all("p")
        content = "\n".join(map(lambda x: x.text, lst))

        return content
    
    @staticmethod
    def collect_one_page_udn(url, earliest=None):
        txt = requests.get(url).text
        soup = BeautifulSoup(txt)

        one_page = []
        for result in soup.find_all("dt"):
            if result.find("img"):
                try:
                    news = UdnCollecting.collect_meta(result)
                    content = UdnCollecting.get_content(news["url"])
                    news["content"] = content
                    if earliest and news["date_released"] < earliest:
                        break
                    one_page.append(news)
                except AttributeError:
                    break

        return one_page
    
    def collect_udn(self, earliest):
        url = self.url
        all_udn = []

        i = 1
        while True:
            tmp = UdnCollecting.collect_one_page_udn(url+"/"+str(i), earliest)
            all_udn.extend(tmp)
            if len(tmp)==0 or list(filter(lambda x: x["date_released"]<earliest, tmp)):
                break
            i+=1
            
        return sorted(all_udn, key=lambda doc: doc["date_released"])


if __name__ == "__main__":
	earliest = datetime(2018,1,30)
	TYCGCollecting().collect_interested_news(earliest)

