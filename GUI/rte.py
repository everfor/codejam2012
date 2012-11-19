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
        self.smaFast=[]
        self.lwmaFast=[]
        self.emaFast=[]
        self.tmaFast=[]
        self.smaSlow=[]
        self.lwmaSlow=[]
        self.emaSlow=[]
        self.tmaSlow=[]

        
        self.mplWidgets=[self.ui.smaMpl, self.ui.lwmaMpl, self.ui.emaMpl, self.ui.tmaMpl]
        self.plot=[]
        self._initializePlot()
        


        self.pf = PriceFeed.PriceFeed()
        self.tf = TradeAndFeedback.TradeAndFeedback()
        
        
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
        os.system("""imview Gant_Chart.jpg&""")
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
        title=['Simple Moving Average', 'Linear Weight Moving Average', 'Exponential Moving Average', 'Triangular Moving Average']
        for i in range(len(self.mplWidgets)):
            self.mplWidgets[i].axes.set_xlabel(xlabel, size=8)
            self.mplWidgets[i].axes.set_ylabel(ylabel, size=8)
            self.mplWidgets[i].axes.set_title(title[i], size=8)
            self.mplWidgets[i].figure.subplots_adjust(bottom=.15)
            self.mplWidgets[i].figure.subplots_adjust(left=.15)
            self.plot.append(self.mplWidgets[i].axes.plot(
                self.timeData,
                self.priceData,
                linewidth=1,
                color='blue',
                )[0])
        for i in range(len(self.mplWidgets)):
            if(i == 0):
                self.plot.append(self.mplWidgets[i].axes.plot(
                    self.timeData,
                    self.smaFast,
                    linewidth=1,
                    color='green',
                    )[0])
                self.plot.append(self.mplWidgets[i].axes.plot(
                    self.timeData,
                    self.smaSlow,
                    linewidth=1,
                    color='red',
                    )[0])
            if(i == 1):
                self.plot.append(self.mplWidgets[i].axes.plot(
                    self.timeData,
                    self.lwmaFast,
                    linewidth=1,
                    color='green',
                    )[0])
                self.plot.append(self.mplWidgets[i].axes.plot(
                    self.timeData,
                    self.lwmaSlow,
                    linewidth=1,
                    color='red',
                    )[0])
            if(i == 2):
                self.plot.append(self.mplWidgets[i].axes.plot(
                    self.timeData,
                    self.emaFast,
                    linewidth=1,
                    color='green',
                    )[0])
                self.plot.append(self.mplWidgets[i].axes.plot(
                    self.timeData,
                    self.emaSlow,
                    linewidth=1,
                    color='red',
                    )[0])
            if(i == 3):
                self.plot.append(self.mplWidgets[i].axes.plot(
                    self.timeData,
                    self.tmaFast,
                    linewidth=1,
                    color='green',
                    )[0])
                self.plot.append(self.mplWidgets[i].axes.plot(
                    self.timeData,
                    self.tmaSlow,
                    linewidth=1,
                    color='red',
                    )[0])
        return
        
    def _slotStartClicked(self):
        self.ui.startButton.setEnabled(False)
        t = threading.Thread(target = self.run())
        t.start()
        t.join(100)

    def run(self):
        price_time = 0
        data=''
        self.pf.startFeed()
        while(1):
            price_time, data = self.pf.getNextPrice()
            if("" == data):
                self.ui.sendButton.setEnabled(True)
                break
            self.tf.update_all(data, price_time)
            self.priceData.append(float(data))
            self.timeData.append(price_time)
            self.smaFast.append(self.tf.all_strategy.SMA_fast.showValue())
            self.lwmaFast.append(self.tf.all_strategy.LWMA_fast.showValue())
            self.emaFast.append(self.tf.all_strategy.EMA_fast.showValue())
            self.tmaFast.append(self.tf.all_strategy.TMA_fast.showValue())
            self.smaSlow.append(self.tf.all_strategy.SMA_slow.showValue())
            self.lwmaSlow.append(self.tf.all_strategy.LWMA_slow.showValue())
            self.emaSlow.append(self.tf.all_strategy.EMA_slow.showValue())
            self.tmaSlow.append(self.tf.all_strategy.TMA_slow.showValue())
            if(price_time % 20 == 0):
                self._drawPlot(price_time, self.timeData, self.priceData, self.smaFast, self.lwmaFast, self.emaFast, 
                                self.tmaFast, self.smaSlow, self.lwmaSlow,
                                self.emaSlow, self.tmaSlow)
                QtGui.QApplication.processEvents()
            if(price_time % 100 == 0):
                self.priceData=self.priceData[100:]
                self.timeData=self.timeData[100:]
                self.smaFast=self.smaFast[100:]
                self.lwmaFast=self.lwmaFast[100:]
                self.emaFast=self.emaFast[100:]
                self.tmaFast=self.tmaFast[100:]
                self.smaSlow=self.smaSlow[100:]
                self.lwmaSlow=self.lwmaSlow[100:]
                self.emaSlow=self.emaSlow[100:]
                self.tmaSlow=self.tmaSlow[100:]   
            
                
        self.tf.json_write()
        self.tf.history()
        os.system("notepad history.txt")

    def write(self):
        self.tf.post()
        self.ui.serialLabel.setText(self.tf.cere)
    
    def _drawPlot(self, price_time, timeData, priceData, smaFast, lwmaFast, emaFast, 
                                tmaFast, smaSlow, lwmaSlow,
                                emaSlow, tmaSlow):
        for i in range(len(self.mplWidgets)):
            xmax = round(max(timeData), 0) - 1
            xmin = round(min(timeData), 0) + 1
            
            mean = sum(priceData)/len(priceData)
            ymin = mean * 0.95
            if(ymin > round(min(priceData), 0)):
                ymin = round(min(priceData), 0)
            ymax = mean * 1.05
            if(ymax < round(max(priceData), 0)):
                ymax = round(max(priceData), 0)
            
            self.mplWidgets[i].axes.set_xbound(lower=xmin, upper=xmax)
            self.mplWidgets[i].axes.set_ybound(lower=ymin, upper=ymax)
            

            self.plot[i].set_data(np.array(timeData),np.array(priceData))
            if(i == 0):
                self.plot[2*i + 4].set_data(np.array(timeData),np.array(smaFast))
                self.plot[2*i + 5].set_data(np.array(timeData),np.array(smaSlow))
            if(i == 1):
                self.plot[2*i + 4].set_data(np.array(timeData),np.array(lwmaFast))
                self.plot[2*i + 5].set_data(np.array(timeData),np.array(lwmaSlow))
            if(i == 2):
                self.plot[2*i + 4].set_data(np.array(timeData),np.array(emaFast))
                self.plot[2*i + 5].set_data(np.array(timeData),np.array(emaSlow))
            if(i == 3):
                self.plot[2*i + 4].set_data(np.array(timeData),np.array(tmaFast))
                self.plot[2*i + 5].set_data(np.array(timeData),np.array(tmaSlow))
                
            self.mplWidgets[i].axes.add_line(self.plot[i])
            self.mplWidgets[i].axes.add_line(self.plot[2*i + 4])
            self.mplWidgets[i].draw()
        return
        

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    rteDlg=MainDisplay()
    rteDlg.show()
    sys.exit(app.exec_())
