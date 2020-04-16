from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # set graph background and line color
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))

        # set x and y values
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # set x and y axis range
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

        # set title
        self.graphWidget.setTitle("S&P500 Live Price",color=(0,0,255),size='30')  # use rgb for color

        # set axis label
        self.graphWidget.setLabel('left', 'Temperature (°C)', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Hour (H)', color='red', size=30)

        # show grid in graph
        self.graphWidget.showGrid(x=True, y=True)

        # self.graphWidget.plot(hour, temperature, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first 
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()