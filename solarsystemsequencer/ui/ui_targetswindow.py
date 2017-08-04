# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'targetswindow.ui'
#
# Created: Sun Feb 12 19:58:20 2017
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(503, 300)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.schedule_date_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.schedule_date_label.sizePolicy().hasHeightForWidth())
        self.schedule_date_label.setSizePolicy(sizePolicy)
        self.schedule_date_label.setObjectName("schedule_date_label")
        self.horizontalLayout.addWidget(self.schedule_date_label)
        self.schedule_dateedit = QtWidgets.QDateEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.schedule_dateedit.sizePolicy().hasHeightForWidth())
        self.schedule_dateedit.setSizePolicy(sizePolicy)
        self.schedule_dateedit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.schedule_dateedit.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.schedule_dateedit.setCalendarPopup(False)
        self.schedule_dateedit.setCurrentSectionIndex(2)
        self.schedule_dateedit.setObjectName("schedule_dateedit")
        self.horizontalLayout.addWidget(self.schedule_dateedit)
        self.today_btn = QtWidgets.QPushButton(Dialog)
        self.today_btn.setObjectName("today_btn")
        self.horizontalLayout.addWidget(self.today_btn)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Solar System Sequencer - Targets"))
        self.schedule_date_label.setText(_translate("Dialog", "Date"))
        self.schedule_dateedit.setDisplayFormat(_translate("Dialog", "yyyy/MM/dd"))
        self.today_btn.setText(_translate("Dialog", "Today"))

