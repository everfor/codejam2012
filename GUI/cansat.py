from PyQt4 import QtCore,QtGui
import matplotlib
import pylab
from matplotlibwidget import MatplotlibWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui_cansat import Ui_CansatDlg
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

def enumerate_serial_ports():
  path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
  try:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
  except WindowsError:
    return

  for i in itertools.count():
    try:
      val = winreg.EnumValue(key, i)
      yield str(val[1])
    except EnvironmentError:
      break
      
def full_port_name(portname):
  m = re.match('^COM(\d+)$', portname)
  if m and int(m.group(1)) < 10:
    return portname
  return '\\\\.\\' + portname

"""
Decode every two chars into a single char representing those decimal numbers
Ex. 44 ---> ','
"""
  
def decodeDecimalEncodedString(numberString):
  correctedString=''
  for i in range(0,len(numberString),2):
    correctedString=correctedString+chr(int(numberString[i]+numberString[i+1]))
  return correctedString
  
"""
line definition
0 - servo1
1 - servo2
2 - battery voltage
3 - temperature
4 - altitude
5 - Lattitude
6 - N/S
7 - Longitude
8 - E/W
9 - UTC Time
10 - Number of Satellites Locks
11 - Mean Sea Level
12 - Descent Rate

Parse line to presentable format.
"""
def parseLine(line):
  
  #Convert analog value to a voltage value
  line[2]=str(float(line[2])*4.2/1023)
  
  for i in range(5,12):
    line[i]=decodeDecimalEncodedString(line[i])
  
  #if these conversions don't work...don't crash.  
  try:
    lat_raw=float(line[5])
    long_raw=float(line[7])
  except:
    return line
  if line[6]=='S':
    lat_raw=-lat_raw
  if line[8]=='W':
    long_raw=-long_raw
  
  lat_deg=int(lat_raw/100)
  lat_min=lat_raw-lat_deg*100
  
  long_deg=int(long_raw/100)
  long_min=long_raw-long_deg*100
  
  line[5]=str(lat_deg+(lat_min/60))
  line[7]=str(long_deg+(long_min/60))
  
  line[9]=time.strftime('%H:%M:%S', time.strptime(line[9].split('.')[0],'%H%M%S'))+'.'+line[9].split('.')[1]
  
  return line

"""
This class contains all serial read/write functionsina seperate
thread
"""
class DataGetter(threading.Thread):
  def __init__(self,display):
    self.ser=serial.Serial()
    self.display=display
    self.connected=True
    self.firstRun=True
    self.firstLine=True
    self.counter=0
    self.badPacketCounter=0
    self.file=open(os.getcwd()+'\\logs\\'+time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())+'.log'
,'wb')
    threading.Thread.__init__(self)

  def _disconnect(self):
    self.connected=False

  def _setConnection(self,port,baud):
    self.ser.baudrate=baud
    self.ser.port=port
    
  def _sendStart(self):
    self.ser.write("START")
    print "Sent an START packet to " + self.ser.port
    
  def _sendEnd(self):
    self.ser.write("END")
    print "Sent an END packet to " + self.ser.port
    
  def run(self):
    print "Connecting to",self.ser.port,"at",self.ser.baudrate,"baud"
    self.ser.open()
    while self.connected:
      if self.firstRun:
        print self.ser.readline()
        self.firstRun=False
      else:
        line=self.ser.readline().rstrip().split(',')
        if len(line)==13:
          line=parseLine(line)
          
          timeSplit=line[9].split('.')[0].split(':')
          timeEpoch=int(timeSplit[0])*60*60+int(timeSplit[1])*60+int(timeSplit[2])
          timeEpoch=float(str(timeEpoch)+'.'+line[9].split('.')[1])
          
          if self.firstLine:
            self.display.initialTime=timeEpoch
            self.firstLine=False
            
          lineText=','.join(map(str,line))
          print lineText
          self.file.write(lineText+'\n')
          
          for i in range(len(self.display.plotLocation)):
            self.display.data[i].append(float(line[self.display.plotLocation[i]]))
          self.display.timeData.append(timeEpoch-self.display.initialTime)
          self.display.latestLine[:]=line
          self.display.counter=self.display.counter+1
          self.display.dataExists=True
          
        elif line[0]=='START TELEMETRY':
          print 'Starting Telemetry'
          
        elif line[0]=='STANDING BY...':
          print 'Ending Telemetry'
          
        else:
          print 'Bad Packet, Dropped'
          self.badPacketCounter=self.badPacketCounter+1
      
    print '\n' + str(self.badPacketCounter) + ' bad packets'
    print 'Disconnecting'
    
    self.firstRun=True
    self.firstLine=True
    self.file.close()
    self.ser.close()

class MainDisplay(QtGui.QMainWindow):
  def __init__(self,parent=None):
    QtGui.QWidget.__init__(self,parent)
    
    self.timer = QtCore.QTimer()
    
    self.ui=Ui_CansatDlg()
    self.ui.setupUi(self)
    self.thread=DataGetter(self)
    
    self.altitudeData=[]
    self.airTempData=[]
    self.descentRateData=[]
    self.voltageData=[]
    self.data=[]
    self.data.append(self.altitudeData)
    self.data.append(self.airTempData)
    self.data.append(self.descentRateData)
    self.data.append(self.voltageData)
    
    self.timeData=[]
    self.initialTime=0.0
    
    self.mplWidgets=[self.ui.altitudeMpl, self.ui.airTempMpl, self.ui.descentRateMpl, self.ui.voltageMpl]
    
    self.plot=[]
    
    self._initializePlot()
    self._connectSlots()   
    self._fillPortsList()
    
    self.counter=0
    self.plotLocation=[4,3,12,2]
    self.latestLine=[]
    self.dataExists=False

    self.ui.disconnectButton.setEnabled(False)
    self.ui.startButton.setEnabled(False)
    self.ui.stopButton.setEnabled(False)
    
  def _fillPortsList(self):
    for portname in enumerate_serial_ports():
      self.ui.serialPortCombo.addItem(portname)

  def _initializePlot(self):
    xlabel='Time (sec.)'
    ylabel=[r'Altitude ($m.$)', r'Air Temperature ($C^\circ$)', r'Descent Rate ($m/s^2$)', r'Battery Voltage ($V$)'] 
    for i in range(len(self.mplWidgets)):
      self.plot.append(self.mplWidgets[i].axes.plot(
        self.data[i], 
        linewidth=1,
        color=(0, 0, 0),
        )[0])
        
      self.mplWidgets[i].axes.set_xlabel(xlabel, size=8)
      self.mplWidgets[i].axes.set_ylabel(ylabel[i], size=8)  
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
      
  def _updateLatestData(self,line):
    self.ui.timeEdit.setText(line[9])
    self.ui.latitudeEdit.setText(line[5])
    self.ui.longitudeEdit.setText(line[7])
    self.ui.seaAltitudeEdit.setText(line[11])
    self.ui.numSatEdit.setText(line[10])
    self.ui.altitudePressureEdit.setText(line[4])
    self.ui.descentRateEdit.setText(line[12])
    self.ui.airTempEdit.setText(line[3])
    self.ui.voltageEdit.setText(line[2])
    self.ui.servo1Edit.setText(line[0])
    self.ui.servo2Edit.setText(line[1])

  def _connectSlots(self):
    self.connect(self.ui.connectButton,QtCore.SIGNAL("clicked()"),self._slotConnectClicked)
    self.connect(self.ui.disconnectButton,QtCore.SIGNAL("clicked()"),self._slotDisconnectClicked)
    self.connect(self.ui.refreshButton,QtCore.SIGNAL("clicked()"),self._slotRefreshClicked)
    self.connect(self.ui.startButton,QtCore.SIGNAL("clicked()"),self._slotStartClicked)
    self.connect(self.ui.stopButton,QtCore.SIGNAL("clicked()"),self._slotStopClicked)
    
    self.connect(self.timer, QtCore.SIGNAL('timeout()'), self._drawPlot)

  def _slotConnectClicked(self):
    if not str(self.ui.serialPortCombo.currentText()) == '':
      self.ui.disconnectButton.setEnabled(True)
      self.ui.connectButton.setEnabled(False)
      self.ui.startButton.setEnabled(True)
      self.ui.stopButton.setEnabled(True)
      self.ui.refreshButton.setEnabled(False)
      self.ui.serialPortCombo.setEnabled(False)
      self.ui.baudEdit.setEnabled(False)
      
      for i in range(4):
        self.data[i][:]=[]
      
      self.timeData[:]=[]
      
      self.counter=0
      self.dataExists=False
      port=str(self.ui.serialPortCombo.currentText())
      baud=self.ui.baudEdit.text()
      
      self.thread._setConnection(port,baud)
      self.thread.start()
      
      self.timer.start(500)
    else:
      print 'No COM port connected'
    
  def _slotDisconnectClicked(self):
    self.ui.disconnectButton.setEnabled(False)
    self.ui.connectButton.setEnabled(True)
    self.ui.startButton.setEnabled(False)
    self.ui.stopButton.setEnabled(False)
    self.ui.refreshButton.setEnabled(True)
    self.ui.serialPortCombo.setEnabled(True)
    self.ui.baudEdit.setEnabled(True)
    
    self.thread._disconnect()
    
    self.timer.stop()
    
  def _slotRefreshClicked(self):
    self.ui.serialPortCombo.clear()
    self._fillPortsList()
  
  def _slotStartClicked(self):    
    self.thread._sendStart()
    
  def _slotStopClicked(self):    
    self.thread._sendEnd()

if __name__=="__main__":
  app=QtGui.QApplication(sys.argv)
  cansatDlg=MainDisplay()
  cansatDlg.show()
  sys.exit(app.exec_())
