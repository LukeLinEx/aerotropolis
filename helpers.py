#coding:utf-8

import re
from datetime import datetime

words_interested = ["航空城", "桃機", "桃捷", "機捷", "機場捷運", "工程", "通車", "交通", "運輸", "重劃", "青埔"]


def roc2gregorian(year):
    if isinstance(year, str):
        year = str(int(year)+1911)
    else:
        year = str(year + 1911)

    return year


def str2date(date_str):
    date_str = date_str.replace("/", "-").split("-")
    date_str[0] = roc2gregorian(date_str[0])
    return datetime.strptime("-".join(date_str).strip(), "%Y-%m-%d")


#  def interested_words_exist(paras):
#     for p in paras:
#         for w in words_interested:
#             if re.search(w, p.text):
#                 return True
#
#     return False


def interested_words_exist(paras):
    for w in words_interested:
        if re.search(w, paras):
            return True

    return False
