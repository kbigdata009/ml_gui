from PyQt5.QtWidgets import *
import sys , pickle

from PyQt5 import uic , QtWidgets , QtCore, QtGui
import pandas as pd


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('./ui_files/Mainwindow.ui', self)

        self.Browse = self.findChild(QPushButton, 'Browse')
        self.columns = self.findChild(QListWidget, 'column_list')
        # self.textField = self.findChild(QLabel , 'label')

        # self.showTextBtn = self.findChild(QPushButton, 'pushButton_2')
        # self.showField = self.findChild(QLabel , 'label_2')

        # self.tresure = self.findChild(QLabel , 'label_3')

        self.Browse.clicked.connect(self.getCSV)
        # self.showTextBtn.clicked.connect(self.showText)
        self.show()

    def getCSV(self):
        self.filepath , _ =   QFileDialog.getOpenFileName(self, '파일 열기', '/','csv(*.csv)')
        self.df = pd.read_csv(self.filepath)
        self.columns.clear()
        column_list = []
        for i in self.df.columns:
            column_list.append(i)
        # print(column_list)
        for i , j in enumerate(column_list):
            stri = f'{j} ------ {self.df[j].dtype}'
            self.columns.insertItem(i, stri)
            print(stri)


        # print(df.head(3))



    def showText(self):
        self.showField.setText("글씨가 나타났다!")
    
    

    def bingo(self):
        self.showField.setText("100억 당첨!!")

if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()