# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ConverterDialog
                                 A QGIS plugin
 This plugin converts Vietnamese Fonts between encodings
                             -------------------
        begin                : 2016-08-31
        git sha              : $Format:%H$
        copyright            : (C) 2016 by ThanhGIS
        email                : thanh.nv@me.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import QSettings, QThread, QFileInfo
from PyQt4.QtGui import QDialog, QDialogButtonBox, QFileDialog

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsMessageLog
from qgis.gui import QgsEncodingFileDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'vn_fonts_dialog_base.ui'))


class ConverterDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ConverterDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
 	self.setupUi(self)