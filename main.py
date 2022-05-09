import time
import datetime
import sys
import pybithumb
from tkinter import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

tickers = ["BTC", "ETH", "BCH", "ETC"]


def bull_market(ticker):
    btc = pybithumb.get_ohlcv(ticker)
    close = btc['close']
    window = close.rolling(5).mean()
    if window[-1] > pybithumb.get_current_price(ticker):
        return True
    else:
        return False


form_class = uic.loadUiType("cointest2.ui")[0]


class Mywindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        timer = QTimer(self)
        timer.start(1000)#타이머를 설정해서 5초에 한 번씩 timeout 이벤트가 발생하도록 설정합니다.
        timer.timeout.connect(self.timeout)
        #Qtimer 객체에서 timeout이 발생하면 MyWindow 클래스의 timeout() 매서드가 호출되도록 설정합니다.

    def timeout(self):#timeout 이벤트 밸생할 때 실행되는 콜백함수
        for i, ticker in enumerate(tickers):
            item = QTableWidgetItem(ticker)
            print(self.tableWidget.setItem(i, 0, item))

            price, last_ma5, state = self.get_market_infos(ticker)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(last_ma5)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(state))

    def get_market_infos(self, ticker):
        df = pybithumb.get_ohlcv(ticker)
        ma5 = df['close'].rolling(window=5).mean()
        last_ma5 = ma5[-2]
        price = pybithumb.get_current_price(ticker)

        state = None

        if price > last_ma5:
            state = "상승장"
        else:
            state = "하락장"
        return price, last_ma5, state


app = QApplication(sys.argv)
win = Mywindow()
win.show()
app.exec_()
