# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'schedulebrain.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                            QRect, QSize, QUrl, Qt, QDateTime, QDate, QTime)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

import res_rc

class Ui_ScheduleBrainDialog(object):
    def setupUi(self, ScheduleBrainDialog):
        if ScheduleBrainDialog.objectName():
            ScheduleBrainDialog.setObjectName(u"ScheduleBrainDialog")
        ScheduleBrainDialog.resize(409, 263)
        self.gridLayout = QGridLayout(ScheduleBrainDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonbox = QDialogButtonBox(ScheduleBrainDialog)
        self.buttonbox.setObjectName(u"buttonbox")
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonbox, 2, 1, 1, 1)

        self.targets_groupbox = QGroupBox(ScheduleBrainDialog)
        self.targets_groupbox.setObjectName(u"targets_groupbox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targets_groupbox.sizePolicy().hasHeightForWidth())
        self.targets_groupbox.setSizePolicy(sizePolicy)
        self.formLayout_2 = QFormLayout(self.targets_groupbox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.mercury_checkbox = QCheckBox(self.targets_groupbox)
        self.targets_buttongroup = QButtonGroup(ScheduleBrainDialog)
        self.targets_buttongroup.setObjectName(u"targets_buttongroup")
        self.targets_buttongroup.setExclusive(False)
        self.targets_buttongroup.addButton(self.mercury_checkbox)
        self.mercury_checkbox.setObjectName(u"mercury_checkbox")
        self.mercury_checkbox.setChecked(True)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.mercury_checkbox)

        self.venus_checkbox = QCheckBox(self.targets_groupbox)
        self.targets_buttongroup.addButton(self.venus_checkbox)
        self.venus_checkbox.setObjectName(u"venus_checkbox")
        self.venus_checkbox.setChecked(True)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.venus_checkbox)

        self.mars_checkbox = QCheckBox(self.targets_groupbox)
        self.targets_buttongroup.addButton(self.mars_checkbox)
        self.mars_checkbox.setObjectName(u"mars_checkbox")
        self.mars_checkbox.setChecked(True)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.mars_checkbox)

        self.jupiter_checkbox = QCheckBox(self.targets_groupbox)
        self.targets_buttongroup.addButton(self.jupiter_checkbox)
        self.jupiter_checkbox.setObjectName(u"jupiter_checkbox")
        self.jupiter_checkbox.setChecked(True)

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.jupiter_checkbox)

        self.saturn_checkbox = QCheckBox(self.targets_groupbox)
        self.targets_buttongroup.addButton(self.saturn_checkbox)
        self.saturn_checkbox.setObjectName(u"saturn_checkbox")
        self.saturn_checkbox.setChecked(True)

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.saturn_checkbox)

        self.uranus_checkbox = QCheckBox(self.targets_groupbox)
        self.targets_buttongroup.addButton(self.uranus_checkbox)
        self.uranus_checkbox.setObjectName(u"uranus_checkbox")
        self.uranus_checkbox.setChecked(True)

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.uranus_checkbox)

        self.neptune_checkbox = QCheckBox(self.targets_groupbox)
        self.targets_buttongroup.addButton(self.neptune_checkbox)
        self.neptune_checkbox.setObjectName(u"neptune_checkbox")
        self.neptune_checkbox.setChecked(True)

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.neptune_checkbox)

        self.venusfilters_button = QToolButton(self.targets_groupbox)
        self.filters_buttongroup = QButtonGroup(ScheduleBrainDialog)
        self.filters_buttongroup.setObjectName(u"filters_buttongroup")
        self.filters_buttongroup.addButton(self.venusfilters_button)
        self.venusfilters_button.setObjectName(u"venusfilters_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.venusfilters_button.sizePolicy().hasHeightForWidth())
        self.venusfilters_button.setSizePolicy(sizePolicy1)
        icon = QIcon()
        icon.addFile(u":/icons/ic_tonality_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.venusfilters_button.setIcon(icon)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.venusfilters_button)

        self.mercuryfilters_button = QToolButton(self.targets_groupbox)
        self.filters_buttongroup.addButton(self.mercuryfilters_button)
        self.mercuryfilters_button.setObjectName(u"mercuryfilters_button")
        sizePolicy1.setHeightForWidth(self.mercuryfilters_button.sizePolicy().hasHeightForWidth())
        self.mercuryfilters_button.setSizePolicy(sizePolicy1)
        self.mercuryfilters_button.setIcon(icon)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.mercuryfilters_button)

        self.marsfilters_button = QToolButton(self.targets_groupbox)
        self.filters_buttongroup.addButton(self.marsfilters_button)
        self.marsfilters_button.setObjectName(u"marsfilters_button")
        sizePolicy1.setHeightForWidth(self.marsfilters_button.sizePolicy().hasHeightForWidth())
        self.marsfilters_button.setSizePolicy(sizePolicy1)
        self.marsfilters_button.setIcon(icon)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.marsfilters_button)

        self.jupiterfilters_button = QToolButton(self.targets_groupbox)
        self.filters_buttongroup.addButton(self.jupiterfilters_button)
        self.jupiterfilters_button.setObjectName(u"jupiterfilters_button")
        sizePolicy1.setHeightForWidth(self.jupiterfilters_button.sizePolicy().hasHeightForWidth())
        self.jupiterfilters_button.setSizePolicy(sizePolicy1)
        self.jupiterfilters_button.setIcon(icon)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.jupiterfilters_button)

        self.saturnfilters_button = QToolButton(self.targets_groupbox)
        self.filters_buttongroup.addButton(self.saturnfilters_button)
        self.saturnfilters_button.setObjectName(u"saturnfilters_button")
        sizePolicy1.setHeightForWidth(self.saturnfilters_button.sizePolicy().hasHeightForWidth())
        self.saturnfilters_button.setSizePolicy(sizePolicy1)
        self.saturnfilters_button.setIcon(icon)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.saturnfilters_button)

        self.uranusfilters_button = QToolButton(self.targets_groupbox)
        self.filters_buttongroup.addButton(self.uranusfilters_button)
        self.uranusfilters_button.setObjectName(u"uranusfilters_button")
        sizePolicy1.setHeightForWidth(self.uranusfilters_button.sizePolicy().hasHeightForWidth())
        self.uranusfilters_button.setSizePolicy(sizePolicy1)
        self.uranusfilters_button.setIcon(icon)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.uranusfilters_button)

        self.neptunefilters_button = QToolButton(self.targets_groupbox)
        self.filters_buttongroup.addButton(self.neptunefilters_button)
        self.neptunefilters_button.setObjectName(u"neptunefilters_button")
        sizePolicy1.setHeightForWidth(self.neptunefilters_button.sizePolicy().hasHeightForWidth())
        self.neptunefilters_button.setSizePolicy(sizePolicy1)
        self.neptunefilters_button.setIcon(icon)

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.neptunefilters_button)


        self.gridLayout.addWidget(self.targets_groupbox, 1, 0, 2, 1, Qt.AlignTop)

        self.form_layout = QFormLayout()
        self.form_layout.setObjectName(u"form_layout")
        self.direction_label = QLabel(ScheduleBrainDialog)
        self.direction_label.setObjectName(u"direction_label")

        self.form_layout.setWidget(4, QFormLayout.LabelRole, self.direction_label)

        self.directional_combobox = QComboBox(ScheduleBrainDialog)
        self.directional_combobox.addItem("")
        self.directional_combobox.addItem("")
        self.directional_combobox.addItem("")
        self.directional_combobox.setObjectName(u"directional_combobox")

        self.form_layout.setWidget(4, QFormLayout.FieldRole, self.directional_combobox)

        self.targetpreference_label = QLabel(ScheduleBrainDialog)
        self.targetpreference_label.setObjectName(u"targetpreference_label")

        self.form_layout.setWidget(5, QFormLayout.LabelRole, self.targetpreference_label)

        self.time_layout = QHBoxLayout()
        self.time_layout.setObjectName(u"time_layout")
        self.start_timeedit = QTimeEdit(ScheduleBrainDialog)
        self.start_timeedit.setObjectName(u"start_timeedit")
        self.start_timeedit.setMaximumDateTime(QDateTime(QDate(2000, 1, 1), QTime(23, 59, 0)))
        self.start_timeedit.setMaximumTime(QTime(23, 59, 0))
        self.start_timeedit.setTime(QTime(0, 0, 0))

        self.time_layout.addWidget(self.start_timeedit)

        self.time_to_label = QLabel(ScheduleBrainDialog)
        self.time_to_label.setObjectName(u"time_to_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.time_to_label.sizePolicy().hasHeightForWidth())
        self.time_to_label.setSizePolicy(sizePolicy2)

        self.time_layout.addWidget(self.time_to_label)

        self.end_timeedit = QTimeEdit(ScheduleBrainDialog)
        self.end_timeedit.setObjectName(u"end_timeedit")
        self.end_timeedit.setDateTime(QDateTime(QDate(2000, 1, 1), QTime(23, 59, 0)))
        self.end_timeedit.setMaximumDateTime(QDateTime(QDate(2000, 1, 1), QTime(23, 59, 0)))
        self.end_timeedit.setMinimumDateTime(QDateTime(QDate(2000, 1, 1), QTime(0, 0, 0)))
        self.end_timeedit.setMinimumTime(QTime(0, 0, 0))
        self.end_timeedit.setTimeSpec(Qt.LocalTime)

        self.time_layout.addWidget(self.end_timeedit)


        self.form_layout.setLayout(0, QFormLayout.FieldRole, self.time_layout)

        self.elevationrange_layout = QHBoxLayout()
        self.elevationrange_layout.setObjectName(u"elevationrange_layout")
        self.minelevation_spinbox = QSpinBox(ScheduleBrainDialog)
        self.minelevation_spinbox.setObjectName(u"minelevation_spinbox")
        self.minelevation_spinbox.setMaximum(89)
        self.minelevation_spinbox.setValue(12)

        self.elevationrange_layout.addWidget(self.minelevation_spinbox)

        self.elevation_to_label = QLabel(ScheduleBrainDialog)
        self.elevation_to_label.setObjectName(u"elevation_to_label")
        sizePolicy2.setHeightForWidth(self.elevation_to_label.sizePolicy().hasHeightForWidth())
        self.elevation_to_label.setSizePolicy(sizePolicy2)

        self.elevationrange_layout.addWidget(self.elevation_to_label)

        self.maxelevation_spinbox = QSpinBox(ScheduleBrainDialog)
        self.maxelevation_spinbox.setObjectName(u"maxelevation_spinbox")
        self.maxelevation_spinbox.setMinimum(1)
        self.maxelevation_spinbox.setMaximum(90)
        self.maxelevation_spinbox.setValue(90)

        self.elevationrange_layout.addWidget(self.maxelevation_spinbox)


        self.form_layout.setLayout(1, QFormLayout.FieldRole, self.elevationrange_layout)

        self.sunelevation_spinbox = QSpinBox(ScheduleBrainDialog)
        self.sunelevation_spinbox.setObjectName(u"sunelevation_spinbox")
        self.sunelevation_spinbox.setMinimum(-90)
        self.sunelevation_spinbox.setMaximum(90)
        self.sunelevation_spinbox.setValue(-18)

        self.form_layout.setWidget(2, QFormLayout.FieldRole, self.sunelevation_spinbox)

        self.time_label = QLabel(ScheduleBrainDialog)
        self.time_label.setObjectName(u"time_label")

        self.form_layout.setWidget(0, QFormLayout.LabelRole, self.time_label)

        self.elevation_label = QLabel(ScheduleBrainDialog)
        self.elevation_label.setObjectName(u"elevation_label")

        self.form_layout.setWidget(1, QFormLayout.LabelRole, self.elevation_label)

        self.darkness_label = QLabel(ScheduleBrainDialog)
        self.darkness_label.setObjectName(u"darkness_label")

        self.form_layout.setWidget(2, QFormLayout.LabelRole, self.darkness_label)

        self.targetpreference_combobox = QComboBox(ScheduleBrainDialog)
        self.targetpreference_combobox.addItem("")
        self.targetpreference_combobox.addItem("")
        self.targetpreference_combobox.setObjectName(u"targetpreference_combobox")

        self.form_layout.setWidget(5, QFormLayout.FieldRole, self.targetpreference_combobox)

        self.notarget_label = QLabel(ScheduleBrainDialog)
        self.notarget_label.setObjectName(u"notarget_label")

        self.form_layout.setWidget(6, QFormLayout.LabelRole, self.notarget_label)

        self.notarget_combobox = QComboBox(ScheduleBrainDialog)
        self.notarget_combobox.addItem("")
        self.notarget_combobox.addItem("")
        self.notarget_combobox.setObjectName(u"notarget_combobox")

        self.form_layout.setWidget(6, QFormLayout.FieldRole, self.notarget_combobox)

        self.endaction_label = QLabel(ScheduleBrainDialog)
        self.endaction_label.setObjectName(u"endaction_label")

        self.form_layout.setWidget(7, QFormLayout.LabelRole, self.endaction_label)

        self.endaction_combobox = QComboBox(ScheduleBrainDialog)
        self.endaction_combobox.addItem("")
        self.endaction_combobox.addItem("")
        self.endaction_combobox.setObjectName(u"endaction_combobox")

        self.form_layout.setWidget(7, QFormLayout.FieldRole, self.endaction_combobox)

        self.interval_label = QLabel(ScheduleBrainDialog)
        self.interval_label.setObjectName(u"interval_label")

        self.form_layout.setWidget(3, QFormLayout.LabelRole, self.interval_label)

        self.interval_spinbox = QSpinBox(ScheduleBrainDialog)
        self.interval_spinbox.setObjectName(u"interval_spinbox")
        self.interval_spinbox.setMinimum(2)
        self.interval_spinbox.setMaximum(60)

        self.form_layout.setWidget(3, QFormLayout.FieldRole, self.interval_spinbox)


        self.gridLayout.addLayout(self.form_layout, 1, 1, 1, 1)

        self.plot_layout = QHBoxLayout()
        self.plot_layout.setObjectName(u"plot_layout")

        self.gridLayout.addLayout(self.plot_layout, 0, 0, 1, 2)


        self.retranslateUi(ScheduleBrainDialog)
        self.buttonbox.accepted.connect(ScheduleBrainDialog.accept)
        self.buttonbox.rejected.connect(ScheduleBrainDialog.reject)

        self.directional_combobox.setCurrentIndex(1)
        self.endaction_combobox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(ScheduleBrainDialog)
    # setupUi

    def retranslateUi(self, ScheduleBrainDialog):
        ScheduleBrainDialog.setWindowTitle(QCoreApplication.translate("ScheduleBrainDialog", u"Schedule Brain", None))
        self.targets_groupbox.setTitle(QCoreApplication.translate("ScheduleBrainDialog", u"Targets", None))
        self.mercury_checkbox.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Mercury", None))
        self.venus_checkbox.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Venus", None))
        self.mars_checkbox.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Mars", None))
        self.jupiter_checkbox.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Jupiter", None))
        self.saturn_checkbox.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Saturn", None))
        self.uranus_checkbox.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Uranus", None))
        self.neptune_checkbox.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Neptune", None))
        self.venusfilters_button.setText("")
        self.mercuryfilters_button.setText("")
        self.marsfilters_button.setText("")
        self.jupiterfilters_button.setText("")
        self.saturnfilters_button.setText("")
        self.uranusfilters_button.setText("")
        self.neptunefilters_button.setText("")
        self.direction_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Direction", None))
        self.directional_combobox.setItemText(0, QCoreApplication.translate("ScheduleBrainDialog", u"East", None))
        self.directional_combobox.setItemText(1, QCoreApplication.translate("ScheduleBrainDialog", u"Both", None))
        self.directional_combobox.setItemText(2, QCoreApplication.translate("ScheduleBrainDialog", u"West", None))

        self.targetpreference_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Target Preference", None))
#if QT_CONFIG(tooltip)
        self.start_timeedit.setToolTip(QCoreApplication.translate("ScheduleBrainDialog", u"Start time", None))
#endif // QT_CONFIG(tooltip)
        self.start_timeedit.setDisplayFormat(QCoreApplication.translate("ScheduleBrainDialog", u"hh:mm UTC", None))
        self.time_to_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"to", None))
#if QT_CONFIG(tooltip)
        self.end_timeedit.setToolTip(QCoreApplication.translate("ScheduleBrainDialog", u"End time", None))
#endif // QT_CONFIG(tooltip)
        self.end_timeedit.setDisplayFormat(QCoreApplication.translate("ScheduleBrainDialog", u"hh:mm UTC", None))
#if QT_CONFIG(tooltip)
        self.minelevation_spinbox.setToolTip(QCoreApplication.translate("ScheduleBrainDialog", u"Minimum elevation of targets", None))
#endif // QT_CONFIG(tooltip)
        self.minelevation_spinbox.setSuffix(QCoreApplication.translate("ScheduleBrainDialog", u"\u00b0", None))
        self.elevation_to_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"to", None))
#if QT_CONFIG(tooltip)
        self.maxelevation_spinbox.setToolTip(QCoreApplication.translate("ScheduleBrainDialog", u"Maximum elevation of targets", None))
#endif // QT_CONFIG(tooltip)
        self.maxelevation_spinbox.setSuffix(QCoreApplication.translate("ScheduleBrainDialog", u"\u00b0", None))
#if QT_CONFIG(tooltip)
        self.sunelevation_spinbox.setToolTip(QCoreApplication.translate("ScheduleBrainDialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Night<br/></span>Sun &gt; 18\u00b0 below horizon</p><p><span style=\" font-weight:600;\">Astronomical Twilight<br/></span>Sun 12\u00b0-18\u00b0 below horizon</p><p><span style=\" font-weight:600;\">Nautical Twilight<br/></span>Sun 6\u00b0-12\u00b0 below horizon</p><p><span style=\" font-weight:600;\">Civil Twilight<br/></span>Sun 0\u00b0-6\u00b0 below horizon</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.sunelevation_spinbox.setSuffix(QCoreApplication.translate("ScheduleBrainDialog", u"\u00b0", None))
        self.time_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Time Range", None))
        self.elevation_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Elevation Range", None))
        self.darkness_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Max Sun Elevation", None))
        self.targetpreference_combobox.setItemText(0, QCoreApplication.translate("ScheduleBrainDialog", u"Less for longer", None))
        self.targetpreference_combobox.setItemText(1, QCoreApplication.translate("ScheduleBrainDialog", u"Prefer highest", None))

        self.notarget_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"No Target Action", None))
        self.notarget_combobox.setItemText(0, QCoreApplication.translate("ScheduleBrainDialog", u"Stop", None))
        self.notarget_combobox.setItemText(1, QCoreApplication.translate("ScheduleBrainDialog", u"Home", None))

#if QT_CONFIG(tooltip)
        self.notarget_combobox.setToolTip(QCoreApplication.translate("ScheduleBrainDialog", u"Action to perform if no targets are available", None))
#endif // QT_CONFIG(tooltip)
        self.endaction_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"End Action", None))
        self.endaction_combobox.setItemText(0, QCoreApplication.translate("ScheduleBrainDialog", u"Stop", None))
        self.endaction_combobox.setItemText(1, QCoreApplication.translate("ScheduleBrainDialog", u"Home", None))

#if QT_CONFIG(tooltip)
        self.endaction_combobox.setToolTip(QCoreApplication.translate("ScheduleBrainDialog", u"Action to perform if no targets are available", None))
#endif // QT_CONFIG(tooltip)
        self.interval_label.setText(QCoreApplication.translate("ScheduleBrainDialog", u"Interval", None))
#if QT_CONFIG(tooltip)
        self.interval_spinbox.setToolTip(QCoreApplication.translate("ScheduleBrainDialog", u"Time intervals at which to calculate between start and end times", None))
#endif // QT_CONFIG(tooltip)
        self.interval_spinbox.setSuffix(QCoreApplication.translate("ScheduleBrainDialog", u" Minutes", None))
    # retranslateUi

