#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Ryan Flynn
Advanced Computer Science
Madaket the Personal Assistant
March 2018
v3.1
"""

from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, 
    QInputDialog, QApplication, QLabel, QGridLayout)
from PyQt5.QtCore import Qt
import sys, Knowledge

class Gui(QWidget):
    
    def __init__(self):
        super().__init__()
        self._question = "M: How can I help you?"
        self.out_text = self._question + '\n'
        self.initUI()
        
        
    def initUI(self):      
        # Output label and textbox
        self.out_label = QLabel('Madaket')
        self.out = QTextEdit(self)
        self.out.setReadOnly(True)
        self.out.setText(self.out_text)
        
        # Input label and textbox
        self.in_label = QLabel('You')
        self.inp = QTextEdit(self)

        # Submit Button
        self.submit = QPushButton('Submit',self)
        QPushButton.setDefault(self.submit, True)
        self.submit.clicked.connect(self.display)
        # print(self.submit.isDefault())

        # Grid
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 4)
        self.grid.setRowStretch(1, 5)
        self.grid.setRowStretch(2,2)

        # Grid Placement
        self.grid.addWidget(self.out_label, 1, 0)
        self.grid.addWidget(self.out, 1, 1)
        self.grid.addWidget(self.in_label, 2, 0)
        self.grid.addWidget(self.inp, 2, 1)
        self.grid.addWidget(self.submit, 3, 0)

        self.setLayout(self.grid)
        
        # Window
        self.setGeometry(500, 500, 500, 485)
        self.setWindowTitle('Madaket')
        self.show()
        
    def _format(self, answer, query):
        # Formats output and updates the text log which is returned
        # general format: Madaket offers assistance, User asks question, Madaket offers assistance, repeat
        new = 'Y: ' + query + '\n' + 'M: ' + answer + '\n'
        self.out_text += new + self._question + '\n'
        return self.out_text
    
    def display(self):
        # get current display text
        txt = self.inp.toPlainText()

        # Calculate and <<format>> output
        output = self.output(txt)
        # print(output)
        self.out.setText(self._format(output, txt))
        self.inp.setText('')
        

    def keyPressEvent(self, event):
        # Default button is submit. Engage default if return key is pressed
        if event.key() == Qt.Key_Return:
            # print("detected")
            self.submit.click()

    def output(self, query):
        # Knowledge engine call to get output text
        return Knowledge.ask(query)
    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())
