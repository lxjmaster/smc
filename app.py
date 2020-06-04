__AUTHOR__ = "Master_lxj"
__WEBSITE__ = "http://www.dagouzi.cn"
__DOC__ = "To do something"


from PyQt5 import QtWidgets
from main import Ui_Form
import sys
import random
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
	url = "https://www.materialtools.com/?page={}".format(page)
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


class MainWindow(QtWidgets.QMainWindow, Ui_Form):
	
	def __init__(self):
		
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.init_phone_table()
		self.pushButton.clicked.connect(self.sms_table)
		self.pushButton_2.clicked.connect(self.init_phone_table)

	def init_phone_table(self):
		
		self.statusBar().showMessage("正在刷新号码....")
		phones = spider(random.randint(1, 13))
		row_count = self.tableWidget.rowCount()
		for row, phone in enumerate(phones):
			if not row_count:
				self.tableWidget.insertRow(row)
			self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(phone[0]))
			self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(phone[1]))
			row += 1
		self.statusBar().showMessage("号码刷新完成....")
	
	def sms_table(self):
		
		self.statusBar().showMessage("正在刷新短信....")
		sms = get_sms()
		row_count = self.tableWidget_2.rowCount()
		for row, s in enumerate(sms):
			if not row_count:
				self.tableWidget_2.insertRow(row)
			self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(s[-1]))
			self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(s[1]))
			row += 1
		self.statusBar().showMessage("短信刷新完成....")
	

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
