# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Converter
                                 A QGIS plugin
 This plugin converts Vietnamese Fonts between encodings
                             -------------------
        begin                : 2016-08-31
        copyright            : (C) 2016 by ThanhGIS
        email                : thanh.nv@me.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Converter class from file Converter.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .vn_fonts import Converter
    return Converter(iface)
