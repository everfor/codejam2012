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
import TradeAndFeedback

class MainDisplay(QtGui.QMainWindow):
    def __init__(self,parent=None):

        QtGui.QWidget.__init__(self,parent)


        self.ui=Ui_RTEDlg()
        self.ui.setupUi(self)

        
        self.priceData=[]
        self.timeData=[]

        self.pf = PriceFeed.PriceFeed()
        self.tf = TradeAndFeedback.TradeAndFeedback()

        self.smaPlot=self._initializePlot()
        self._connectSlots()
        self.ui.disconnectButton.setEnabled(False)
        self.ui.startButton.setEnabled(False)
        self.ui.sendButton.setEnabled(False)


    def _connectSlots(self):
        self.connect(self.ui.connectButton,QtCore.SIGNAL("clicked()"),self._slotConnectClicked)
        self.connect(self.ui.disconnectButton,QtCore.SIGNAL("clicked()"),self._slotDisconnectClicked)
        self.connect(self.ui.startButton,QtCore.SIGNAL("clicked()"),self._slotStartClicked)
        self.connect(self.ui.sendButton,QtCore.SIGNAL("clicked()"),self._slotSendClicked)

    def _slotConnectClicked(self):
        self.ui.disconnectButton.setEnabled(False)
        self.ui.connectButton.setEnabled(False)
        self.ui.startButton.setEnabled(True)
        self.ui.pfEdit.setEnabled(False)
        self.ui.tbEdit.setEnabled(False)
        self.ui.ipEdit.setEnabled(False)

        self.ip=str(self.ui.ipEdit.text())
        self.port1=int(str(self.ui.pfEdit.text()))
        self.port2=int(str(self.ui.tbEdit.text()))
        self.pf.connect(self.ip,self.port1)
        self.tf.connect(self.ip,self.port2)

    def _slotDisconnectClicked(self):
        self.ui.disconnectButton.setEnabled(False)
        self.ui.connectButton.setEnabled(True)
        self.ui.startButton.setEnabled(False)
        self.ui.pfEdit.setEnabled(True)
        self.ui.tbEdit.setEnabled(True)
        
    def _slotSendClicked(self):
        self.write()

    def _initializePlot(self):
        xlabel='Time (sec.)'
        ylabel='Price'
        title=['Simple Moving Average','Linear Weighted Moving Average','Exponential Moving Average','Triangular Moving Average']
        plot=self.ui.smaMpl.axes.plot(
            np.array(self.timeData),
            np.array(self.priceData),
            linewidth=1,
            color='blue',
            )[0]
        
        self.ui.smaMpl.axes.set_xlabel(xlabel, size=8)
        self.ui.smaMpl.axes.set_ylabel(ylabel, size=8)  
        self.ui.smaMpl.axes.set_title(title[0], size=8)  
        self.ui.smaMpl.figure.subplots_adjust(bottom=.15)
        self.ui.smaMpl.figure.subplots_adjust(left=.15)
        
        return plot
        
    def _slotStartClicked(self):
        self.ui.startButton.setEnabled(False)
        t = threading.Thread(target = self.run())
        t.start()
        t.join(10)

    def run(self):
        price_time = 0
        data=''
        self.pf.startFeed()
        while(1):
            price_time, data = self.pf.getNextPrice()
            if("" == data):
                self.ui.sendButton.setEnabled(True)
                break
            self.priceData.append(float(data))
            self.timeData.append(price_time)
            if(price_time % 100 == 0):
                t_plot = threading.Thread(target = self._drawPlot())
                t_update = threading.Thread(target = self.tf.update_all(data, price_time))
                t_update.start()
                t_plot.start()
                t_plot.join()
                t_update.join()
                QtGui.QApplication.processEvents()
            else:
                self.tf.update_all(data, price_time)
        
    def write(self):
        self.tf.json_write()
    
    def _drawPlot(self):
        xmax = round(max(self.timeData), 0) + 1
        xmin = round(min(self.timeData), 0) - 1

        ymin = 5
        ymax = round(max(self.priceData), 0) + 1

        self.ui.smaMpl.axes.set_xbound(lower=xmin, upper=xmax)
        self.ui.smaMpl.axes.set_ybound(lower=ymin, upper=ymax)

        self.smaPlot.set_data(np.array(self.timeData),np.array(self.priceData))

        self.ui.smaMpl.draw()
        return

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    rteDlg=MainDisplay()
    rteDlg.show()
    sys.exit(app.exec_())
