# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/NCPStageMainWindow.ui'
#
# Created: Fri Mar 20 10:42:41 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(816, 552)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.meaNavigationWidget = MEANavigationWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meaNavigationWidget.sizePolicy().hasHeightForWidth())
        self.meaNavigationWidget.setSizePolicy(sizePolicy)
        self.meaNavigationWidget.setObjectName(_fromUtf8("meaNavigationWidget"))
        self.horizontalLayout.addWidget(self.meaNavigationWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.jogRightButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jogRightButton.sizePolicy().hasHeightForWidth())
        self.jogRightButton.setSizePolicy(sizePolicy)
        self.jogRightButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.jogRightButton.setText(_fromUtf8(""))
        self.jogRightButton.setObjectName(_fromUtf8("jogRightButton"))
        self.gridLayout.addWidget(self.jogRightButton, 1, 2, 1, 1)
        self.jogLeftButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jogLeftButton.sizePolicy().hasHeightForWidth())
        self.jogLeftButton.setSizePolicy(sizePolicy)
        self.jogLeftButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.jogLeftButton.setText(_fromUtf8(""))
        self.jogLeftButton.setObjectName(_fromUtf8("jogLeftButton"))
        self.gridLayout.addWidget(self.jogLeftButton, 1, 0, 1, 1)
        self.jogDownButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jogDownButton.sizePolicy().hasHeightForWidth())
        self.jogDownButton.setSizePolicy(sizePolicy)
        self.jogDownButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.jogDownButton.setText(_fromUtf8(""))
        self.jogDownButton.setObjectName(_fromUtf8("jogDownButton"))
        self.gridLayout.addWidget(self.jogDownButton, 2, 1, 1, 1)
        self.jogUpButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jogUpButton.sizePolicy().hasHeightForWidth())
        self.jogUpButton.setSizePolicy(sizePolicy)
        self.jogUpButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.jogUpButton.setText(_fromUtf8(""))
        self.jogUpButton.setObjectName(_fromUtf8("jogUpButton"))
        self.gridLayout.addWidget(self.jogUpButton, 0, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.okLabel = QtGui.QLabel(self.centralwidget)
        self.okLabel.setObjectName(_fromUtf8("okLabel"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.okLabel)
        self.jogSpeedSlider = QtGui.QSlider(self.centralwidget)
        self.jogSpeedSlider.setMinimum(5)
        self.jogSpeedSlider.setMaximum(200)
        self.jogSpeedSlider.setSliderPosition(100)
        self.jogSpeedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.jogSpeedSlider.setObjectName(_fromUtf8("jogSpeedSlider"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.jogSpeedSlider)
        self.verticalLayout.addLayout(self.formLayout_3)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.retractYButton = QtGui.QPushButton(self.centralwidget)
        self.retractYButton.setObjectName(_fromUtf8("retractYButton"))
        self.gridLayout_2.addWidget(self.retractYButton, 4, 1, 1, 1)
        self.zeroButton = QtGui.QPushButton(self.centralwidget)
        self.zeroButton.setObjectName(_fromUtf8("zeroButton"))
        self.gridLayout_2.addWidget(self.zeroButton, 3, 0, 1, 1)
        self.returnYButton = QtGui.QPushButton(self.centralwidget)
        self.returnYButton.setObjectName(_fromUtf8("returnYButton"))
        self.gridLayout_2.addWidget(self.returnYButton, 1, 1, 1, 1)
        self.homeButton = QtGui.QPushButton(self.centralwidget)
        self.homeButton.setObjectName(_fromUtf8("homeButton"))
        self.gridLayout_2.addWidget(self.homeButton, 3, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(-1, 10, -1, -1)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.xLabel = QtGui.QLabel(self.centralwidget)
        self.xLabel.setObjectName(_fromUtf8("xLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.xLabel)
        self.xPosSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.xPosSpinBox.setEnabled(False)
        self.xPosSpinBox.setFrame(True)
        self.xPosSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.xPosSpinBox.setKeyboardTracking(False)
        self.xPosSpinBox.setDecimals(1)
        self.xPosSpinBox.setMinimum(-100000000.0)
        self.xPosSpinBox.setMaximum(100000000.0)
        self.xPosSpinBox.setObjectName(_fromUtf8("xPosSpinBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.xPosSpinBox)
        self.yLabel = QtGui.QLabel(self.centralwidget)
        self.yLabel.setObjectName(_fromUtf8("yLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.yLabel)
        self.yPosSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.yPosSpinBox.setEnabled(False)
        self.yPosSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.yPosSpinBox.setKeyboardTracking(False)
        self.yPosSpinBox.setDecimals(1)
        self.yPosSpinBox.setMinimum(-100000000.0)
        self.yPosSpinBox.setMaximum(100000000.0)
        self.yPosSpinBox.setObjectName(_fromUtf8("yPosSpinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.yPosSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionHome = QtGui.QAction(MainWindow)
        self.actionHome.setObjectName(_fromUtf8("actionHome"))
        self.actionGoToPos = QtGui.QAction(MainWindow)
        self.actionGoToPos.setObjectName(_fromUtf8("actionGoToPos"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Neural Circuit Probe Stage Controller", None))
        self.okLabel.setText(_translate("MainWindow", "Jog Speed", None))
        self.retractYButton.setText(_translate("MainWindow", "Retract", None))
        self.zeroButton.setText(_translate("MainWindow", "Zero", None))
        self.returnYButton.setText(_translate("MainWindow", "Return", None))
        self.homeButton.setText(_translate("MainWindow", "Home", None))
        self.xLabel.setText(_translate("MainWindow", "X", None))
        self.xPosSpinBox.setSuffix(_translate("MainWindow", " um", None))
        self.yLabel.setText(_translate("MainWindow", "Y", None))
        self.yPosSpinBox.setSuffix(_translate("MainWindow", " um", None))
        self.actionHome.setText(_translate("MainWindow", "Home", None))
        self.actionGoToPos.setText(_translate("MainWindow", "Go to...", None))

from ui.widgets import MEANavigationWidget
