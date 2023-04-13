from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import cv2
import copy
from Operations import *
import datetime


def resizeToView(img,size = (500,500)):
    org_img =cv2.resize(img,size)
    height, width, channel = org_img.shape
    bytesPerLine = 3 * width
    qImg = QImage(org_img, width, height, bytesPerLine, QImage.Format_BGR888)
    return qImg


class Ui_MainWindow(QWidget):
    tmp_img = None
    org_img = None
    res_img = None
    tmp_file = None

    def browseImage(self):
        self.setEnabled(False)
        fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Image files (*.jpg *.png *.jpeg)")
        self.setEnabled(True)
        if(fname[0]!=''):
            org_img = cv2.imread(fname[0])
            x = fname[0].rindex('/')
            Ui_MainWindow.tmp_file = fname[0][x+1:]
            self.selected_file_label.setText(Ui_MainWindow.tmp_file)
            Ui_MainWindow.tmp_img = copy.deepcopy(org_img)
            self.upload_button.setEnabled(True)
    def save_image(self):
        self.setEnabled(False)
        try:
            res_name = QFileDialog.getSaveFileName(self, f'Save Image',"c:\\Processed Image\\download.jpg","Image Files (*.jpg *png *jpeg)")
            if(res_name[0]!=''):
                cv2.imwrite(res_name[0],Ui_MainWindow.res_img)
                QMessageBox.information(self,"Download Status", "Download Success!!")
        except:
            QMessageBox.critical(self,"Download Status", "Download Failed. Might be due to extension error.")
        self.setEnabled(True)
    def uploadImage(self):
        Ui_MainWindow.org_img = copy.deepcopy(Ui_MainWindow.tmp_img)
        Ui_MainWindow.res_img = copy.deepcopy(Ui_MainWindow.org_img)
        self.reset()
        self.viewOriginal_checkbox.setEnabled(True)
        # self.compress_button.setEnabled(True)
        self.brightness_control.setEnabled(True)
        self.contrast_control.setEnabled(True)
        self.sharpening_control.setEnabled(True)
        self.download_button.setEnabled(True)
        self.blurrness_control.setEnabled(True)
        QMessageBox.information(self,"Upload Status","Upload Success!!")
        self.viewOriginal()
        self.processImage()

    def reset(self):
        Ui_MainWindow.res_img = Ui_MainWindow.org_img
        org_img = resizeToView(Ui_MainWindow.org_img)
        self.resultant_image.setPixmap(QPixmap(org_img))
        self.brightness_control.setValue(0)
        self.contrast_control.setValue(10)
        self.sharpening_control.setValue(0)
        self.blurrness_control.setValue(0)
        pass       
     
    def viewOriginal(self):
        if self.viewOriginal_checkbox.isChecked():
            org_img = resizeToView(Ui_MainWindow.org_img)
            self.original_box.setVisible(True)
            self.original_image.setPixmap(QPixmap(org_img))
        else:
            self.original_box.setVisible(False)

    def processImage(self):
        self.reset_button.setEnabled(True)
        factor = (self.brightness_control.value(),self.contrast_control.value(),self.sharpening_control.value(),self.blurrness_control.value())
        Ui_MainWindow.res_img = color_brightness(Ui_MainWindow.org_img,factor[0]/10)
        Ui_MainWindow.res_img = color_contrast(Ui_MainWindow.res_img,factor[1]/10)
        Ui_MainWindow.res_img = colour_blurring(Ui_MainWindow.res_img,factor[3]*2+1)
        if factor[2]==0:
            Ui_MainWindow.res_img = color_sharpening(Ui_MainWindow.res_img,0)

        else:
            Ui_MainWindow.res_img = color_sharpening(Ui_MainWindow.res_img,1.05**factor[2])
            
        res_img = resizeToView(Ui_MainWindow.res_img)
        self.resultant_image.setPixmap(QPixmap(res_img))
        pass

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(456, 345)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.selected_file_label = QtWidgets.QLabel(self.widget)
        self.selected_file_label.setObjectName("selected_file_label")
        self.horizontalLayout.addWidget(self.selected_file_label)
        self.browse_button = QtWidgets.QPushButton(self.widget)
        self.browse_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.browseImage)
        self.horizontalLayout.addWidget(self.browse_button)
        self.upload_button = QtWidgets.QPushButton(self.widget)
        self.upload_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.upload_button.setObjectName("upload_button")
        self.horizontalLayout.addWidget(self.upload_button)
        spacerItem = QtWidgets.QSpacerItem(201, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.viewOriginal_checkbox = QtWidgets.QCheckBox(self.widget)
        self.viewOriginal_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.viewOriginal_checkbox.setObjectName("viewOriginal_checkbox")
        self.horizontalLayout.addWidget(self.viewOriginal_checkbox)
        self.verticalLayout_2.addWidget(self.widget)
        self.upload_button.setEnabled(False)
        self.viewOriginal_checkbox.setChecked(True)
        self.viewOriginal_checkbox.setEnabled(False)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.original_box = QtWidgets.QGroupBox(self.widget_2)
        self.original_box.setObjectName("original_box")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.original_box)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.original_image = QtWidgets.QLabel(self.original_box)
        self.original_image.setObjectName("original_image")
        self.horizontalLayout_4.addWidget(self.original_image)
        self.horizontalLayout_2.addWidget(self.original_box)
        
        self.resultant_box = QtWidgets.QGroupBox(self.widget_2)
        self.resultant_box.setObjectName("resultant_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.resultant_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_7 = QtWidgets.QWidget(self.resultant_box)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem1 = QtWidgets.QSpacerItem(160, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.resultant_image = QtWidgets.QLabel(self.widget_7)
        self.resultant_image.setObjectName("resultant_image")
        self.horizontalLayout_8.addWidget(self.resultant_image)
        spacerItem2 = QtWidgets.QSpacerItem(160, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.widget_7)
        self.widget_4 = QtWidgets.QWidget(self.resultant_box)
        self.widget_4.setObjectName("widget_4")
        
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.brightness_label = QtWidgets.QLabel(self.widget_4)
        self.brightness_label.setObjectName("brightness_label")
        self.horizontalLayout_5.addWidget(self.brightness_label)
        spacerItem1 = QtWidgets.QSpacerItem(153, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.brightness_control = QtWidgets.QSlider(self.widget_4)
        self.brightness_control.setOrientation(QtCore.Qt.Horizontal)
        self.brightness_control.setObjectName("brightness_control")
        self.horizontalLayout_5.addWidget(self.brightness_control)
        self.verticalLayout.addWidget(self.widget_4)
        
        self.widget_8 = QtWidgets.QWidget(self.resultant_box)
        self.widget_8.setObjectName("widget_8")
        
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.blurrness_label = QtWidgets.QLabel(self.widget_8)
        self.blurrness_label.setObjectName("blurrness_label")
        self.blurrness_label.setText("Blurrness")
        self.horizontalLayout_9.addWidget(self.blurrness_label)
        spacerItem5 = QtWidgets.QSpacerItem(153, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.blurrness_control = QtWidgets.QSlider(self.widget_8)
        self.blurrness_control.setOrientation(QtCore.Qt.Horizontal)
        self.blurrness_control.setObjectName("blurrness_control")
        self.horizontalLayout_9.addWidget(self.blurrness_control)
        self.verticalLayout.addWidget(self.widget_8)
        
        self.widget_5 = QtWidgets.QWidget(self.resultant_box)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.contrast_label = QtWidgets.QLabel(self.widget_5)
        self.contrast_label.setObjectName("contrast_label")
        self.horizontalLayout_6.addWidget(self.contrast_label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.contrast_control = QtWidgets.QSlider(self.widget_5)
        self.contrast_control.setOrientation(QtCore.Qt.Horizontal)
        self.contrast_control.setObjectName("contrast_control")
        self.horizontalLayout_6.addWidget(self.contrast_control)
        self.verticalLayout.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(self.resultant_box)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.sharpening_label = QtWidgets.QLabel(self.widget_6)
        self.sharpening_label.setObjectName("sharpening_label")
        self.horizontalLayout_7.addWidget(self.sharpening_label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.sharpening_control = QtWidgets.QSlider(self.widget_6)
        self.sharpening_control.setOrientation(QtCore.Qt.Horizontal)
        self.sharpening_control.setObjectName("sharpening_control")
        self.horizontalLayout_7.addWidget(self.sharpening_control)
        self.verticalLayout.addWidget(self.widget_6)
        self.horizontalLayout_2.addWidget(self.resultant_box)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.reset_button = QtWidgets.QPushButton(self.widget_3)
        self.reset_button.setObjectName("reset_button")
        self.horizontalLayout_3.addWidget(self.reset_button)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        # self.compress_button = QtWidgets.QPushButton(self.widget_3)
        # self.compress_button.setObjectName("compress_button")
        # self.horizontalLayout_3.addWidget(self.compress_button)
        self.download_button = QtWidgets.QPushButton(self.widget_3)
        self.download_button.setObjectName("download_button")
        self.horizontalLayout_3.addWidget(self.download_button)
        self.verticalLayout_2.addWidget(self.widget_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.download_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        # self.compress_button.setEnabled(False)
        self.upload_button.clicked.connect(self.uploadImage)
        self.brightness_control.setMinimum(-10)
        self.brightness_control.setMaximum(10)
        self.brightness_control.setSingleStep(1)
        self.brightness_control.valueChanged.connect(self.processImage)
        self.blurrness_control.setMinimum(0)
        self.blurrness_control.setMaximum(49)
        self.blurrness_control.setSingleStep(1)
        self.blurrness_control.valueChanged.connect(self.processImage)
        self.contrast_control.setMinimum(0)
        self.contrast_control.setMaximum(20)
        self.contrast_control.setValue(10)
        self.contrast_control.setSingleStep(1)
        self.contrast_control.valueChanged.connect(self.processImage)
        self.sharpening_control.setMinimum(0)
        self.sharpening_control.setMaximum(100)
        self.sharpening_control.setValue(0)
        self.sharpening_control.setSingleStep(1)
        self.sharpening_control.valueChanged.connect(self.processImage)
        self.brightness_control.setEnabled(False)
        self.contrast_control.setEnabled(False)
        self.sharpening_control.setEnabled(False)
        self.blurrness_control.setEnabled(False)
        self.reset_button.clicked.connect(self.reset)
        self.download_button.clicked.connect(self.save_image)
        # self.compress_button.setEnabled(False)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Processing Tool"))
        self.selected_file_label.setText(_translate("MainWindow", "No File Selected"))
        self.browse_button.setToolTip(_translate("MainWindow", "Click to select image"))
        self.browse_button.setText(_translate("MainWindow", "Browse"))
        self.upload_button.setToolTip(_translate("MainWindow", "Upload Image"))
        self.upload_button.setText(_translate("MainWindow", "Upload"))
        self.viewOriginal_checkbox.setToolTip(_translate("MainWindow", "Click to view original image"))
        self.viewOriginal_checkbox.setText(_translate("MainWindow", "View Original"))
        self.viewOriginal_checkbox.stateChanged.connect(self.viewOriginal)
        self.original_box.setTitle(_translate("MainWindow", "Original"))
        self.original_image.setText(_translate("MainWindow", "No Image Selected"))
        self.resultant_box.setTitle(_translate("MainWindow", "Result"))
        self.resultant_image.setText(_translate("MainWindow", "No Image Selected"))
        self.brightness_label.setText(_translate("MainWindow", "Brightness"))
        self.contrast_label.setText(_translate("MainWindow", "Contrast"))
        self.sharpening_label.setText(_translate("MainWindow", "Sharpening"))
        self.reset_button.setText(_translate("MainWindow", "Reset"))
        # self.compress_button.setText(_translate("MainWindow", "Compress && Download"))
        self.download_button.setText(_translate("MainWindow", "Download"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setStyle("Fusion")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())