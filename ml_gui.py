from PyQt5.QtWidgets import *
import sys , pickle

from PyQt5 import uic , QtWidgets , QtCore, QtGui
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from table_display import DataFrameModel
import matplotlib.pyplot as plt

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('./ui_files/Mainwindow.ui', self)

        self.Browse = self.findChild(QPushButton, 'Browse')
        self.columns = self.findChild(QListWidget, 'column_list')
        self.submit_btn = self.findChild(QPushButton, 'Submit')
        self.cat_column = self.findChild(QComboBox, 'cat_column')
        self.dropcolumns = self.findChild(QComboBox, 'dropcolumn')
        self.empty_columns = self.findChild(QComboBox, 'empty_column')

        self.table = self.findChild(QTableView, 'tableView')
        
        #scatter plot combobox
        self.scatter_x_column = self.findChild(QComboBox, 'scatter_x')
        self.scatter_y_column = self.findChild(QComboBox, 'scatter_y')
        self.scatter_c = self.findChild(QComboBox, 'scatter_c')
        self.scatter_mark = self.findChild(QComboBox, 'scatter_mark')

        #button 
        self.drop_btn = self.findChild(QPushButton, 'Drop')
        self.convert_btn = self.findChild(QPushButton, 'convert_btn')
        self.fill_na_btn = self.findChild(QPushButton, 'fill_na')
        self.fill_mean_btn = self.findChild(QPushButton, 'fillmean')
        self.scatterplot_btn = self.findChild(QPushButton, 'scatterplot')
        # self.textField = self.findChild(QLabel , 'label')

        # self.showTextBtn = self.findChild(QPushButton, 'pushButton_2')
        # self.showField = self.findChild(QLabel , 'label_2')

        # self.tresure = self.findChild(QLabel , 'label_3')

        self.Browse.clicked.connect(self.getCSV)
        self.columns.clicked.connect(self.target)
        self.submit_btn.clicked.connect(self.set_target)
        self.convert_btn.clicked.connect(self.con_cat)
        self.drop_btn.clicked.connect(self.drop_column)

        self.fill_mean_btn.clicked.connect(self.fill_mean)
        self.fill_na_btn.clicked.connect(self.fillna)

        self.scatterplot_btn.clicked.connect(self.scatter_plot)
        self.show()
    
    def scatter_plot(self):
        df=self.df
        x=self.scatter_x_column.currentText()
        y=self.scatter_y_column.currentText()
        c=self.scatter_c.currentText()
        marker=self.scatter_mark.currentText()
        
        plt.figure()
        plt.scatter(df[x],df[y],c=c,marker=marker)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(y + " vs "+ x)
        plt.show()

    def fillna(self):
        a=self.empty_columns.currentText()
        self.df[a].fillna("Unknown",inplace=True)
        self.filldetails()

    def fill_mean(self):
        a=self.empty_columns.currentText()
        self.df[a].fillna(self.df[a].mean(),inplace=True)

        self.filldetails() 

    

    def drop_column(self):
        if (self.dropcolumns.currentText() == self.target_value):
            self.target_value=""
            self.target_col.setText("")
        a=self.dropcolumns.currentText()
        self.df = self.df.drop(a , axis =1)
        self.filldetails()  


    def con_cat(self):
        a=self.cat_column.currentText()
        le = LabelEncoder()
        self.df[a] = le.fit_transform(self.df[a])

        self.filldetails()

    def get_empty_list(self):
        empty_list = []
        for i in self.df.columns:
            if (self.df[i].isnull().values.any() ==True):
                empty_list.append(i)
                
        return empty_list

    def fill_combo_box(self):
        self.cat_column.clear()
        self.cat_column.addItems(self.column_list)
        self.dropcolumns.clear()
        self.dropcolumns.addItems(self.column_list)
        self.empty_columns.clear()
        self.empty_columns.addItems(self.get_empty_list())
        self.scatter_x_column.clear()
        self.scatter_x_column.addItems(self.column_list)
        self.scatter_y_column.clear()
        self.scatter_y_column.addItems(self.column_list)

    def set_target(self):
        self.target_value=str(self.item.text()).split()[0]
        self.target_col.setText(self.target_value)


    def target(self):
        self.item=self.columns.currentItem()
        print(self.item.text().split()[0])
        
    def getCSV(self):
        self.filepath , _ =   QFileDialog.getOpenFileName(self, '파일 열기', '/','csv(*.csv)')
        if self.filepath:
            self.columns.clear()
            self.filldetails(flag=0)
            

    def filldetails(self,flag=1):
         
        if(flag==0):  
            if self.filepath:
                self.df = pd.read_csv(self.filepath)
                
        
        self.column_list = []
        empty_list = []
        for i in self.df.columns:
            
            self.column_list.append(i)
        print(self.column_list)
        # self.columns.insertItems(column_list)
        for i ,j in enumerate(self.column_list):
            stri=j+ " -------   " + str(self.df[j].dtype)
            self.columns.insertItem(i,stri)

        x = DataFrameModel(self.df)
        self.table.setModel(x)

        self.fill_combo_box()
        # print(df.head(3))



    def showText(self):
        self.showField.setText("글씨가 나타났다!")
    
    

    def bingo(self):
        self.showField.setText("100억 당첨!!")

if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()