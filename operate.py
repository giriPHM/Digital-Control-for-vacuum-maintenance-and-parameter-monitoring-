import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import *
import serial
import decimal

ser=serial.Serial('/dev/ttyS0', 115200, timeout=5)

'''(
    QApplication, QDialog, QMainWindow, QMessageBox, QLabel, QPushButton, QVBoxLayout, QWidget
) '''
#from PyQt6.QtCore import QProcess
#from PyQt6.uic import loadUi

from Py_ras import Ui_MainWindow
class Worker(QObject):
    finished= pyqtSignal()
    progress= pyqtSignal()
    def run(self):
      while True:
          time.sleep(1)
          self.progress.emit()
      self.finished.emit()

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.state=0
        self.turb=1
        
    def connectSignalsSlots(self):
        val="TRUE"
        self.pushButton_3.setEnabled(False)
        #print(self.pushButton.isEnabled())
        #self.pushButton_2.setEnabled(False)
        #self.pushButton_3.setEnabled(False)
        self.pushButton_5.clicked.connect(self.runLoop)
        self.pushButton.clicked.connect(self.roughing_pump_on)
        self.pushButton_2.clicked.connect(self.roughing_pump_off)
        self.pushButton_3.clicked.connect(self.TURBO_PUMP_ON)
        self.pushButton_4.clicked.connect(self.TURBO_PUMP_OFF)
       # self.dateTimeEdit.dateTimeChanged.connect(self.update)



        self.progressBar.setValue(0)
        #self.pushButton_2.clicked.connect(self.test)

        #self.pushButton.setEnabled(False)
        
    def roughing_pump_on(self):
        print("ROUGHING_PUMP_ON")

    def roughing_pump_off(self):
        print("ROUGHING_PUMP_OFF")
        self.pushButton_3.setEnabled(False)
        self.turb=0

    def TURBO_PUMP_ON(self):
        print("TURBO_PUMP_ON")
        self.turb=1
        self.state=1

    def TURBO_PUMP_OFF(self):
        print("TURBO_PUMP_OFF")
        self.state=0


    def display_realtime_data(self):
        k="ON"
        #print(n)
        #v=str(n)
        if self.state==1 and self.pushButton_3.isEnabled():
            self.pushButton_2.setEnabled(False)
        else:
            self.pushButton_2.setEnabled(True)
        data=(ser.read(8))
        temperature=str(data, 'UTF-8')
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.textBrowser.append("Oxygen_level ===="+ " "+temperature)
        self.textBrowser_2.append("Pressure ===="+ " "+temperature)
        self.textBrowser_3.append("Roughing Pump is ON")
        if decimal.Decimal(temperature)>=7 and self.turb!=0: 
            self.pushButton_3.setEnabled(True)
            self.progressBar.setValue(decimal.Decimal(temperature))
    def runLoop(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.display_realtime_data)
        self.thread.start()

        #Final resets
        self.pushButton_5.setEnabled(False)
        #self.pushButton_3.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.pushButton_5.setEnabled(True)
        )
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
