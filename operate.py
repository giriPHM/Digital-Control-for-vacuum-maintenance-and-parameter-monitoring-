import sys
import time

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.uic import *
'''(
    QApplication, QDialog, QMainWindow, QMessageBox, QLabel, QPushButton, QVBoxLayout, QWidget
) '''
#from PyQt6.QtCore import QProcess
#from PyQt6.uic import loadUi
#Just a comment

from final_version_2 import Ui_MainWindow
class Worker(QObject):
    finished= pyqtSignal()
    progress= pyqtSignal(int)
    def run(self):
      for i in range(107):
          time.sleep(1)
          self.progress.emit(i)
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
        self.pushButton.setEnabled(False)
        #print(self.pushButton.isEnabled())
        #self.pushButton_2.setEnabled(False)
        #self.pushButton_3.setEnabled(False)
        self.pushButton_5.clicked.connect(self.runLoop)
        self.pushButton_3.clicked.connect(self.roughing_pump_on)
        self.pushButton_4.clicked.connect(self.roughing_pump_off)
        self.pushButton.clicked.connect(self.TURBO_PUMP_ON)
        self.pushButton_2.clicked.connect(self.TURBO_PUMP_OFF)
        self.dateTimeEdit.dateTimeChanged.connect(self.update)



        self.progressBar.setValue(0)
        #self.pushButton_2.clicked.connect(self.test)

        #self.pushButton.setEnabled(False)
        
    def roughing_pump_on(self):
        print("ROUGHING_PUMP_ON")

    def roughing_pump_off(self):
        print("ROUGHING_PUMP_OFF")
        self.pushButton.setEnabled(False)
        self.turb=0

    def TURBO_PUMP_ON(self):
        print("TURBO_PUMP_ON")
        self.state=0

    def TURBO_PUMP_OFF(self):
        print("TURBO_PUMP_OFF")
        self.state=1


    def display_realtime_data(self, n):
        k="ON"
        #print(n)
        #v=str(n)
        if self.state==0 and self.pushButton.isEnabled():
            self.pushButton_4.setEnabled(False)
        else:
            self.pushButton_4.setEnabled(True)

        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.textBrowser.append("Oxygen_level ===="+ " "+str(n))
        self.textBrowser_2.append("Pressure ===="+ " "+str(n))
        self.textBrowser_3.append("Roughing Pump is ON")
        if n>=7 and self.turb==1: #k=="ON":
            self.pushButton.setEnabled(True)
            self.progressBar.setValue(n-7)
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
