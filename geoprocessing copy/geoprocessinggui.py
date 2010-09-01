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
from ui_geoprocessing import Ui_Geoprocessing
import os, sys

class GeoprocessingGui(QDialog, Ui_Geoprocessing):
  
  def __init__(self, parent):
    QDialog.__init__(self, parent)
    self.setupUi(self)
    
     # get the parameters from last session
    self.settings = QSettings("SOGIS","geoprocessing")
    self.savePath = self.settings.value("gui/savepath")
    self.lineEditShapeDir.setText(QString(self.savePath.toString()))
    self.cmbLayerA.setEnabled(False)  
    self.cmbLayerB.setEnabled(False)
    self.lineEditParameter.setEnabled(False)  
    self.lineEditShapeDir.text() 
    self.chkBoxAddShape.setEnabled(False)
    self.chkBoxSelectedFeatures.setEnabled(False)
    self.btnOk.setEnabled(False)
    self.lblItems.setEnabled(False)
    self.label.setEnabled(False)
    self.label_2.setEnabled(False)
    self.label_6.setEnabled(False)    
    
    
#Translation environment    
    userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+"/python/plugins"  
    systemPluginPath = QgsApplication.prefixPath()+"/share/qgis/python/plugins"
    myLocaleName = QLocale.system().name()
    myLocale = myLocaleName[0:2]

    if QFileInfo(userPluginPath).exists():
      pluginPath = userPluginPath+"/geoprocessing/i18n/geoprocessing_"+myLocale+".qm"
    elif QFileInfo(systemPluginPath).exists():
      pluginPath = systemPluginPath+"/geoprocessing/i18n/geoprocessing_"+myLocale+".qm"
    
    
#    QMessageBox.information(None, "Meldung", pluginPath)
   
    self.localePath = pluginPath
    self.translator = QTranslator()
    self.translator.load(self.localePath)       
  
   
  @pyqtSignature("on_btnOk_clicked()")  
  def on_btnOk_clicked(self):
  
    QCoreApplication.installTranslator(self.translator)  
  
    if not os.path.isdir(self.lineEditShapeDir.text()):
        QMessageBox.warning(None, QCoreApplication.translate("Geoprocessing","Error"), QCoreApplication.translate("Geoprocessing","Directory not available"))
    elif self.cmbFunction.currentIndex() == 0:
        QMessageBox.warning(None,  QCoreApplication.translate("Geoprocessing","Error"),  QCoreApplication.translate("Geoprocessing","Select a function"))
    elif self.lineEditParameter.isEnabled() and self.lineEditParameter.text() == "":
        QMessageBox.warning(None, QCoreApplication.translate("Geoprocessing","Error"), QCoreApplication.translate("Geoprocessing","no buffer size selected"))
    else: 
        self.emit(SIGNAL("geoprocessingSignal(QString,QString,QString,QString,int,int,bool,bool)"), 
                          self.cmbLayerA.currentText(),  
                          self.cmbLayerB.currentText(), 
                          self.lineEditParameter.text(),  
                          self.lineEditShapeDir.text(),  
                          self.cmbFunction.currentIndex(), 
                          self.cmbAttribA.currentIndex(),
                          self.chkBoxAddShape.checkState(), 
                          self.chkBoxSelectedFeatures.checkState())
  
  
  @pyqtSignature("on_cmbFunction_currentIndexChanged(int)")
  def on_cmbFunction_currentIndexChanged(self):
    self.emit(SIGNAL("functionChanged(QString)"), self.cmbFunction.currentText())
   
  @pyqtSignature("on_cmbLayerA_currentIndexChanged(int)")
  def on_cmbLayerA_currentIndexChanged(self):
    self.emit(SIGNAL("layerAChanged(QString)"), self.cmbLayerA.currentText())

    
    
  @pyqtSignature("on_btnBrowse_clicked()")    
  def on_btnBrowse_clicked(self):
    self.ShapePath = QFileDialog.getExistingDirectory(self, QApplication.translate("Geoprocessing","Save in:"), self.savePath.toString(), QFileDialog.ShowDirsOnly)
    self.lineEditShapeDir.setText(QString(self.ShapePath))
#    self.settings.setValue("gui/savepath", QVariant(self.ShapePath))

  @pyqtSignature("on_btnExit_clicked()")    
  def on_btnExit_clicked(self):  
    self.close()
    
  @pyqtSignature("on_btnAbout_clicked()")    
  def on_btnAbout_clicked(self):  
    self.emit(SIGNAL("showAbout()"))
      