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
        self.worker = Worker()  # 스레드를 관리하는 객체생성
        self.worker.finished.connect(self.update_table_widget)
        self.worker.start()  # start가 호출될때 마다 밑에서 정의한 함수가 실행된다.
        # Worker class의 run 메서드가 콜백함수 출력된다.

        timer = QTimer(self)
        timer.start(1000)  # 타이머를 설정해서 5초에 한 번씩 timeout 이벤트가 발생하도록 설정합니다.

    def update_table_widget(self, data):
        try:
            for ticker, infos in data.items():
                index = tickers.index(ticker)
                self.tableWidget.setItem(index, 0, QTableWidgetItem(ticker))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(str(infos[0])))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(str(infos[1])))
                self.tableWidget.setItem(index, 3, QTableWidgetItem(str(infos[2])))

        except:
            pass


class Worker(QThread):
    finished = pyqtSignal(dict)

    # finished 라는 이름으로 사용자 정의 시그녈 이벤트 객체를 생성함

    def run(self):#반드시 이름을 동일하게 적용해서 콜백함수로 적용된다.
        while True:
            data = {}
            for ticker in tickers:
                data[ticker] = self.get_market_infos(ticker)

            print(data)
            self.finished.emit(data)
            self.msleep(500)
            # 사용자가 정의한 시그널 emit하고 data변수가 바인딩하고 있는 딕셔너리 객체가 전송된다.

    def get_market_infos(self, ticker):  # 다른 스레드를 사용하기 위해서 이동함

        try:
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
        except:
            return None, None, None


# 라인 5: 스레드가 실행될 때 수행할 코드를 run() 메서드에 작성합니다. Worker 스레드는 1초에 한 번씩 “안녕하세요” 문자열을 반복 출력합니다.


app = QApplication(sys.argv)
win = Mywindow()
win.show()
app.exec_()

