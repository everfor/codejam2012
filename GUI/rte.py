from PyQt4 import QtCore,QtGui
import matplotlib
import pylab
from matplotlibwidget import MatplotlibWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui_rte import Ui_RTEDlg
import numpy as np
import sys
import serial
import threading
import Queue
import _winreg as winreg
import itertools
import re
import time
import os

class MainDisplay(QtGui.QMainWindow):
  def __init__(self,parent=None):
    QtGui.QWidget.__init__(self,parent)
    self.timer = QtCore.QTimer()
    
    self.ui=Ui_RTEDlg()
    self.ui.setupUi(self)
    
    self.mplWidgets=[self.ui.smaMpl, self.ui.lwmaMpl, self.ui.emaMpl, self.ui.tmaMpl]
   
    self.altitudeData=[]
    self.airTempData=[]
    self.descentRateData=[]
    self.voltageData=[]
    self.data=[]
    self.data.append(self.altitudeData)
    self.data.append(self.airTempData)
    self.data.append(self.descentRateData)
    self.data.append(self.voltageData)
    
    self.plot=[]
    
    self._initializePlot()
    self._connectSlots()   
    
    self.ui.disconnectButton.setEnabled(False)
    self.ui.startButton.setEnabled(False)
    self.ui.stopButton.setEnabled(False)

  def _initializePlot(self):
    xlabel='Time (sec.)'
    ylabel='Price'
    title=['Simple Moving Average', 'Linear Weight Moving Average', 'Exponential Moving Average', 'Triangular Moving Average']
    for i in range(len(self.mplWidgets)):
      self.plot.append(self.mplWidgets[i].axes.plot(
        self.data[i], 
        linewidth=1,
        color=(0, 0, 0),
        )[0])
        
      self.mplWidgets[i].axes.set_xlabel(xlabel, size=8)
      self.mplWidgets[i].axes.set_ylabel(ylabel, size=8)  
      self.mplWidgets[i].axes.set_title(title[i], size=8) 
      self.mplWidgets[i].figure.subplots_adjust(bottom=.15)
      self.mplWidgets[i].figure.subplots_adjust(left=.15)
      
  def _drawPlot(self):
    if self.dataExists:
      for i in range(len(self.mplWidgets)):
        xmax = max(self.timeData) if max(self.timeData) > 20 else 20
        xmin = 0

        ymin = round(min(self.data[i]), 0) - 1
        ymax = round(max(self.data[i]), 0) + 1

        self.mplWidgets[i].axes.set_xbound(lower=xmin, upper=xmax)
        self.mplWidgets[i].axes.set_ybound(lower=ymin, upper=ymax)
        
        self.plot[i].set_data(np.array(self.timeData),np.array(self.data[i]))
        
        self.mplWidgets[i].draw()
      
      self._updateLatestData(self.latestLine)

  def _connectSlots(self):
    self.connect(self.ui.connectButton,QtCore.SIGNAL("clicked()"),self._slotConnectClicked)
    self.connect(self.ui.disconnectButton,QtCore.SIGNAL("clicked()"),self._slotDisconnectClicked)
    self.connect(self.ui.startButton,QtCore.SIGNAL("clicked()"),self._slotStartClicked)
    self.connect(self.ui.stopButton,QtCore.SIGNAL("clicked()"),self._slotStopClicked)
    
    self.connect(self.timer, QtCore.SIGNAL('timeout()'), self._drawPlot)

  def _slotConnectClicked(self):
    self.ui.disconnectButton.setEnabled(True)
    self.ui.connectButton.setEnabled(False)
    self.ui.startButton.setEnabled(True)
    self.ui.stopButton.setEnabled(True)
    self.ui.pfEdit.setEnabled(False)
    self.ui.tbEdit.setEnabled(False)
    
  def _slotDisconnectClicked(self):
    self.ui.disconnectButton.setEnabled(False)
    self.ui.connectButton.setEnabled(True)
    self.ui.startButton.setEnabled(False)
    self.ui.stopButton.setEnabled(False)
    self.ui.pfEdit.setEnabled(True)
    self.ui.tbEdit.setEnabled(True)
  
  def _slotStartClicked(self):    
    print 'Start Clicked'
    
  def _slotStopClicked(self):    
    print 'Stop Clicked'

if __name__=="__main__":
  app=QtGui.QApplication(sys.argv)
  rteDlg=MainDisplay()
  rteDlg.show()
  sys.exit(app.exec_())
