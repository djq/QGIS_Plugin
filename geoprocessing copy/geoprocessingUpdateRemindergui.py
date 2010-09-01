# -*- coding: latin1 -*-
# /***************************************************************************
#   geoprocessing.py QGIS Geoprocessing Plugin
#  -------------------------------------------------------------------
# Date                 : 22 January 2008
# Copyright            : (C) 2008 by Dr. Horst Duester, Stefan Ziegler
# email                : horst dot duester at bd dot so dot ch
#                      : stefan dot ziegler at bd dot so dot ch
#  ***************************************************************************
#  *                                                                         *
#  *   This program is free software; you can redistribute it and/or modify  *
#  *   it under the terms of the GNU General Public License as published by  *
#  *   the Free Software Foundation; either version 2 of the License, or     *
#  *   (at your option) any later version.                                   *
#  *                                                                         *
#  ***************************************************************************/
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_geoprocessingUpdateReminder import Ui_GeoprocessingUpdateReminder
import os, sys

class GeoprocessingUpdateReminderGui(QDialog, Ui_GeoprocessingUpdateReminder):

  def __init__(self, parent):
    QDialog.__init__(self, parent)
    self.setupUi(self)
    
  @pyqtSignature("on_btnNo_clicked()")  
  def on_btnNo_clicked(self):
    self.close()    