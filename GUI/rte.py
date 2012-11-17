from ImportDirectoryList import * #import all used directories
from PyQt4 import QtCore,QtGui
import matplotlib
import pylab
from matplotlibwidget import MatplotlibWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import animation
from matplotlib import pyplot as plt
from ui_rte import Ui_RTEDlg
import numpy as np
import sys
import time
import os
import threading


import PriceFeed
import Strategy

class MainDisplay(QtGui.QMainWindow):
    def __init__(self,parent=None):
        self.all_strategy = Strategy.Strategy()

        QtGui.QWidget.__init__(self,parent)
        self.timer = QtCore.QTimer()

        self.ui=Ui_RTEDlg()
        self.ui.setupUi(self)
        
        self.smaData=[]

        self.pf = PriceFeed.PriceFeed()

        self.smaPlot=self._initializePlot()
        self._connectSlots()
        self.ui.disconnectButton.setEnabled(False)
        self.ui.startButton.setEnabled(False)

    def _connectSlots(self):
        self.connect(self.ui.connectButton,QtCore.SIGNAL("clicked()"),self._slotConnectClicked)
        self.connect(self.ui.disconnectButton,QtCore.SIGNAL("clicked()"),self._slotDisconnectClicked)
        self.connect(self.ui.startButton,QtCore.SIGNAL("clicked()"),self._slotStartClicked)

    def _slotConnectClicked(self):
        self.ui.disconnectButton.setEnabled(True)
        self.ui.connectButton.setEnabled(False)
        self.ui.startButton.setEnabled(True)
        self.ui.pfEdit.setEnabled(False)
        self.ui.tbEdit.setEnabled(False)

        self.ip=str(self.ui.ipEdit.text())
        self.port=int(str(self.ui.pfEdit.text()))
        self.pf.connect(self.ip,self.port)

    def _slotDisconnectClicked(self):
        self.ui.disconnectButton.setEnabled(False)
        self.ui.connectButton.setEnabled(True)
        self.ui.startButton.setEnabled(False)
        self.ui.pfEdit.setEnabled(True)
        self.ui.tbEdit.setEnabled(True)

    def _initializePlot(self):
        xlabel='Time (sec.)'
        ylabel='Price'
        title=['Simple Moving Average','Linear Weighted Moving Average','Exponential Moving Average','Triangular Moving Average']
        plot=self.ui.smaMpl.axes.plot(
            self.smaData, 
            linewidth=1,
            color=(0, 0, 0),
            )[0]
        
        self.ui.smaMpl.axes.set_xlabel(xlabel, size=8)
        self.ui.smaMpl.axes.set_ylabel(ylabel, size=8)  
        self.ui.smaMpl.axes.set_title(title[0], size=8)  
        self.ui.smaMpl.figure.subplots_adjust(bottom=.15)
        self.ui.smaMpl.figure.subplots_adjust(left=.15)
        
        return plot
        
    def _slotStartClicked(self):
        price_time = 0
        data=''
        initial = time.time()
        self.pf.startFeed()
        while(1):
            price_time, data = self.pf.getNextPrice()
            self.smaData.append(float(data))
            if(len(self.smaData)==10000):
                self._drawPlot()
                self.smaData=[]
            '''self.timeData.append(price_time)
            self.data.append(float(data))
            if(price_time % 1000 == 0):
                self._drawPlot(self.timeData, self.data)
                self.timeData = []
                self.data = []
            '''
            if(data == 'C'):
                print data
                break
            self.all_strategy.update(float(data), price_time)
        print time.time() - initial
    
    def _drawPlot(self):
        xmax = 10000
        xmin = 0

        ymin = round(min(self.smaData), 0) - 1
        ymax = round(max(self.smaData), 0) + 1

        self.ui.smaMpl.axes.set_xbound(lower=xmin, upper=xmax)
        self.ui.smaMpl.axes.set_ybound(lower=ymin, upper=ymax)

        self.smaPlot.set_data(np.linspace(0,9999,10000),np.array(self.smaData))

        self.ui.smaMpl.draw()

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    rteDlg=MainDisplay()
    rteDlg.show()
    sys.exit(app.exec_())
