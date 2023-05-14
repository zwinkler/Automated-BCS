#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyrealsense2 as rs
import cv2
import numpy as np
import matplotlib.pyplot as plt
import logging
import glob
import imageio
import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import time


# In[2]:


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
#         pipeline.start(config)
        while self._run_flag:
            frames = pipeline.wait_for_frames()
            global color_image
            global depth_image
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            cv_img = color_image
            #if ret:
            self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        pipeline.stop()
        

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


# In[3]:


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Capture Window")
        self.disply_width = 1280
        self.display_height = 720
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        
        
        self.textbox = QLineEdit(placeholderText="Cow BCS")
#         textboxValue = self.textbox.text()
#         print(textboxValue)
        vbox.addWidget(self.textbox)
    
        self.textbox2 = QLineEdit(placeholderText="Cow Breed")
#         textboxValue = self.textbox.text()
#         print(textboxValue)
        vbox.addWidget(self.textbox2)
        
        capture_button = QPushButton('Capture Image')
        capture_button.clicked.connect(self.capture_image)
        vbox.addWidget(capture_button)
        
        
        
    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def capture_image(self):
        BCS = self.textbox.text()
        breed = self.textbox2.text()
#         try:
#             os.mkdir('Images')
#         except FileExistsError:
#             pass
#         try:
#             os.mkdir('Images/RGB')
#         except FileExistsError:
#             pass
#         try:
#             os.mkdir('Images/depth')
#         except FileExistsError:
#             pass

        files = sorted(glob.glob('Images/RGB/'+BCS+'_'+breed+'/*'))
        max_num = 0
        for i in range(len(files)):
            temp = int(files[i][len('Images/RGB/2_'+breed+'/'):-len('.tiff')])
            if temp > max_num:
                max_num = temp
    
#         max_num = 0
#         for i in range(len(folders)):
#             temp = int(folders[i][len('Images/RGB/'+BCS):])
#             if temp > max_num:
#                 max_num = temp
        
        
        
        
#         os.mkdir('Images/image_'+str(max_num+1))
    
#         imageio.imwrite('Images/image_'+str(max_num+1)+'/image_'+str(max_num+1)+'_color.tiff', color_image)
#         imageio.imwrite('Images/image_'+str(max_num+1)+'/image_'+str(max_num+1)+'_depth.tiff', depth_image)
    
    
#         BCS = self.textbox.text()
        try:
            os.mkdir('Images/RGB/'+BCS+'_'+breed)
        except FileExistsError:
            pass
        
        try:
            os.mkdir('Images/depth/'+BCS+'_'+breed)
        except FileExistsError:
            pass
        
        imageio.imwrite('Images/RGB/'+BCS+'_'+breed+'/'+str(max_num+1)+'.tiff', color_image)
        imageio.imwrite('Images/depth/'+BCS+'_'+breed+'/'+str(max_num+1)+'.tiff', depth_image)

#         BCS_file = open('Images/image_'+str(max_num+1)+'/image_'+str(max_num+1)+'_score.txt', 'w')
#         BCS_file.write(BCS)
#         BCS_file.close()
        self.textbox.setText("")


# In[4]:


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.any, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720)
#config.enable_stream(rs.stream.infrared, 1280, 720)
pipeline.start(config)


try:
    os.mkdir('Images')
except FileExistsError:
    pass
try:
    os.mkdir('Images/RGB')
except FileExistsError:
    pass
try:
    os.mkdir('Images/depth')
except FileExistsError:
    pass



# for i in range(1,10):
#     try:
#         os.mkdir('Images/RGB/'+str(i))
#     except FileExistsError:
#         pass

# for i in range(1,10):
#     try:
#         os.mkdir('Images/depth/'+str(i))
#     except FileExistsError:
#         pass

        
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())

