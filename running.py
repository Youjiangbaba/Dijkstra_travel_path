# -*- coding: utf-8 -*-
#from __future__ import division
import golbal_define as gd
import sys, time ,os
import numpy as np

# from flask import Flask,render_template,Response
import thread#python2 为thread  #---------------------------------------------------------

from PyQt5 import QtCore, QtGui, QtWidgets

from windows import Ui_TabWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QTabWidget, QMessageBox, QTableWidget,QTableWidgetItem
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt,QDate,QTime,QDateTime
from PyQt5.QtGui import QPixmap, QImage


#人脸识别类 - 使用face_recognition模块
import cv2
import face_recognition

from PIL import Image,ImageDraw,ImageFont
# from hardware import HardWare
#utf8
reload(sys)             #---------------------------------------------------------
sys.setdefaultencoding('utf8')

today_date = QDate.currentDate()
today_date = today_date.toString(Qt.DefaultLocaleLongDate)
print(today_date)




class mywindow(QTabWidget,Ui_TabWidget): #这个窗口继承了用QtDesignner 绘制的窗口
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        
        self.labeldate.setText(today_date)
        aa = 0
        kk = 0       				# kk = 1  auto open camera; kk = 0,an jian da kai
        if kk==1 and aa ==0:
            self.videoprocessing() 	        # 启动摄像头线程
            kk = 100
            aa = 100
        

    #按键：退出的槽函数
    def quit_system(self):
        #sender 是发送信号的对象，此处发送信号的对象是button1按钮 
        sender = self.sender()         
        print( sender.text() + ' 被按下了' ,'退出系统！')  
        qApp = QtWidgets.QApplication.instance()
        qApp.quit()

    #按键：开启打卡的槽函数
    def videoprocessing(self):
        global push_key
        push_key = 100
        print("open camera")				#定义线程
        th = Thread(self)			 	#开启显示进程	
        th.changePixmap.connect(self.setImage)          #显示在 Label中
        th.start()					#开启显示进程
        self.pushButton.setEnabled(False)
        self.pushButton3.setEnabled(True)

    #按键：按A打卡的槽函数
    def pushButtonA(self):
        global start_reconition
        start_reconition = 1 
        print('开始打卡！')

    #键盘响应，按键A
    def keyPressEvent(self, QKeyEvent):  # 键盘某个键被按下时调用
        global start_reconition,push_key
        if push_key == 0:
            self.videoprocessing()
        #参数1  控件
        elif QKeyEvent.key()== Qt.Key_A:  #判断是否按下了A键
            #key()  是普通键
            start_reconition = 1 
            print('开始打卡！')
        elif QKeyEvent.key()== Qt.Key_Q:
            qApp = QtWidgets.QApplication.instance()
            qApp.quit()
            print ('Q被按下，退出系统！')



    def setImage(self, image):
        global now_time
        self.label.setPixmap(QPixmap.fromImage(image))  #label显示
        #刷新时间
        time = QTime.currentTime()
        now_time = time.toString(Qt.DefaultLocaleLongDate)
        now_time = now_time.split(' ')[1]
        self.labeldate.setText(today_date+'  '+now_time)
            


class Thread(QThread):#采用线程来播放视频

    global minH, minW, font,cap,total_face_encoding,total_image_name,faceCascade
    changePixmap = pyqtSignal(QtGui.QImage)

    #线程主函数
    def run(self,falg_function=0):
        global the_num,names
        global  start_reconition
        global none_save                            #定义没有识别到的序号，最后保存的文件名
        none_save = 0
        if_dist = 1				      #默认没有人走过来
        
        count_0 = 0
        cap = cv2.VideoCapture(0)
        last_value = -1
        value = 100

        # iniciate id counter
        the_num = -1#识别的第几个人,且＝－100时作为即将重复打卡的flag
        last_num = -1#上一个人

        push_key = 0#按键第二次后变为100，按键开启系统功能
        now_time = ' 2019'

        #face_recognition
        load_time = time.time()
        path = "img/face_recognition"  # 模型数据图片目录  face_recognition face_test
        total_image_name = []
        total_face_encoding = []
        for fn in os.listdir(path):  #fn 表示的是文件名q
            print(path + "/" + fn)
            img = cv2.imread(path + "/" + fn)
            location_face = [[0,img.shape[1],img.shape[0],0]]
            total_face_encoding.append(
                face_recognition.face_encodings(
                    face_recognition.load_image_file(path + "/" + fn),location_face)[0])
            fn = fn[:(len(fn) - 4)]  #截取图片名（这里应该把images文件中的图片名命名为为人物名）
            total_image_name.append(fn)  #图片名字列表


        print ("read completed!,took ",'%.3f' %(time.time()-load_time),'s.')

        #按键改变参数，1为识别
        start_reconition = 0

        # 名字工号列表，分别对应 1 ，2 ，3 ...;原文件名为 yj_1009
        names = []
        numbers = []
        for fn in total_image_name:
            _name = fn.split("_")[0]
            _number = fn.split("_")[1]
            names.append(_name)
            numbers.append(_number)
        print (names,numbers)
   #pdb.set_trace()  # start debug
        while 1:
            
            # value = HardWare.if_distance()
            if value == 1 and last_value == 0:
                #print ('开始----------------------------------------',value)
                start_reconition = 1
            last_value = value
            
            
            ret,img = cap.read()
            flag = self.face_detect_recognition2(img,start_reconition) #-1 unknown; 1 ok
            #print "3:",the_num
            if flag == 0:
                count_0 += 1
                if count_0 >= 10:#多次没识别到人，关闭识别
                    start_reconition = 0
                    count_0 = 0
                
            elif flag == -1:#unknown
                start_reconition = 0
                time.sleep(0.5)

		    #识别到用户
            else:
                time.sleep(0.5)
                start_reconition = 0

    #opencv的人脸检测
    def detect_byOpencv(self,img):
        start_detect_time = time.time()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        loctions = []
        #  rect to css
        for (x,y,w,h) in faces:
            top = y
            right = x + w
            bottom = y + h
            left = x
            loctions.append((top, right, bottom, left))   
        print ("opencv detect:",time.time()-start_detect_time)
        return loctions


    #识别  
    def face_detect_recognition2(self,fff,if_recognition):
        global now_time,last_num,the_num,names,ok_img,err_img

        frame= cv2.resize(fff,(320,240))
        if_open = 0 #三种状态，０未找到脸，继续找；１识别成功；－１检测到了脸，但是陌生的
        if_this_recog_ok = 0
        
        #########################################################
        #增加识别人脸开启
        # kkkkk = time.time()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces = faceCascade.detectMultiScale(gray, 1.5, 5)
        # print (time.time() - kkkkk)
        #if len(faces) >= 1:
        #    if the_num != -100:
        #        if_recognition = 1
            
        #########################################################
        
        took_d_time = 0
        took_r_time = 0
        if 1: #开启检测
            took_d_time = time.time()
            #face_locations = self.detect_byOpencv(frame)    #利用opencv人脸检测代替其检测，检测速度提高了一倍
            face_locations = face_recognition.face_locations(frame)
            print ('detect1 time:','{:.3f}'.format(time.time() - took_d_time),'s')
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            print ('detect time:','{:.3f}'.format(time.time() - took_d_time),'s')
            print (face_locations)

            # 在这个视频帧中循环遍历每个人脸
            for (top, right, bottom, left), face_encoding in zip(
                    face_locations, face_encodings):
                # 画出一个框，框住脸
                cv2.rectangle(fff, (2*left, 2*top), (2*right, 2*bottom), (0, 0, 255), 2)
                fff[2*top+10:2*bottom-10,2*left+10:2*right-10].fill(180)
                if 1:
                #if if_recognition == 1:
                    # 看看面部是否与已知人脸相匹配。
                    took_r_time = time.time()
                    for i, v in enumerate(total_face_encoding):
                        match = face_recognition.compare_faces([v], face_encoding, tolerance=0.5)#0.5
                        name = "Unknown"
                        
                        print ('-----------',match)
                        if match[0]:
                            name = names[i]
                            # 画出一个带名字的标签，放在框下
                            #print (right-left)
                            the_num = i
                            #print "1:",the_num
                            if_open = 1
                            if_this_recog_ok = 1

                            break
                        else:
                            if i == len(total_face_encoding)-1:
                                if if_open != 1:
                                    if_open = -1


                    if if_this_recog_ok == 1:# and last_num != the_num:#如果这张脸识别成功且没有重复

                        if_this_recog_ok = 0
                        aa = int(35*((right-left)/130.0))
                        bb = int((right-left)/6.0)
                        cc = int(6*((right-left)/130.0))
                        print (aa,bb,cc)
                        cv2.rectangle(fff, (2*left, 2*(bottom - aa)), (2*right, 2*bottom), (0, 0, 255),cv2.FILLED)
                        cv2.putText(fff, numbers[i], (2*(left + bb), 2*(bottom - cc)), cv2.FONT_HERSHEY_SIMPLEX, 1.0,(255, 255, 255), 2)
                        fff[10:60,210:430] = ok_img.copy()
                    
                    elif last_num == the_num:
                        the_num = -100#不再开启
                    else:#识别失败
                        cv2.rectangle(fff, (2*left, 2*(bottom - int(35*((right-left)/130.0)))), (2*right, 2*bottom), (0, 0, 255),cv2.FILLED)
                        cv2.putText(fff, name, (2*left, 2*(bottom - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(255, 255, 255), 2)
                        fff[10:60,210:430] = err_img.copy()
                        #报警程序
                        # ...


        rgbImage = cv2.cvtColor(fff, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                        QImage.Format_RGB888)  
        p = convertToQtFormat.scaled(gd.show_w, gd.show_h, Qt.KeepAspectRatio)
        self.changePixmap.emit(p)
        return if_open

if __name__ == '__main__':

    ok_img = cv2.imread('通过.png')
    ok_img = cv2.resize(ok_img,(220,50))

    err_img = cv2.imread('报警.png')
    err_img = cv2.resize(err_img,(220,50))

    cap = 0
    kk = 0
    print('wait for load...')
    cascadePath = "haarcascade_frontalface_alt.xml"      # 下载人脸检测器
    print('load completed')
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = ImageFont.truetype("./font/FZXBSJW.TTF", 30, encoding="utf-8") # simsun.ttc FZXBSJW.TTF
    
    # iniciate id counter
    the_num = -1#识别的第几个人,且＝－100时作为即将重复打卡的flag
    last_num = -1#上一个人

    push_key = 0#按键第二次后变为100，按键开启系统功能
    now_time = ' 2019'

    #face_recognition
    load_time = time.time()
    path = "img/face_recognition"  # 模型数据图片目录  face_recognition face_test
    total_image_name = []
    total_face_encoding = []
    for fn in os.listdir(path):  #fn 表示的是文件名q
        print(path + "/" + fn)
        img = cv2.imread(path + "/" + fn)
        location_face = [[0,img.shape[1],img.shape[0],0]]
        total_face_encoding.append(
            face_recognition.face_encodings(
                face_recognition.load_image_file(path + "/" + fn),location_face)[0])
        fn = fn[:(len(fn) - 4)]  #截取图片名（这里应该把images文件中的图片名命名为为人物名）
        total_image_name.append(fn)  #图片名字列表


    print ("read completed!,took ",'%.3f' %(time.time()-load_time),'s.')

    #按键改变参数，1为识别
    start_reconition = 0

    # 名字工号列表，分别对应 1 ，2 ，3 ...;原文件名为 yj_1009
    names = []
    numbers = []
    for fn in total_image_name:
        _name = fn.split("_")[0]
        _number = fn.split("_")[1]
        names.append(_name)
        numbers.append(_number)
    print (names,numbers)


    # 定义被识别的最小窗口
    minW = 0.05 * 640
    minH = 0.05 * 480

    
    #启动qt窗口
    appp = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    
    # thread.start_new_thread(start_run,())
    #app.run(host='0.0.0.0',port = 9000)
    sys.exit(appp.exec_())
    cap.release()
    print('over')

