__AUTHOR__ = "Master_lxj"
__WEBSITE__ = "http://www.dagouzi.cn"
__DOC__ = "To do something"

import requests
from bs4 import BeautifulSoup

headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


def download(url):
	r = requests.get(url, headers=headers)
	
	return r.content


def parse_html(content):
	phone_list = []
	bs = BeautifulSoup(content, "lxml")
	phones = bs.findAll("div", {"class": "phone_number-text"})
	for phone in phones:
		code = phone.small.em.text
		number = phone.h3.text
		phone_list.append([code, number])
	return phone_list


def spider(page):
	# for i in range(1, 2):
	url = f"https://www.materialtools.com/?page={page}"
	# url = "https://www.materialtools.com/"
	response = download(url)
	return parse_html(response)


def get_sms():
	sms_list = []
	url = "https://www.materialtools.com/SMSContent/1"
	r = requests.get(url, headers=headers)
	bs = BeautifulSoup(r.content, "lxml")
	tables = bs.findAll("table")
	if tables:
		table = tables[-1]
		sms = table.findAll("tr")
		for s in sms[1:]:
			data = s.findAll("td")
			from_num = data[1].text
			text = data[2].text
			sms_time = data[3].time.text
			sms_list.append([from_num, text, sms_time])
	return sms_list
	

# if __name__ == '__main__':
# 	print(spider())
# get_sms()
