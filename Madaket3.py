#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we receive data from
a QInputDialog dialog. 

Aauthor: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, 
    QInputDialog, QApplication, QLabel, QGridLayout)
from PyQt5.QtCore import Qt
import sys, Knowledge

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      
        #Output label and textbox
        self.out_label = QLabel('Madaket')
        self.out = QTextEdit(self)
        self.out.setReadOnly(True)
        
        #Input label and textbox
        self.in_label = QLabel('You')
        self.inp = QTextEdit(self)

        #Submit Button
        self.submit = QPushButton('Submit',self)
        QPushButton.setDefault(self.submit, True)
        self.submit.clicked.connect(self.display)
        print(self.submit.isDefault())

        #Grid
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 4)
        self.grid.setRowStretch(1, 5)
        self.grid.setRowStretch(2,2)

        #Grid Placement
        self.grid.addWidget(self.out_label, 1, 0)
        self.grid.addWidget(self.out, 1, 1)
        self.grid.addWidget(self.in_label, 2, 0)
        self.grid.addWidget(self.inp, 2, 1)
        self.grid.addWidget(self.submit, 3, 0)

        self.setLayout(self.grid)
        
        #Window
        self.setGeometry(500, 500, 500, 485)
        self.setWindowTitle('Madaket')
        self.show()
        
        
    def display(self):
        txt = self.inp.toPlainText()
        output = self.output(txt)
        print(output)
        self.out.setText(output)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            print("detected")
            self.submit.click()

    def output(self, query):
        print(Knowledge.ask(query))
        return Knowledge.ask(query)
        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
