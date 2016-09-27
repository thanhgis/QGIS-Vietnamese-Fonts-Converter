# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\THANHNV\.qgis2\python\plugins\Converter\vn_fonts_dialog_base.ui'
#
# Created: Sat Sep 03 16:30:44 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ConverterDialogBase(object):
    def setupUi(self, ConverterDialogBase):
        ConverterDialogBase.setObjectName(_fromUtf8("ConverterDialogBase"))
        ConverterDialogBase.resize(508, 281)
        self.gridLayout = QtGui.QGridLayout(ConverterDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ConverterDialogBase)
        self.label.setMaximumSize(QtCore.QSize(250, 35))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(ConverterDialogBase)
        self.label_3.setMaximumSize(QtCore.QSize(300, 35))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.input_layer = QtGui.QComboBox(ConverterDialogBase)
        self.input_layer.setMinimumSize(QtCore.QSize(0, 35))
        self.input_layer.setMaximumSize(QtCore.QSize(16777215, 35))
        self.input_layer.setObjectName(_fromUtf8("input_layer"))
        self.gridLayout.addWidget(self.input_layer, 1, 0, 1, 2)
        self.output_select_Button = QtGui.QPushButton(ConverterDialogBase)
        self.output_select_Button.setMaximumSize(QtCore.QSize(150, 35))
        self.output_select_Button.setObjectName(_fromUtf8("output_select_Button"))
        self.gridLayout.addWidget(self.output_select_Button, 3, 2, 1, 1)
        self.button_box = QtGui.QDialogButtonBox(ConverterDialogBase)
        self.button_box.setMaximumSize(QtCore.QSize(16777215, 35))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.gridLayout.addWidget(self.button_box, 7, 1, 1, 2)
        self.label_4 = QtGui.QLabel(ConverterDialogBase)
        self.label_4.setMaximumSize(QtCore.QSize(290, 35))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.output_layer = QtGui.QLineEdit(ConverterDialogBase)
        self.output_layer.setMaximumSize(QtCore.QSize(16777215, 35))
        self.output_layer.setObjectName(_fromUtf8("output_layer"))
        self.gridLayout.addWidget(self.output_layer, 3, 0, 1, 2)
        self.type_Box = QtGui.QComboBox(ConverterDialogBase)
        self.type_Box.setMinimumSize(QtCore.QSize(0, 35))
        self.type_Box.setMaximumSize(QtCore.QSize(16777215, 35))
        self.type_Box.setObjectName(_fromUtf8("type_Box"))
        self.type_Box.addItem(_fromUtf8(""))
        self.type_Box.addItem(_fromUtf8(""))
        self.type_Box.addItem(_fromUtf8(""))
        self.type_Box.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.type_Box, 5, 0, 1, 2)

        self.retranslateUi(ConverterDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), ConverterDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), ConverterDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ConverterDialogBase)

    def retranslateUi(self, ConverterDialogBase):
        ConverterDialogBase.setWindowTitle(_translate("ConverterDialogBase", u"Chuyển đổi mã font chữ tiếng Việt", None))
        self.label.setText(_translate("ConverterDialogBase", "Chọn lớp vector đầu vào:", None))
        self.label_3.setText(_translate("ConverterDialogBase", "Chọn thư mục và tên lớp đầu ra:", None))
        self.output_select_Button.setText(_translate("ConverterDialogBase", "...", None))
        self.label_4.setText(_translate("ConverterDialogBase", "Chọn mã nguồn >> mã đích:", None))
        self.type_Box.setItemText(0, _translate("ConverterDialogBase", "TCVN (ABC) >> Unicode", None))
        self.type_Box.setItemText(1, _translate("ConverterDialogBase", "Unicode >> TCVN (ABC)", None))
        self.type_Box.setItemText(2, _translate("ConverterDialogBase", "TCVN (ABC) >> Khong dau", None))
        self.type_Box.setItemText(3, _translate("ConverterDialogBase", "Unicode >> Khong dau", None))

