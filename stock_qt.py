from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
import datetime
import sys  # We need sys so that we can pass argv to QApplication
import os
import time
from yahoo_fin import stock_info as si
import decimal


def float_range(start, stop, step):
    """Get range obj by float"""
    while start < stop:
        yield float(start)
        start += decimal.Decimal(step)


def get_sp500():
    """Get S&P500 current price and current time"""
    sp500 = si.get_live_price("^GSPC")
    sp500_trim = "%.2f" % sp500

    _time = datetime.datetime.now().timetuple()
    _time = time.mktime(tuple(_time))
    _time_label = f"test"

    return float(sp500_trim), int(_time)


class MainWindow(QtWidgets.QMainWindow):
    """Main application window for display and init graphing.
    User update_plot_data to live update this window"""
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # instantiate widget window
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # set graph background and line color
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(0, 0, 0), width=2)


        # try to modify the init range of table according to price day high low
        self.x = list(range(100))
        price, xx = get_sp500()
        price_range = float_range(int(price)-1, int(price)+1, .02) 
        self.y = list(price_range)

        # draw init line on widget
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        # set title
        self.graphWidget.setTitle("S&P500 Live Price",color=(0,0,255),size='30')  # use rgb for color

        # set axis label
        self.graphWidget.setLabel('left', 'Price (USD)', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Time (s)', color='red', size=30)

        # show grid in graph
        self.graphWidget.showGrid(x=True, y=True)

        # run self.update_plot_data to update main widget
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)  # ms
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        """Update plot realtime"""
        sp500, _time = get_sp500()
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + _time)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first 
        old_price = self.y[-1]
        self.y.append(sp500)  # Add new sp500 price
        # set label in graph
        self.data_line.setData(self.x, self.y)  # Update the data.
        if sp500 > old_price:
            self.graphWidget.setLabel('top', f'sp500: {self.y[-1]}', color='forestgreen')
        elif sp500 == old_price:
            self.graphWidget.setLabel('top', f'sp500: {self.y[-1]}', color='orange')
        else:
            self.graphWidget.setLabel('top', f'sp500: {self.y[-1]}', color='red')

def main():
    """Start app instance with proper exit"""
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()