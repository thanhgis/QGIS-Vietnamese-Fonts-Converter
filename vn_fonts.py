#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Converter
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
from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4.QtGui import QAction, QIcon, QAbstractItemView, QFileDialog, QProgressBar
from qgis.gui import QgsMessageBar
from processing.tools.vector import VectorWriter
import time
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from vn_fonts_dialog import ConverterDialog
#from vn_fonts_dialog.ConverterDialog import ConverterDialog
import os.path


class Converter:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Converter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ConverterDialog()
        #self.ui = Ui_ConverterDialogBase()

        # Declare instance attributes
        self.actions = []
        self.menu = u'&Chuyển đổi mã font chữ tiếng Việt'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Converter')
        self.toolbar.setObjectName(u'Converter')
        self.dlg.output_layer.clear()
        self.dlg.output_select_Button.clicked.connect(self.select_output)
        	
    # noinspection PyMethodMayBeStatic
    			
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Converter', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

  

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Converter/icon.png'
        self.add_action(
            icon_path,
            text=u'Chuyển đổi mã font chữ tiếng Việt',
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                u'&Chuyển đổi mã font chữ tiếng Việt',
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
    """Chọn tập tin vector đầu ra"""
    def select_output(self):
        filename = QFileDialog.getSaveFileName(self.dlg, u"Chọn thư mục và tên lớp đầu ra ","", '*.shp')
        self.dlg.output_layer.setText(filename)
    def run(self):
        """Run method that performs all the real work"""
        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        self.dlg.input_layer.addItems(layer_list)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            filename = self.dlg.output_layer.text()
            selectedLayerIndex = self.dlg.input_layer.currentIndex()
            selectedLayer = layers[selectedLayerIndex]
            loaicd = self.dlg.type_Box.currentText()
            shapeWriter = VectorWriter(filename, "UTF-8", selectedLayer.dataProvider().fields(),selectedLayer.dataProvider().geometryType(), selectedLayer.crs())
            features = selectedLayer.getFeatures()
            textfield = []
            for field in selectedLayer.dataProvider().fields():
                if field.type() in [QVariant.String]:
                    textfield.append(field.name())
            for feat in features:
                for ab in textfield:
                    abc = feat[ab]
                    if abc != None:
                        if loaicd == "TCVN (ABC) >> Unicode":
                            bc = abc.replace(u'¨',u'ă').replace(u'¡',u'Ă').replace(u'®',u'đ').replace(u'§',u'Đ').replace(u'¬',u'ơ').replace(u'¥',u'Ơ').replace(u'­',u'ư').replace(u'¦',u'Ư').replace(u'µ',u'à').replace(u'µ',u'À').replace(u'¶',u'ả').replace(u'¶',u'Ả').replace(u'¹',u'ạ').replace(u'¹',u'Ạ').replace(u'Ê',u'ấ').replace(u'Ê',u'Ấ').replace(u'Ç',u'ầ').replace(u'Ç',u'Ầ').replace(u'È',u'ẩ').replace(u'È',u'Ẩ').replace(u'É',u'ẫ').replace(u'É',u'Ẫ').replace(u'Ë',u'ậ').replace(u'Ë',u'Ậ').replace(u'¾',u'ắ').replace(u'¾',u'Ắ').replace(u'»',u'ằ').replace(u'»',u'Ằ').replace(u'¼',u'ẳ').replace(u'¼',u'Ẳ').replace(u'½',u'ẵ').replace(u'½',u'Ẵ').replace(u'Æ',u'ặ').replace(u'Æ',u'Ặ').replace(u'Ð',u'é').replace(u'Ð',u'É').replace(u'Î',u'ẻ').replace(u'Î',u'Ẻ').replace(u'Ï',u'ẽ').replace(u'Ï',u'Ẽ').replace(u'Ñ',u'ẹ').replace(u'Ñ',u'Ẹ').replace(u'Õ',u'ế').replace(u'Õ',u'Ế').replace(u'Ò',u'ề').replace(u'Ò',u'Ề').replace(u'Ó',u'ể').replace(u'Ó',u'Ể').replace(u'Ô',u'ễ').replace(u'Ô',u'Ễ').replace(u'Ö',u'ệ').replace(u'Ö',u'Ệ').replace(u'Ø',u'ỉ').replace(u'Ø',u'Ỉ').replace(u'Ü',u'ĩ').replace(u'Ü',u'Ĩ').replace(u'Þ',u'ị').replace(u'Þ',u'Ị').replace(u'á',u'ỏ').replace(u'á',u'Ỏ').replace(u'â',u'õ').replace(u'â',u'Õ').replace(u'ä',u'ọ').replace(u'ä',u'Ọ').replace(u'è',u'ố').replace(u'è',u'Ố').replace(u'Ì',u'è').replace(u'Ì',u'È').replace(u'å',u'ồ').replace(u'å',u'Ồ').replace(u'æ',u'ổ').replace(u'æ',u'Ổ').replace(u'ç',u'ỗ').replace(u'ç',u'Ỗ').replace(u'é',u'ộ').replace(u'é',u'Ộ').replace(u'í',u'ớ').replace(u'í',u'Ớ').replace(u'ê',u'ờ').replace(u'ê',u'Ờ').replace(u'ë',u'ở').replace(u'ë',u'Ở').replace(u'ì',u'ỡ').replace(u'ì',u'Ỡ').replace(u'î',u'ợ').replace(u'î',u'Ợ').replace(u'×',u'ì').replace(u'×',u'Ì').replace(u'¸',u'á').replace(u'¸',u'Á').replace(u'©',u'â').replace(u'¢',u'Â').replace(u'ù',u'ự').replace(u'ù',u'Ự').replace(u'ï',u'ù').replace(u'ï',u'Ù').replace(u'ñ',u'ủ').replace(u'ñ',u'Ủ').replace(u'ô',u'ụ').replace(u'ô',u'Ụ').replace(u'ø',u'ứ').replace(u'ø',u'Ứ').replace(u'õ',u'ừ').replace(u'õ',u'Ừ').replace(u'ö',u'ử').replace(u'ö',u'Ử').replace(u'÷',u'ữ').replace(u'÷',u'Ữ').replace(u'ú',u'ỳ').replace(u'ú',u'Ỳ').replace(u'û',u'ỷ').replace(u'û',u'Ỷ').replace(u'ü',u'ỹ').replace(u'ü',u'Ỹ').replace(u'þ',u'ỵ').replace(u'þ',u'Ỵ').replace(u'ý',u'ý').replace(u'ý',u'Ý').replace(u'«',u'ô').replace(u'¤',u'Ô').replace(u'ó',u'ú').replace(u'ó',u'Ú').replace(u'ã',u'ó').replace(u'ã',u'Ó').replace(u'·',u'ã').replace(u'·',u'Ã').replace(u'Ý',u'í').replace(u'Ý',u'Í').replace(u'ª',u'ê').replace(u'£',u'Ê').replace(u'ò',u'ũ').replace(u'ò',u'Ũ').replace(u'ß',u'ò').replace(u'ß',u'Ò')
                            feat[ab] = bc
                        elif loaicd == "Unicode >> TCVN (ABC)":
                            bd = abc.replace(u'ă',u'¨').replace(u'Ă',u'¡').replace(u'đ',u'®').replace(u'Đ',u'§').replace(u'ơ',u'¬').replace(u'Ơ',u'¥').replace(u'ư',u'­').replace(u'Ư',u'¦').replace(u'à',u'µ').replace(u'À',u'µ').replace(u'ả',u'¶').replace(u'Ả',u'¶').replace(u'ạ',u'¹').replace(u'Ạ',u'¹').replace(u'ấ',u'Ê').replace(u'Ấ',u'Ê').replace(u'ầ',u'Ç').replace(u'Ầ',u'Ç').replace(u'ẩ',u'È').replace(u'Ẩ',u'È').replace(u'ẫ',u'É').replace(u'Ẫ',u'É').replace(u'ậ',u'Ë').replace(u'Ậ',u'Ë').replace(u'ắ',u'¾').replace(u'Ắ',u'¾').replace(u'ằ',u'»').replace(u'Ằ',u'»').replace(u'ẳ',u'¼').replace(u'Ẳ',u'¼').replace(u'ẵ',u'½').replace(u'Ẵ',u'½').replace(u'ặ',u'Æ').replace(u'Ặ',u'Æ').replace(u'é',u'Ð').replace(u'É',u'Ð').replace(u'ẻ',u'Î').replace(u'Ẻ',u'Î').replace(u'ẽ',u'Ï').replace(u'Ẽ',u'Ï').replace(u'ẹ',u'Ñ').replace(u'Ẹ',u'Ñ').replace(u'ế',u'Õ').replace(u'Ế',u'Õ').replace(u'ề',u'Ò').replace(u'Ề',u'Ò').replace(u'ể',u'Ó').replace(u'Ể',u'Ó').replace(u'ễ',u'Ô').replace(u'Ễ',u'Ô').replace(u'ệ',u'Ö').replace(u'Ệ',u'Ö').replace(u'ỉ',u'Ø').replace(u'Ỉ',u'Ø').replace(u'ĩ',u'Ü').replace(u'Ĩ',u'Ü').replace(u'ị',u'Þ').replace(u'Ị',u'Þ').replace(u'ò',u'ß').replace(u'Ò',u'ß').replace(u'ỏ',u'á').replace(u'Ỏ',u'á').replace(u'õ',u'â').replace(u'Õ',u'â').replace(u'ọ',u'ä').replace(u'Ọ',u'ä').replace(u'ố',u'è').replace(u'Ố',u'è').replace(u'è',u'Ì').replace(u'È',u'Ì').replace(u'ồ',u'å').replace(u'Ồ',u'å').replace(u'ổ',u'æ').replace(u'Ổ',u'æ').replace(u'ỗ',u'ç').replace(u'Ỗ',u'ç').replace(u'ộ',u'é').replace(u'Ộ',u'é').replace(u'ớ',u'í').replace(u'Ớ',u'í').replace(u'ờ',u'ê').replace(u'Ờ',u'ê').replace(u'ở',u'ë').replace(u'Ở',u'ë').replace(u'ỡ',u'ì').replace(u'Ỡ',u'ì').replace(u'ợ',u'î').replace(u'Ợ',u'î').replace(u'ì',u'×').replace(u'Ì',u'×').replace(u'á',u'¸').replace(u'Á',u'¸').replace(u'â',u'©').replace(u'Â',u'¢').replace(u'ự',u'ù').replace(u'Ự',u'ù').replace(u'ù',u'ï').replace(u'Ù',u'ï').replace(u'ủ',u'ñ').replace(u'Ủ',u'ñ').replace(u'ũ',u'ò').replace(u'Ũ',u'ò').replace(u'ụ',u'ô').replace(u'Ụ',u'ô').replace(u'ứ',u'ø').replace(u'Ứ',u'ø').replace(u'ừ',u'õ').replace(u'Ừ',u'õ').replace(u'ử',u'ö').replace(u'Ử',u'ö').replace(u'ữ',u'÷').replace(u'Ữ',u'÷').replace(u'ỳ',u'ú').replace(u'Ỳ',u'ú').replace(u'ỷ',u'û').replace(u'Ỷ',u'û').replace(u'ỹ',u'ü').replace(u'Ỹ',u'ü').replace(u'ỵ',u'þ').replace(u'Ỵ',u'þ').replace(u'ý',u'ý').replace(u'Ý',u'ý').replace(u'ô',u'«').replace(u'Ô',u'¤').replace(u'ú',u'ó').replace(u'Ú',u'ó').replace(u'ó',u'ã').replace(u'Ó',u'ã').replace(u'ã',u'·').replace(u'Ã',u'·').replace(u'í',u'Ý').replace(u'Í',u'Ý').replace(u'ê',u'ª').replace(u'Ê',u'£')
                            feat[ab] = bd
                        elif loaicd == "TCVN (ABC) >> Khong dau":
                            be = abc.replace(u'¨',u'a').replace(u'¡',u'A').replace(u'®',u'd').replace(u'§',u'D').replace(u'¬',u'o').replace(u'¥',u'O').replace(u'­',u'u').replace(u'¦',u'U').replace(u'µ',u'a').replace(u'µ',u'A').replace(u'¶',u'a').replace(u'¶',u'A').replace(u'¹',u'a').replace(u'¹',u'A').replace(u'Ê',u'a').replace(u'Ê',u'A').replace(u'Ç',u'a').replace(u'Ç',u'A').replace(u'È',u'a').replace(u'È',u'A').replace(u'É',u'a').replace(u'É',u'A').replace(u'Ë',u'a').replace(u'Ë',u'A').replace(u'¾',u'a').replace(u'¾',u'A').replace(u'»',u'a').replace(u'»',u'A').replace(u'¼',u'a').replace(u'¼',u'A').replace(u'½',u'a').replace(u'½',u'A').replace(u'Æ',u'a').replace(u'Æ',u'A').replace(u'Ð',u'e').replace(u'Ð',u'E').replace(u'Î',u'e').replace(u'Î',u'E').replace(u'Ï',u'e').replace(u'Ï',u'E').replace(u'Ñ',u'e').replace(u'Ñ',u'E').replace(u'Õ',u'e').replace(u'Õ',u'E').replace(u'Ò',u'e').replace(u'Ò',u'E').replace(u'Ó',u'e').replace(u'Ó',u'E').replace(u'Ô',u'e').replace(u'Ô',u'E').replace(u'Ö',u'e').replace(u'Ö',u'E').replace(u'Ø',u'i').replace(u'Ø',u'I').replace(u'Ü',u'i').replace(u'Ü',u'I').replace(u'Þ',u'i').replace(u'Þ',u'I').replace(u'ß',u'o').replace(u'ß',u'O').replace(u'á',u'o').replace(u'á',u'O').replace(u'â',u'o').replace(u'â',u'O').replace(u'ä',u'o').replace(u'ä',u'O').replace(u'è',u'o').replace(u'è',u'O').replace(u'Ì',u'e').replace(u'Ì',u'E').replace(u'å',u'o').replace(u'å',u'O').replace(u'æ',u'o').replace(u'æ',u'O').replace(u'ç',u'o').replace(u'ç',u'O').replace(u'é',u'o').replace(u'é',u'O').replace(u'í',u'o').replace(u'í',u'O').replace(u'ê',u'o').replace(u'ê',u'O').replace(u'ë',u'o').replace(u'ë',u'O').replace(u'ì',u'o').replace(u'ì',u'O').replace(u'î',u'o').replace(u'î',u'O').replace(u'×',u'i').replace(u'×',u'I').replace(u'¸',u'a').replace(u'¸',u'A').replace(u'©',u'a').replace(u'¢',u'A').replace(u'ù',u'u').replace(u'ù',u'U').replace(u'ï',u'u').replace(u'ï',u'U').replace(u'ñ',u'u').replace(u'ñ',u'U').replace(u'ò',u'u').replace(u'ò',u'U').replace(u'ô',u'u').replace(u'ô',u'U').replace(u'ø',u'u').replace(u'ø',u'U').replace(u'õ',u'u').replace(u'õ',u'U').replace(u'ö',u'u').replace(u'ö',u'U').replace(u'÷',u'u').replace(u'÷',u'U').replace(u'ú',u'y').replace(u'ú',u'Y').replace(u'û',u'y').replace(u'û',u'Y').replace(u'ü',u'y').replace(u'ü',u'Y').replace(u'þ',u'y').replace(u'þ',u'Y').replace(u'ý',u'y').replace(u'ý',u'Y').replace(u'«',u'o').replace(u'¤',u'O').replace(u'ó',u'u').replace(u'ó',u'U').replace(u'ã',u'o').replace(u'ã',u'O').replace(u'·',u'a').replace(u'·',u'A').replace(u'Ý',u'i').replace(u'Ý',u'I').replace(u'ª',u'e').replace(u'£',u'E')
                            feat[ab] = be
                        elif loaicd == "Unicode >> Khong dau":
                            bf = abc.replace(u'ă',u'a').replace(u'Ă',u'A').replace(u'đ',u'd').replace(u'Đ',u'D').replace(u'ơ',u'o').replace(u'Ơ',u'O').replace(u'ư',u'u').replace(u'Ư',u'U').replace(u'à',u'a').replace(u'À',u'A').replace(u'ả',u'a').replace(u'Ả',u'A').replace(u'ạ',u'a').replace(u'Ạ',u'A').replace(u'ấ',u'a').replace(u'Ấ',u'A').replace(u'ầ',u'a').replace(u'Ầ',u'A').replace(u'ẩ',u'a').replace(u'Ẩ',u'A').replace(u'ẫ',u'a').replace(u'Ẫ',u'A').replace(u'ậ',u'a').replace(u'Ậ',u'A').replace(u'ắ',u'a').replace(u'Ắ',u'A').replace(u'ằ',u'a').replace(u'Ằ',u'A').replace(u'ẳ',u'a').replace(u'Ẳ',u'A').replace(u'ẵ',u'a').replace(u'Ẵ',u'A').replace(u'ặ',u'a').replace(u'Ặ',u'A').replace(u'é',u'e').replace(u'É',u'E').replace(u'ẻ',u'e').replace(u'Ẻ',u'E').replace(u'ẽ',u'e').replace(u'Ẽ',u'E').replace(u'ẹ',u'e').replace(u'Ẹ',u'E').replace(u'ế',u'e').replace(u'Ế',u'E').replace(u'ề',u'e').replace(u'Ề',u'E').replace(u'ể',u'e').replace(u'Ể',u'E').replace(u'ễ',u'e').replace(u'Ễ',u'O').replace(u'ệ',u'e').replace(u'Ệ',u'E').replace(u'ỉ',u'i').replace(u'Ỉ',u'I').replace(u'ĩ',u'i').replace(u'Ĩ',u'I').replace(u'ị',u'i').replace(u'Ị',u'I').replace(u'ò',u'o').replace(u'Ò',u'O').replace(u'ỏ',u'o').replace(u'Ỏ',u'O').replace(u'õ',u'o').replace(u'Õ',u'O').replace(u'ọ',u'o').replace(u'Ọ',u'O').replace(u'ố',u'o').replace(u'Ố',u'O').replace(u'è',u'e').replace(u'È',u'E').replace(u'ồ',u'o').replace(u'Ồ',u'O').replace(u'ổ',u'o').replace(u'Ổ',u'O').replace(u'ỗ',u'o').replace(u'Ỗ',u'O').replace(u'ộ',u'o').replace(u'Ộ',u'O').replace(u'ớ',u'o').replace(u'Ớ',u'O').replace(u'ờ',u'o').replace(u'Ờ',u'O').replace(u'ở',u'o').replace(u'Ở',u'O').replace(u'ỡ',u'o').replace(u'Ỡ',u'O').replace(u'ợ',u'o').replace(u'Ợ',u'O').replace(u'ì',u'i').replace(u'Ì',u'I').replace(u'á',u'a').replace(u'Á',u'A').replace(u'â',u'a').replace(u'Â',u'A').replace(u'ự',u'u').replace(u'Ự',u'U').replace(u'ù',u'u').replace(u'Ù',u'U').replace(u'ủ',u'u').replace(u'Ủ',u'U').replace(u'ũ',u'u').replace(u'Ũ',u'U').replace(u'ụ',u'u').replace(u'Ụ',u'U').replace(u'ứ',u'u').replace(u'Ứ',u'U').replace(u'ừ',u'u').replace(u'Ừ',u'U').replace(u'ử',u'u').replace(u'Ử',u'U').replace(u'ữ',u'u').replace(u'Ữ',u'U').replace(u'ỳ',u'y').replace(u'Ỳ',u'Y').replace(u'ỷ',u'y').replace(u'Ỷ',u'Y').replace(u'ỹ',u'y').replace(u'Ỹ',u'Y').replace(u'ỵ',u'y').replace(u'Ỵ',u'Y').replace(u'ý',u'y').replace(u'Ý',u'Y').replace(u'ô',u'o').replace(u'Ô',u'O').replace(u'ú',u'u').replace(u'Ú',u'U').replace(u'ó',u'o').replace(u'Ó',u'O').replace(u'ã',u'a').replace(u'Ã',u'A').replace(u'í',u'i').replace(u'Í',u'Y').replace(u'ê',u'e').replace(u'Ê',u'E')
                            feat[ab] = bf
                        else: pass
                shapeWriter.addFeature(feat)
            self._restoreGui()
            del shapeWriter
            layer = QgsVectorLayer(filename, QFileInfo(filename).baseName(), 'ogr')
            layer.setProviderEncoding(u'System')
	    layer.dataProvider().setEncoding(u'UTF-8')
            if layer.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(layer)
                self.iface.messageBar().pushMessage(u"Thành công: ", u"Đã chuyển đổi xong mã font chữ cho bảng thuộc tính", level = QgsMessageBar.SUCCESS, duration = 5)
            else:
                self.iface.messageBar().pushMessage(u"Lỗi: ", u"Chuyển đổi mã font chữ không thành công", level = QgsMessageBar.WARNING, duration = 5)
        return False
    def _restoreGui(self):
        self.dlg.output_layer.clear()
        self.dlg.input_layer.clear()
