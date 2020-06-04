# -*- coding: utf-8 -*-
import os
import time
import golbal_define as gd
import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtWidgets import QApplication, QLineEdit,QLabel, QTabWidget,QWidget,QTextEdit, QFormLayout, QPushButton, QTableWidget,QTableWidgetItem,QAbstractItemView
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QTabWidget, QTableWidget,QTableWidgetItem
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt,QDate,QTime,QDateTime
from PyQt5.QtGui import QPixmap, QImage
import dijkstra_run as d


today_date = QDate.currentDate()
today_date = today_date.toString(Qt.DefaultLocaleLongDate)
print(today_date)

main_location = '北京'
zoom_ = 12#地图放大 1-17

class Ui_TabWidget(object):

    def setupUi(self, TabWidget):

        #主窗口设置
        TabWidget.setObjectName("网络优化课程报告——基于dijkstra算法的路径规划")          #创建的是"TabWidget"
        TabWidget.setGeometry(gd.big_x,gd.big_y,gd.big_w, gd.big_h+50)
        #self = QtWidgets.QWidget()
        #self.setObjectName("camera")                    #"第一个子窗口"
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(5, 80, 90, 46))
        self.pushButton.setObjectName("pushButton")

        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(5, 500, 90, 46))
        self.pushButton1.setObjectName("pushButton")

        self.pushButton3 = QtWidgets.QPushButton(self)
        self.pushButton3.setGeometry(QtCore.QRect(5, 300, 90, 46))
        self.pushButton3.setObjectName("按A打卡")

        self.pushButton2 = QtWidgets.QPushButton(self)
        self.pushButton2.setGeometry(QtCore.QRect(5, 700, 90, 46))
        self.pushButton2.setObjectName("pushButton")

    
        #日期显示设置
        self.labeldate = QtWidgets.QLabel(self)
        self.labeldate.setGeometry(QtCore.QRect(300, gd.show_y-30, gd.show_w-30, 30))

        #结果显示设置
        self.labelresult = QtWidgets.QLabel(self)
        self.labelresult.setGeometry(QtCore.QRect(100, gd.show_y + gd.show_h+30, gd.show_w, 60))    
        self.labelresult.setAlignment(QtCore.Qt.AlignVCenter)

        #显示设置
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(gd.show_x, gd.show_y, gd.show_w, gd.show_h))
        self.label.setText("")
        self.label.setObjectName("label")

        #TabWidget.addTab(self, "")                      #显示tab

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(TabWidget.tsp_show) #将按键与事件相连

        self.pushButton1.clicked.connect(TabWidget.showdialog) #将按键与事件相连

        self.pushButton2.clicked.connect(TabWidget.quit_system) #将按键与事件相连

        self.pushButton3.clicked.connect(TabWidget.changeMain_location) #将按键与事件相连

        QtCore.QMetaObject.connectSlotsByName(TabWidget)



    def retranslateUi(self, TabWidget):
        global main_location
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "网络优化课程报告——基于dijkstra算法的路径规划"))
        self.pushButton.setText(_translate("TabWidget", "TSP问题"))

        self.pushButton1.setText(_translate("TabWidget", "输入地点"))

        self.pushButton2.setText(_translate("TabWidget", "退出系统"))

        self.pushButton3.setText(_translate("TabWidget", "当前：%s"%main_location))

        TabWidget.setTabText(TabWidget.indexOf(self), _translate("TabWidget", " "))
        # self.pushButton.setCheckable(True) #保持该状态，但可点击
        #self.pushButton3.setEnabled(False)

    #与按钮：登录链接
    def changeMain_location(self):
        global change
        global change_line
        change = QtWidgets.QDialog()
        change.setGeometry(QtCore.QRect(300, 300, 260, 160))
        btn1 = QPushButton("确定", change)
        btn1.move(20, 100)
        btn2 = QPushButton("退出", change)
        btn2.move(140, 100)
        flo = QFormLayout()
        change_line = QLineEdit()
        flo.addRow("城市", change_line)
        change_line.setMaxLength(10)                   

        # 设置显示效果
        change_line.setEchoMode(QLineEdit.Normal)
        change.setLayout(flo)

        btn1.clicked.connect(self.new_city)
        btn2.clicked.connect(change.close)
        change.exec_()

    def new_city(self):
        global change,change_line,main_location
        new_city_changed = change_line.text()
        main_location = new_city_changed
        self.pushButton3.setText( "当前：%s"%main_location)
        change.close()


    #与按钮：登录链接
    def showdialog(self):
        global dialog
        global pNormalLineEdit
        dialog = QtWidgets.QDialog()
        dialog.setGeometry(QtCore.QRect(300, 300, 300, 260))
        btn1 = QPushButton("确定", dialog)
        btn1.move(20, 200)
        btn2 = QPushButton("退出", dialog)
        btn2.move(200, 200)


        self.label_ =  QLabel("输入地点,空格隔开\n例子：天安门 清华大学 颐和园\n",dialog)
        self.label_.move(20,10)


        pNormalLineEdit = QTextEdit(dialog)
        pNormalLineEdit.setPlaceholderText("天安门;清华大学;颐和园")
        pNormalLineEdit.move(20,70)
        pNormalLineEdit.resize(260,100)
        # pNormalLineEdit.setMaxLength(100)
        # # 设置显示效果
        # pNormalLineEdit.setEchoMode(QLineEdit.Normal)

        btn1.clicked.connect(self.input_detect)
        btn2.clicked.connect(dialog.close)
        dialog.exec_()

#用户在该函数下改密码和名字,相关定义见 global_define.py中  修改名字和密码
    def input_detect(self):
        global main_location
        name = pNormalLineEdit.toPlainText()
        places = name.split(' ')

        img,result_p = d.path_planning(places,main_location,zoom_)
        
        dialog.close()

        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                        QImage.Format_RGB888)  
        p = convertToQtFormat.scaled(gd.show_w, gd.show_h, Qt.KeepAspectRatio)
        self.setImage(p)

        re_text = '自驾游玩顺序：\n'
        for p in result_p:
            re_text += str(p)
            re_text += ' 到 '
        re_text = re_text[:-3]
        self.labelresult.setText(re_text)

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))  #label显示
        # #刷新时间
        # time = QTime.currentTime()
        # now_time = time.toString(Qt.DefaultLocaleLongDate)
        # now_time = now_time.split(' ')[1]
        # self.labeldate.setText(today_date+'  '+now_time)

class mywindow(QTabWidget,Ui_TabWidget): #这个窗口继承了用QtDesignner 绘制的窗口
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        
        self.th = QTimer()
        self.th.timeout.connect(self.setDataLabel)          #显示在 Label中
        self.th.start(1000)
        # self.labeldate.setText(today_date)
        # aa = 0
        # kk = 0       				# kk = 1  auto open camera; kk = 0,an jian da kai
        # if kk==1 and aa ==0:
        #     self.videoprocessing() 	        # 启动摄像头线程
        #     kk = 100
        #     aa = 100
        

    #按键：退出的槽函数
    def quit_system(self):
        #sender 是发送信号的对象，此处发送信号的对象是button1按钮 
        sender = self.sender()         
        print( sender.text() + ' 被按下了' ,'退出系统！')  
        self.th.stop()
        qApp = QtWidgets.QApplication.instance()
        qApp.quit()

    def tsp_show(self):
        tsp_re = cv2.imread('Figure_1.png')
        rgbImage = cv2.cvtColor(tsp_re, cv2.COLOR_BGR2RGB)
        show =  cv2.resize(rgbImage,(800,800))
        rgbImage = cv2.resize(rgbImage,(800,540),cv2.INTER_CUBIC)
        show.fill(255)
        show[130:800-130,:] = rgbImage.copy()
        convertToQtFormat = QtGui.QImage(show.data, show.shape[1], show.shape[0],show.shape[1]*3,
                                        QImage.Format_RGB888)  
        p = convertToQtFormat.scaled(gd.show_w, gd.show_h, Qt.KeepAspectRatio)
        self.setImage(p)

        self.labelresult.setText("")

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))  #label显示


    def setDataLabel(self):
        #刷新时间
        time = QTime.currentTime()
        now_time = time.toString(Qt.DefaultLocaleLongDate)
        now_time = now_time.split(' ')[1]
        self.labeldate.setText(today_date+'  '+now_time)

if __name__ == "__main__":
    #启动qt窗口
    appp = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(appp.exec_())

#火车东站 武侯祠 春熙路 金沙博物馆 天府广场 大熊猫繁育研究基地 宽窄巷子
#清华大学 颐和园 圆明园 天安门广场 海淀黄庄
# 清华大学 北京大学 圆明园 颐和园 北京动物园 天安门广场
# 双流国际机场 成都大熊猫繁育研究基地 金沙博物馆 武侯祠 宽窄巷子 春熙路 天府广场
