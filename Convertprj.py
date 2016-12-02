# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ConvertprjBatch
                                 A QGIS plugin
 Chuyen he VN2000 Noi bo sang he khac
                              -------------------
        begin                : 2016-10-04
        git sha              : $Format:%H$
        copyright            : (C) 2016 by GFD
        email                : hoa.lq@gfd.com.vn
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
from qgis import *
from qgis.utils import *
from qgis.core import *
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
from qgis.core import QgsVectorFileWriter


# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Convertprj_dialog import ConvertprjBatchDialog
import os.path
import os


class ConvertprjBatch:
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
            'ConvertprjBatch_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ConvertprjBatchDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Convert coordinate system VN2000')
        # TODO: We are going to let the user set this up in a future iteration
        # self.toolbar = self.iface.addToolBar(u'BatchSaveLayers')
        # self.toolbar.setObjectName(u'BatchSaveLayers')
        
        self.dlg.lineEdit.clear()
        self.dlg.toolButton.clicked.connect(self.select_output)       
        

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
        return QCoreApplication.translate('ConvertprjBatch', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=False,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

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
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ConvertprjBatch/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Chuyen he VN2000 Noi bo sang he khac'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # add to plugin toolbar
        self.action1 = QAction(
            QIcon(":/plugins/ConvertprjBatch/icon.png"),
            u"&Convert coordinate system VN2000", self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action1)
        self.action1.triggered.connect(self.run)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Convert coordinate system VN2000'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        # del self.toolbar

        # remove from plugin toolbar
        self.iface.removeToolBarIcon(self.action1)

    # Select output file 
    def select_output(self):
        output_dir = QFileDialog.getExistingDirectory(self.dlg, "Chọn thư mục để lưu","")
        self.dlg.lineEdit.setText(output_dir)


    def run(self):
        """Run method that performs all the real work"""

        # Select the layers open in the legendInterface and add them to an array
        layers = self.iface.legendInterface().layers()
        layer_list = []
        # Append only Vector (type == 0) to the layer_list
        for layer in layers:
                if layer.type() == 0:
                    layer_list.append(layer.name())
                else:
                    pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlg.listWidget.clear()
        self.dlg.listWidget.addItems(layer_list)
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            # pass
            output_dir = self.dlg.lineEdit.text()

            if not os.path.exists(output_dir):
                self.iface.messageBar().pushMessage("Khong co duong dan den thu muc", "Vui long chon thu muc de luu file", 1, 5)
            if os.path.exists(output_dir):
                self.save_layers()

    def save_layers(self):
        # if checkbox is checked, run the appropriate save function
        if self.dlg.checkBox_shp.isChecked():
            self.save_esri_shapefile()
        else:
            pass


    # save shp
    def save_esri_shapefile(self):
        layers = self.iface.legendInterface().layers()
        output_dir = self.dlg.lineEdit.text() + "/" #+ "/KETQUA_SHP/"
        htd = self.dlg.comboBox.currentText()
        htd_output = self.dlg.comboBox_output.currentText()
        #Coordinate UTM, WGS84
        crs_4326 = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        htd_utm_48 = QgsCoordinateReferenceSystem(32648,QgsCoordinateReferenceSystem.EpsgCrsId)
        htd_utm_49 = QgsCoordinateReferenceSystem(32649, QgsCoordinateReferenceSystem.EpsgCrsId)
        #Declare function coordinate system
        crs_custom_102 = QgsCoordinateReferenceSystem()
        crs_custom_103 = QgsCoordinateReferenceSystem()
        crs_custom_104 = QgsCoordinateReferenceSystem()
        crs_custom_104_5 = QgsCoordinateReferenceSystem()
        crs_custom_104_75 = QgsCoordinateReferenceSystem()
        crs_custom_105 = QgsCoordinateReferenceSystem()
        crs_custom_105_5 = QgsCoordinateReferenceSystem()
        crs_custom_105_75 = QgsCoordinateReferenceSystem()
        crs_custom_106 = QgsCoordinateReferenceSystem()
        crs_custom_106_25 = QgsCoordinateReferenceSystem()
        crs_custom_106_5 = QgsCoordinateReferenceSystem()
        crs_custom_107 = QgsCoordinateReferenceSystem()
        crs_custom_107_25 = QgsCoordinateReferenceSystem()
        crs_custom_107_5 = QgsCoordinateReferenceSystem()
        crs_custom_107_75 = QgsCoordinateReferenceSystem()
        crs_custom_108 = QgsCoordinateReferenceSystem()
        crs_custom_108_25 = QgsCoordinateReferenceSystem()
        crs_custom_108_5 = QgsCoordinateReferenceSystem()

        #Declare VN2000
        # VN2000 Noi bo mui 3
        # htd_102_nb = "+proj=tmerc +lat_0=0 +lon_0=102 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_103_nb = "+proj=tmerc +lat_0=0 +lon_0=103 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_104_nb = "+proj=tmerc +lat_0=0 +lon_0=104 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_104_5_nb = "+proj=tmerc +lat_0=0 +lon_0=104.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_104_75_nb = "+proj=tmerc +lat_0=0 +lon_0=104.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_105_nb = "+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_105_5_nb = "+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_105_75_nb = "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_106_nb = "+proj=tmerc +lat_0=0 +lon_0=106 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_106_25_nb = "+proj=tmerc +lat_0=0 +lon_0=106.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_106_5_nb = "+proj=tmerc +lat_0=0 +lon_0=106.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_107_nb = "+proj=tmerc +lat_0=0 +lon_0=107 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_107_25_nb = "+proj=tmerc +lat_0=0 +lon_0=107.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_107_5_nb = "+proj=tmerc +lat_0=0 +lon_0=107.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_107_75_nb = "+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_108_nb = "+proj=tmerc +lat_0=0 +lon_0=108 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_108_25_nb = "+proj=tmerc +lat_0=0 +lon_0=108.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        # htd_108_5_nb = "+proj=tmerc +lat_0=0 +lon_0=108.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"

        # VN2000 Hoi nhap mui 3
        htd_102_hn = "+proj=tmerc +lat_0=0 +lon_0=102 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_103_hn = "+proj=tmerc +lat_0=0 +lon_0=103 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_hn = "+proj=tmerc +lat_0=0 +lon_0=104 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_5_hn = "+proj=tmerc +lat_0=0 +lon_0=104_5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_104_75_hn = "+proj=tmerc +lat_0=0 +lon_0=104.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_hn = "+proj=tmerc +lat_0=0 +lon_0=105 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_5_hn = "+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_105_75_hn = "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_hn = "+proj=tmerc +lat_0=0 +lon_0=106 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_25_hn = "+proj=tmerc +lat_0=0 +lon_0=106.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_106_5_hn = "+proj=tmerc +lat_0=0 +lon_0=106.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_hn = "+proj=tmerc +lat_0=0 +lon_0=107 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_25_hn = "+proj=tmerc +lat_0=0 +lon_0=107.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_5_hn = "+proj=tmerc +lat_0=0 +lon_0=107.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_107_75_hn = "+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_hn = "+proj=tmerc +lat_0=0 +lon_0=108 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_25_hn = "+proj=tmerc +lat_0=0 +lon_0=108.25 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"
        htd_108_5_hn = "+proj=tmerc +lat_0=0 +lon_0=108.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,0.00928836,-0.01975479,0.00427372,0.252906278 +units=m +no_defs"

        # Custom CRS 3 degree 7 parameters
        crs_custom_102.createFromProj4(htd_102_hn)
        crs_custom_103.createFromProj4(htd_103_hn)
        crs_custom_104.createFromProj4(htd_104_hn)
        crs_custom_104_5.createFromProj4(htd_104_5_hn)
        crs_custom_104_75.createFromProj4(htd_104_75_hn)
        crs_custom_105.createFromProj4(htd_105_hn)
        crs_custom_105_5.createFromProj4(htd_105_5_hn)
        crs_custom_105_75.createFromProj4(htd_105_75_hn)
        crs_custom_106.createFromProj4(htd_106_hn)
        crs_custom_106_25.createFromProj4(htd_106_25_hn)
        crs_custom_106_5.createFromProj4(htd_106_5_hn)
        crs_custom_107.createFromProj4(htd_107_hn)
        crs_custom_107_25.createFromProj4(htd_107_25_hn)
        crs_custom_107_5.createFromProj4(htd_107_5_hn)
        crs_custom_107_75.createFromProj4(htd_107_75_hn)
        crs_custom_108.createFromProj4(htd_108_hn)
        crs_custom_108_25.createFromProj4(htd_108_25_hn)
        crs_custom_108_5.createFromProj4(htd_108_5_hn)

        # create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for f in layers:
                #VN2000 mui 3 KTT 102
                if f.type() == 0 and htd =="VN2000 mui 3 KTT 102":
                    f.setCrs(crs_custom_102)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)


                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 102":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_102, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                #Theo tọa độ file nguồn
                elif f.type() == 0 and htd =="System":
                    if htd_output == "System":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", f.crs(), "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "UTM Zone 49N - EPGS: 32649":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_49, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)


                    if htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)
                    # ĐƯA VÀO VN2000 HỘI NHẬP
                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 102":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_102, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)			

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 103":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_103, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 104":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_104, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 104.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_104_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 104.75":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_104_75, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)	

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 105":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_105, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 105.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_105_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 105.75":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_105_75, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 106":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_106, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 106.25":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_106_25, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 106.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_106_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 107":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_107, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)


                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.25":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_107_25, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_107_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)


                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.75":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_107_75, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    if htd_output == "VN-2000 Hoi nhap mui 3 KTT 108":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_108, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 108.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_108_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                #VN2000 mui 3 KTT 103
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 103":
                    f.setCrs(crs_custom_103)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 103":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_103, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 104
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 104":
                    f.setCrs(crs_custom_104)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 104":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_104, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                #VN2000 mui 3 KTT 104.5
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 104.5":
                    f.setCrs(crs_custom_104_5)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 104.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_104_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                #VN2000 mui 3 KTT 104.75
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 104.75":
                    f.setCrs(crs_custom_104_75)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 104.75":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_104_75, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)


                # VN2000 mui 3 KTT 105
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 105":
                    f.setCrs(crs_custom_105)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 105":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_105, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 105.5
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 105.5":
                    f.setCrs(crs_custom_105_5)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 105.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_105_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 105.75
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 105.75":
                    f.setCrs(crs_custom_105_75)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 105.75":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_105_75, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)
							
                # VN2000 mui 3 KTT 106
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 106":
                    f.setCrs(crs_custom_106)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 106":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_106, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 106.25
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 106.25":
                    f.setCrs(crs_custom_106_25)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 106.25":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_106_25, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 106.5
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 106.5":
                    f.setCrs(crs_custom_106_5)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 106.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_106_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 107
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 107":
                    f.setCrs(crs_custom_107)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "UTM Zone 49N - EPGS: 32649":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_49, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 107":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_107, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 107.25
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 107.25":
                    f.setCrs(crs_custom_107_25)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "UTM Zone 49N - EPGS: 32649":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_49, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.25":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_107_25, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 107.5
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 107.5":
                    f.setCrs(crs_custom_107_5)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "UTM Zone 49N - EPGS: 32649":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_49, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_107_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 107.75
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 107.75":
                    f.setCrs(crs_custom_107_75)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "UTM Zone 49N - EPGS: 32649":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_49, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 107.75":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_107_75, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 108
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 108":
                    f.setCrs(crs_custom_108)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "UTM Zone 49N - EPGS: 32649":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_49, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 108":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_108, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 108.25
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 108.25":
                    f.setCrs(crs_custom_108_25)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "UTM Zone 49N - EPGS: 32649":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_49, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 108.25":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_108_25, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                # VN2000 mui 3 KTT 108.5
                elif f.type() == 0 and htd =="VN2000 mui 3 KTT 108.5":
                    f.setCrs(crs_custom_108_5)
                    if htd_output == "UTM Zone 48N - EPGS: 32648":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_48, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "UTM Zone 49N - EPGS: 32649":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System", htd_utm_49, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "WGS84 Lat/long - EPGS: 4326":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_4326, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir,0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                    elif htd_output == "VN-2000 Hoi nhap mui 3 KTT 108.5":
                        writer = QgsVectorFileWriter.writeAsVectorFormat(f, output_dir + f.name() + ".shp", "System",crs_custom_108_5, "ESRI Shapefile")
                        if writer == QgsVectorFileWriter.NoError:
                            self.iface.messageBar().pushMessage("File duoc luu:", f.name() + ".shp tai " + output_dir, 0, 2)
                        else:
                            self.iface.messageBar().pushMessage("Loi luu file:", f.name() + ".shp tai " + output_dir, 1, 2)

                else:
                    pass
