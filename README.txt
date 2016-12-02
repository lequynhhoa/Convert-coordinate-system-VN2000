# Convert-coordinate-system-VN2000
This tool convert map layers (currently open in TOC) to VN2000 coordinate system.

Since the VN2000 coordinate 3 degree need to support 18 different central meridian (from 102 to 108.5) the current default VN2000 in the EPSG is not supporting all the configuration. This tool aim to address this issue.

Supporting use cases:
VN2000 without 7 Bursa-Wolfe parameter to WGS84 Latlong
VN2000 without 7 Bursa-Wolfe parameter to UTM WGS84
VN2000 without 7 Bursa-Wolfe parameter to correct VN2000 (with 7 Bursa-Wolfe parameter)

Dữ liệu bản đồ của hệ thống ngành Lâm nghiệp hầu hết đều đang ở hệ tọa độ VN2000 Nội bộ, lệch với Google earth 230m. Công cụ này cho phép người dùng chuyển hệ tọa độ, defined hệ tọa độ chồng khớp với Google earth sang định dạng shapefile (.shp)

Các chức năng chuyển đổi:
1. Save as sang định dạng .shp giữ nguyên hệ tọa độ đầu vào
2. Chuyển hệ tọa độ VN2000 Nội bộ sang WGS84 Latlong
3. Chuyển hệ tọa độ VN2000 Nội bộ sang UTM
4. Chuyển hệ tọa độ VN2000 Nội bộ sang VN2000 Hội nhập


Plugin Builder Results

Your plugin ConvertprjBatch was created in:
    C:\Users\HOA-PC\.qgis2\python\plugins\ConvertprjBatch

Your QGIS plugin directory is located at:
    C:/Users/HOA-PC/.qgis2/python/plugins

What's Next:

  * Copy the entire directory containing your new plugin to the QGIS plugin
    directory

  * Compile the resources file using pyrcc4

  * Run the tests (``make test``)

  * Test the plugin by enabling it in the QGIS plugin manager

  * Customize it by editing the implementation file: ``Convertprj.py``

  * Create your own custom icon, replacing the default icon.png

  * Modify your user interface by opening ConvertprjBatch.ui in Qt Designer

  * You can use the Makefile to compile your Ui and resource files when
    you make changes. This requires GNU make (gmake)

For more information, see the PyQGIS Developer Cookbook at:
http://www.qgis.org/pyqgis-cookbook/index.html

(C) 2011-2014 GeoApt LLC - geoapt.com
Git revision : $Format:%H$
