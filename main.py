# -*- coding: utf-8 -*-
"""
process monitoring and power-off
"""

import os

import psutil

from gui import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.process = str()
        self.cancel = bool()
        self.ui.listWidget.addItems(self.get_process_list())  # Show Process list in listWidget
        self.ui.pushButton.clicked.connect(self.check_radio_buttons)  # Start Monitoring Process
        self.ui.listWidget.itemClicked.connect(self.add_process)  # Add Clicked Process Name to var: process
        self.ui.pushButton_2.clicked.connect(self.stop)  # Start Monitoring Process
        self.ui.pushButton_3.clicked.connect(self.refresh)

    def get_process_list(self):
        process_list = set()
        processes = psutil.process_iter()
        for process in processes:
            process_list.add(process.name().lower())
        clean_process_list = sorted(list(process_list))

        return clean_process_list

    def add_process(self, item):
        self.ui.label_3.setText(str(item.text()))

    def stop(self):
        self.cancel = True

    def refresh(self):
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.get_process_list())  # Show Process list in listWidget

    def check_process(self):
        process_count = 0
        for proc in psutil.process_iter():
            if proc.name().lower() == self.ui.label_3.text():
                process_count += 1
        return process_count

    def start_monitoring(self, command):
        self.cancel = False
        while self.cancel is False:
            QtCore.QCoreApplication.processEvents()
            if self.check_process() == 0:
                os.system(command)
                sys.exit(app.exec_())

    def check_radio_buttons(self):
        if self.ui.radioButton.isChecked():  # Sleep/Hibernation
            self.start_monitoring("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        if self.ui.radioButton_2.isChecked():  # Power Off
            self.start_monitoring("Shutdown.exe -s -t 00")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

# pyuic5.exe -x "C:\Users\boris\Documents\PycharmProjects\PMPO\pmpo.ui" -o gui.py
# pyinstaller -F -w -i "ico\main.ico" --name "PMPO" main.py
