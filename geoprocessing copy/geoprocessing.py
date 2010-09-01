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
from PyQt4 import QtXml
from geoprocessinggui import GeoprocessingGui
import os,sys,urllib

import resources

class Geoprocessing:
  def __init__(self, iface):
        
    # save reference to the QGIS interface
    self.iface = iface 
    self.QgisVersion = str(QGis.QGIS_VERSION)
    
    userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+"/python/plugins/geoprocessing"  
    systemPluginPath = QgsApplication.prefixPath()+"/share/qgis/python/plugins/geoprocessing"
    myLocaleName = QLocale.system().name()
    myLocale = myLocaleName[0:2]
    
    
    if QFileInfo(userPluginPath).exists():
      pluginPath = userPluginPath+"/i18n/geoprocessing_"+myLocale+".qm"
    elif QFileInfo(systemPluginPath).exists():
      pluginPath = systemPluginPath+"/i18n/geoprocessing_"+myLocale+".qm"

    self.localePath = pluginPath
    if QFileInfo(self.localePath).exists():
      self.translator = QTranslator()
      self.translator.load(self.localePath)
      if qVersion() > '4.3.3':        
        QCoreApplication.installTranslator(self.translator)

# Error Messages
    self.topoErrorMessage = QCoreApplication.translate("Geoprocessing","Resulting Geometry is not valid due to topology errors "
                                                      +"caused by invalid input geometries or GEOS topology exceptions during process!\n\n"
                                                      +"The resulting geometry probably will not show the correct results.\n"
                                                      +"Try to clean your input geometries.")
                                                      
    self.versionMessage = QCoreApplication.translate("Geoprocessing","Quantum GIS version detected: "+str(self.QgisVersion)+"\n"
                                                                    +"Geoprocessing plugin requires version at least 1.0.0!\n"
                                                                    +"Plugin not loaded.")                                                      
       
          

  def initGui(self):

# check Qgis Version
    
    
    if int(self.QgisVersion[0]) < 1:
      if (int(self.QgisVersion[2]) >= 7 and int(self.QgisVersion[2]) <= 9): 
        QMessageBox.warning(None, "Version", self.versionMessage)
        return 1

  
    # create action that will start plugin configuration
    self.actionGeoprocessing = QAction(QIcon(":/plugins/geoprocessing/icon_buffer.xpm"), QCoreApplication.translate("Geoprocessing","Geoprocessing Tool"), self.iface.mainWindow())    
    QObject.connect(self.actionGeoprocessing, SIGNAL("triggered()"), self.run_geoprocessing_ctrl)

    # Create about button
    #self.aboutaction = QAction(QIcon(":/plugins/geoprocessing/about.png"), "About", self.iface.mainWindow())
    #self.aboutaction.setWhatsThis("About Geoprocessing")
    #QObject.connect(self.aboutaction, SIGNAL("activated()"), self.about)
        
    # add toolbar buttons
    self.toolbar = self.iface.addToolBarIcon(self.actionGeoprocessing)
    self.iface.addPluginToMenu("&Geoprocessing", self.actionGeoprocessing)
    #self.iface.addPluginToMenu("Geoprocessing", self.aboutaction)    
    
         

  def about(self):
	infoString = QString(QCoreApplication.translate("Geoprocessing","Population Density Gradient Plugin\n"
                     + "The Plugin provides a standardized way to analyze the population density gradient of cities.\n"
                     + "Author: David Quinn\n"
                     + "Mail: djq@mit.edu"))
  
	QMessageBox.information(self.iface.mainWindow(), "About PopDenGradient",infoString)    

  def unload(self):
    # remove the toolbar and the menu
    self.iface.removePluginMenu("&Geoprocessing", self.actionGeoprocessing)
    self.iface.removeToolBarIcon(self.actionGeoprocessing)    
    
  def run_geoprocessing_ctrl(self):
    self.geo_ctrl = GeoprocessingGui(self.iface.mainWindow())
    QObject.connect(self.geo_ctrl, SIGNAL("geoprocessingSignal(QString, QString, QString, QString, int, int, bool, bool)"), self.geoprocessing)
    QObject.connect(self.geo_ctrl, SIGNAL("functionChanged(QString)"), self.manageGui)
    QObject.connect(self.geo_ctrl, SIGNAL("layerAChanged(QString)"), self.addSpecialAttributes)
    QObject.connect(self.geo_ctrl, SIGNAL("layerAChanged(QString)"), self.checkBtnOK)            
    QObject.connect(self.geo_ctrl, SIGNAL("showAbout()"), self.about)            
    
    self.geo_ctrl.show()

  def isValidGeometry(self, fet):
    try:              
      if fet.geometry().wkbSize() > 0:
        return True        
    except:
      if self.message == False:
        QMessageBox.warning(None, QCoreApplication.translate("Geoprocessing","Error"), self.topoErrorMessage)
        self.message = True                 
      return False
    
  def writerErrorMessage(self, errorNum):
    if errorNum == 1:
      return QCoreApplication.translate("Geoprocessing","Driver not found")
    elif errorNum == 2:
      return QCoreApplication.translate("Geoprocessing","Error while creating datasource")
    elif errorNum == 3:
      return QCoreApplication.translate("Geoprocessing","Error while creating layer")
    elif errorNum == 4:
      return QCoreApplication.translate("Geoprocessing","Input layer has not supported column types")
        
  def checkBtnOK(self, lyerName):
     if self.geo_ctrl.cmbLayerA.currentIndex() > 0:
        self.geo_ctrl.btnOk.setEnabled(True)
     
     return 0     
     
# Add Attributes of Layer A to the non working Item Attribute chkBox for Buffer-Item and Dissolve Item
#TODO apply this functionality
  def addSpecialAttributes(self, layerName):
     if self.geo_ctrl.cmbLayerA.currentIndex() > 0 and self.geo_ctrl.cmbFunction.currentIndex()==4:
       vLayer = self.getVectorLayerByName(layerName)
       self.geo_ctrl.cmbAttribA.clear()  
       itemList = []
       itemList.append(QCoreApplication.translate("Geoprocessing","select an Item"))    
       self.geo_ctrl.cmbAttribA.addItems(itemList)
       self.geo_ctrl.cmbAttribA.addItems(self.getFieldNames(vLayer))
       self.geo_ctrl.cmbAttribA.setEnabled(True)
     return 0


# Dynamic configuration of geoprocessing GUI    
# Buffer           => 1      
# Convex Hull      => 2
# Difference A - B => 3
# Dissolve         => 4      
# Intersection     => 5      
# Union            => 6
# SymDifference    => 99      
      
 
  def manageGui(self, myFunction):
    self.geo_ctrl.chkBoxSelectedFeatures.setText(QCoreApplication.translate("Geoprocessing","Dissolve Buffer Result"))
    self.geo_ctrl.label_6.setText(QCoreApplication.translate("Geoprocessing","Maximum Radius [km]:"))
    self.geo_ctrl.lblItems.setText(QCoreApplication.translate("Geoprocessing","Buffer Item"))          
    self.geo_ctrl.lblItems.setEnabled(False)
    self.geo_ctrl.label_6.setEnabled(False)

    if self.geo_ctrl.cmbFunction.currentIndex() == 1:
        self.geo_ctrl.label_2.setEnabled(True)    
        self.geo_ctrl.cmbLayerA.setEnabled(True)
        self.geo_ctrl.label_6.setEnabled(True) 
        self.geo_ctrl.lblItems.setEnabled(False)
        self.geo_ctrl.lineEditParameter.setEnabled(True)                
        self.geo_ctrl.label.setEnabled(False)        
        self.geo_ctrl.cmbLayerB.setEnabled(False)                
        self.geo_ctrl.cmbAttribA.setEnabled(True)        
        self.geo_ctrl.chkBoxSelectedFeatures.setEnabled(True)
        self.geo_ctrl.chkBoxAddShape.setEnabled(True)
        self.geo_ctrl.label_3.setEnabled(True)          
        self.geo_ctrl.lineEditShapeDir.setEnabled(True)         
        self.geo_ctrl.btnBrowse.setEnabled(True)   
    elif self.geo_ctrl.cmbFunction.currentIndex() == 4:
        self.geo_ctrl.label_2.setEnabled(True)    
        self.geo_ctrl.cmbLayerA.setEnabled(True)
        self.geo_ctrl.label_6.setEnabled(False)
        self.geo_ctrl.lineEditParameter.setEnabled(False)                
        self.geo_ctrl.label.setEnabled(False)        
        self.geo_ctrl.cmbLayerB.setEnabled(False)
        self.geo_ctrl.lblItems.setEnabled(True)         
        self.geo_ctrl.lblItems.setText(QCoreApplication.translate("Geoprocessing","Dissolve Item"))       
        self.geo_ctrl.cmbAttribA.setEnabled(True)        
        self.geo_ctrl.chkBoxSelectedFeatures.setEnabled(False)
        self.geo_ctrl.chkBoxAddShape.setEnabled(True)
    elif self.geo_ctrl.cmbFunction.currentIndex() == 2:
        self.geo_ctrl.label_2.setEnabled(True)    
        self.geo_ctrl.cmbLayerA.setEnabled(True)
        self.geo_ctrl.label_6.setEnabled(False)
        self.geo_ctrl.lineEditParameter.setEnabled(False)                
        self.geo_ctrl.label.setEnabled(False)      
        self.geo_ctrl.cmbLayerB.setEnabled(False)
        self.geo_ctrl.lblItems.setEnabled(False)         
        self.geo_ctrl.cmbAttribA.setEnabled(False)        
        self.geo_ctrl.chkBoxSelectedFeatures.setEnabled(False)
        self.geo_ctrl.chkBoxAddShape.setEnabled(True)
    elif self.geo_ctrl.cmbFunction.currentIndex() == 3:
        self.geo_ctrl.label_2.setEnabled(True)    
        self.geo_ctrl.cmbLayerA.setEnabled(True)
        self.geo_ctrl.label_6.setEnabled(False)
        self.geo_ctrl.lineEditParameter.setEnabled(False)                
        self.geo_ctrl.label.setEnabled(True)        
        self.geo_ctrl.cmbLayerB.setEnabled(True)
        self.geo_ctrl.lblItems.setEnabled(False)         
        self.geo_ctrl.cmbAttribA.setEnabled(False)        
        self.geo_ctrl.chkBoxSelectedFeatures.setEnabled(False)
        self.geo_ctrl.chkBoxAddShape.setEnabled(True)
    else: 
        self.geo_ctrl.label_2.setEnabled(True)    
        self.geo_ctrl.cmbLayerA.setEnabled(True)
        self.geo_ctrl.label_6.setEnabled(False)
        self.geo_ctrl.label.setEnabled(True)        
        self.geo_ctrl.cmbLayerB.setEnabled(True)
        self.geo_ctrl.lblItems.setEnabled(False)         
        self.geo_ctrl.cmbAttribA.setEnabled(True)        
        self.geo_ctrl.lineEditParameter.setEnabled(False)
        self.geo_ctrl.chkBoxSelectedFeatures.setEnabled(False)
        self.geo_ctrl.chkBoxAddShape.setEnabled(True)
        self.geo_ctrl.label_3.setEnabled(True)          
        self.geo_ctrl.btnOk.setEnabled(False)     
        
    self.geo_ctrl.label_3.setEnabled(True)          
    self.geo_ctrl.lineEditShapeDir.setEnabled(True)         
    self.geo_ctrl.btnBrowse.setEnabled(True)           
    self.geo_ctrl.chkBoxAddShape.setEnabled(True)
    self.geo_ctrl.cmbAttribA.setEnabled(False)    
    
    myListA = []
    myListB = []
    self.geo_ctrl.cmbLayerA.clear()
    self.geo_ctrl.cmbLayerB.clear() 
        
    if self.geo_ctrl.cmbFunction.currentIndex()==5:
      myListA = self.getLayerNames("all")    
      myListB = self.getLayerNames("Polygon")    
    elif self.geo_ctrl.cmbFunction.currentIndex()==7:
      myListA = self.getLayerNames("all")
      myListB = self.getLayerNames("all")    
    elif self.geo_ctrl.cmbFunction.currentIndex()==3:
      myListA = self.getLayerNames("Polygon")
      myListB = self.getLayerNames("Polygon")    
    elif self.geo_ctrl.cmbFunction.currentIndex()==6:
      myListA = self.getLayerNames("Polygon")
      myListB = self.getLayerNames("Polygon")    
    elif self.geo_ctrl.cmbFunction.currentIndex()==99:
      myListA = self.getLayerNames("Polygon")
      myListB = self.getLayerNames("Polygon")              
    elif self.geo_ctrl.cmbFunction.currentIndex()==4:
      myListA = self.getLayerNames("Polygon")
      myListB = self.getLayerNames("Polygon")
      self.geo_ctrl.cmbAttribA.clear()                    
    else:    
      myListA = self.getLayerNames("all")    
      myListB = self.getLayerNames("all")    
    
    emptyString = []
    emptyString.append("---------")   
    self.geo_ctrl.cmbLayerA.addItems(emptyString)
    self.geo_ctrl.cmbLayerB.addItems(emptyString)
    self.geo_ctrl.cmbLayerA.addItems(myListA)
    self.geo_ctrl.cmbLayerB.addItems(myListB)

    
    return 0        
  

  def geoprocessing(self,  myLayerA,  myLayerB,  myParam,  myPath,  myFunction, attribID, myBool, mergeBool):

# Difference A - B    
    if myFunction == 3:
      self.difference(myLayerA,  myLayerB,  myPath,  myBool)
# Buffer      
    elif myFunction == 1:    
      self.buffering(myLayerA,  myParam,  myPath, myBool, mergeBool)
# Intersection      
    elif myFunction == 5:    
      self.intersection(myLayerA,  myLayerB,  myPath,  myBool)
# SymDifference      
    elif myFunction == 99:    
      self.symDifference(myLayerA,  myLayerB,  myPath,  myBool)
# Union      
    elif myFunction == 6:    
      self.union(myLayerA,  myLayerB,  myPath,  myBool)
# Convex Hull      
    elif myFunction == 2:    
      self.convexHull(myLayerA,  myPath,  myBool)
# Dissolve      
    elif myFunction == 4:    
      self.dissolve(myLayerA,  myPath,  myBool, attribID)
# Merge equal structured Layer      
    elif myFunction == 7:    
      self.merge(myLayerA,  myLayerB, myPath, myBool)

      
      
#Preparation of the Union Process
#TODO: union is not working until now but can be substituted by intersection      
  def union(self, myLayerA,  myLayerB,  myPath,  myBool):
    vlayerA = self.getVectorLayerByName(myLayerA)
    vlayerB = self.getVectorLayerByName(myLayerB)      
    
    fieldList = self.mergeFields(vlayerA, vlayerB)
    
    shapeFilePath = self.createShapeFileName(vlayerA, myPath, "union", )    
    writer = self.createShapeFileWriter(shapeFilePath, fieldList, vlayerA.dataProvider().geometryType())

    
            
    if writer==0:
      return 0      
      
    resultList = self.makeUnion(vlayerA, vlayerB)   

    for fet in resultList:
      writer.addFeature(fet)
#      mLayer.addFeature(fet)     
      
    del writer
            # add the new Shape to the map canvas
    if myBool:
      self.addShapeToCanvas(shapeFilePath)

    self.geo_ctrl.close()
        
  def merge(self, myLayerA,  myLayerB,  myPath,  myBool):
    vlayerA = self.getVectorLayerByName(myLayerA)
    vlayerB = self.getVectorLayerByName(myLayerB)      
    
    fieldList = self.getFieldList(vlayerA)
    
    shapeFilePath = self.createShapeFileName(vlayerA, myPath, "merge", )    
    writer = self.createShapeFileWriter(shapeFilePath, fieldList, vlayerA.dataProvider().geometryType())        
    if writer==0:
      return 0      

    resultList = self.makeMerge(vlayerA, vlayerB)   

    for fet in resultList:
      writer.addFeature(fet)     
      
    del writer
            # add the new Shape to the map canvas
    if myBool:
      self.addShapeToCanvas(shapeFilePath)

    self.geo_ctrl.close()

    
  def intersection(self, myLayerA,  myLayerB,  myPath,  myBool, virtual=False):

    vlayerA = self.getVectorLayerByName(myLayerA)
    vlayerB = self.getVectorLayerByName(myLayerB)      
    
    fieldList = self.mergeFields(vlayerA, vlayerB)
    
    shapeFilePath = self.createShapeFileName(vlayerA, myPath, "intersection", )    
    writer = self.createShapeFileWriter(shapeFilePath, fieldList, vlayerA.dataProvider().geometryType())        
    if writer==0:
      return 0      

    resultList = self.makeIntersection(vlayerA, vlayerB)    

    for fet in resultList:
      writer.addFeature(fet)        
          # delete the writer to flush features to disk (optional)
    del writer

            # add the new Shape to the map canvas        
    if myBool:
      self.addShapeToCanvas(shapeFilePath)
        
    self.geo_ctrl.close()        


  def convexHull(self, myLayer,  myPath,  myBool):
    vlayer = self.getVectorLayerByName(myLayer)
    provider = vlayer.dataProvider()
    feat = QgsFeature()
    allAttrs = provider.attributeIndexes()
        
    provider.select(allAttrs)
    shapeFilePath = self.createShapeFileName(vlayer, myPath, "convexHull", )

    fieldList = self.getFeatureList(vlayer)
    writer = self.createShapeFileWriter(shapeFilePath, fieldList, QGis.WKBPolygon)
    if writer==0:
      return 0      
    
#    while provider.getNextFeature(feat):
    hullGeo = self.singleToMulti(vlayer)
    hullResult = hullGeo.convexHull()            

    fet = QgsFeature()
    fet.setGeometry(hullResult)
    fet.addAttribute(0, QVariant(1))
    writer.addFeature(fet)


    # delete the writer to flush features to disk (optional)
    del writer

    # add the new Shape to the map canvas
    if myBool:
      self.addShapeToCanvas(shapeFilePath)
    
    self.geo_ctrl.close()


  def dissolve(self, myLayerA,  myPath,  myBool, attribID=0, virtual=False):

    attribName = self.geo_ctrl.cmbAttribA.itemText(attribID)
    
    vlayerA = self.getVectorLayerByName(myLayerA)
    fieldList = self.getFeatureList(vlayerA) 
    
#    mLayer = self.createMemoryLayer("POLYGON","test",fieldList)
    
    shapeFilePath = self.createShapeFileName(vlayerA, myPath, "dissolve", )    
    writer = self.createShapeFileWriter(shapeFilePath, fieldList, vlayerA.dataProvider().geometryType())        
    if writer==0:
      return 0      
 
    nFeat = vlayerA.dataProvider().featureCount()
    self.nElement = 0
    self.geo_ctrl.progressBar.setValue(0)
    self.geo_ctrl.progressBar.setRange(0, nFeat) 
 
    if attribID > 0:  
      featureList = self.getFeatureList(vlayerA)
      fieldID = vlayerA.dataProvider().fieldNameIndex(attribName)
      attribValueList = self.getUniqueAttributeValues(vlayerA, fieldID)
    
      for attr in attribValueList:
        dissResult = self.makeDissolve(vlayerA, fieldID, attr)  
      
        for fet in dissResult:
          writer.addFeature(fet)
    else:  
      dissResult = self.makeDissolve(vlayerA)  
    
      for fet in dissResult:
        writer.addFeature(fet)
        
          # delete the writer to flush features to disk (optional)
    del writer

            # add the new Shape to the map canvas        
    if myBool:
      self.addShapeToCanvas(shapeFilePath)
        
    self.geo_ctrl.close()
    
        
 
  def difference(self, myLayerA,  myLayerB,  myPath,  myBool):

    vlayerA = self.getVectorLayerByName(myLayerA)
    vlayerB = self.getVectorLayerByName(myLayerB)      
    
    self.mergeFields(vlayerA, vlayerB)
    fieldList = self.getFeatureList(vlayerA) 
    
    shapeFilePath = self.createShapeFileName(vlayerA, myPath, "difference", )    
    writer = self.createShapeFileWriter(shapeFilePath, fieldList, vlayerA.dataProvider().geometryType())        
    if writer==0:
      return 0      

    diffResult = self.makeDifference(vlayerA, vlayerB)            
    
    for fet in diffResult:
      writer.addFeature(fet)
    
          # delete the writer to flush features to disk (optional)
    del writer

            # add the new Shape to the map canvas
    if myBool:
      self.addShapeToCanvas(shapeFilePath)
        
    self.geo_ctrl.close()
    
    
#TODO is not working until now    
  def symDifference(self, myLayerA,  myLayerB,  myPath,  myBool):

    vlayerA = self.getVectorLayerByName(myLayerA)
    vlayerB = self.getVectorLayerByName(myLayerB)
            
    fieldList = self.getFeatureList(vlayerA)
    
    shapeFilePath = self.createShapeFileName(vlayerA, myPath, "symdifference", )    
    writer = self.createShapeFileWriter(shapeFilePath, fieldList, vlayerA.dataProvider().geometryType())        
    if writer==0:
      return 0      

    self.makeSymDifference(writer,vlayerA, vlayerB)
      

          # delete the writer to flush features to disk (optional)
    del writer

            # add the new Shape to the map canvas
    if myBool:
      self.addShapeToCanvas(shapeFilePath)
        
    self.geo_ctrl.close()
    
  def buffering(self,  myLayer,  bufferDistance, myPath,  myBool, mergeBool):    
    vlayer = self.getVectorLayerByName(myLayer)
    provider = vlayer.dataProvider()
    
    fieldList = self.getFeatureList(vlayer)
    allAttrs = provider.attributeIndexes()
    provider.select(allAttrs)

    shapeFilePath = self.createShapeFileName(vlayer, myPath, "buffer", )

    if mergeBool or self.geo_ctrl.cmbAttribA.currentIndex() > 0:
      writer = self.createShapeFileWriter(shapeFilePath, fieldList, QGis.WKBMultiPolygon)
      if writer==0:
        return 0      
    else:
      writer = self.createShapeFileWriter(shapeFilePath, fieldList, QGis.WKBPolygon)          
      if writer==0:
        return 0      
    
    bufferResult = self.makeBuffer(provider, mergeBool, bufferDistance)
    
    for fet in bufferResult:
      writer.addFeature(fet)
      
    # delete the writer to flush features to disk (optional)
    del writer

    # add the new Shape to the map canvas
    if myBool:
      self.addShapeToCanvas(shapeFilePath)
            
    self.geo_ctrl.close()
    
    
    return 0
    
#  def createMemoryLayer(layerType, layerName, fieldList):
  
    # create layer
#    vl = QgsVectorLayer(layerType, layerName, "memory")
#    pr = vl.getDataProvider()
    
    # add fields
    # to preserve correct order they must be added one-by-one (d'oh)
#    print fieldList
#    return 0
#    for att in fieldList:
#      pr.addAttributes( att )
  
#    return vl
    
    
#Gets Layernames from canvas
#Return: List of Layernames    
  def getLayerNames(self, vectorType):
    mc=self.iface.mapCanvas()
    nLayers=mc.layerCount()
    layerNamesList = []
    
    if vectorType=="all":
      myType=0
    elif vectorType=="Polygon":
      myType=2
        
    for l in range(nLayers):
        layer = mc.layer(l)
        if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() >= myType and not layer.name() in layerNamesList:
          layerNamesList.append(unicode(layer.name(),'latin1'))
            
    return layerNamesList
                
# Gets Vector Layer by Layername in canvas
#Return: QgsVectorLayer            
  def getVectorLayerByName(self, myName):
    mc=self.iface.mapCanvas()
    nLayers=mc.layerCount()
    for l in range(nLayers):
        layer = mc.layer(l)
        if layer.name() == unicode(myName,'latin1'):
            if(unicode(layer.source(),'latin1').lower().find("host=") > 0):
                # it's a postgis-layer 
                providerName = "postgres"            
            elif(unicode(layer.source(),'latin1').lower().find(".shp") > 0):
                # it's a shape-layer
                providerName = "ogr"
            else:
                QMessageBox.error(None, "Meldung", "Kein Provider gefunden!")
                # wie schliess ich hier eben das Plugin generisch?             
            vlayer = QgsVectorLayer(unicode(layer.source(),'latin1'),  unicode(myName,'latin1'),  providerName)
            if vlayer.isValid():
              return vlayer
            else:
               QMessageBox.warning(None, QCoreApplication.translate("Geoprocessing",vlayer.name()+" is not valid -> exit plugin!"))


#Creates ShapeFileName
#Return: Full Path with Shape Name    
  def createShapeFileName(self, layer, myPath, process):
    if myPath[-1] == "/": 
      myPath = myPath
    else:
      myPath = myPath + "/"     

    i = 1 
    myTempShape = str(myPath) + process + str(i) + ".shp"
       
    while os.path.isfile(unicode(myTempShape,'latin1')):
        i  = i + 1
        myTempShape = str(myPath) + process + str(i) + ".shp"
        
    return myTempShape
      
#Creates a QgsVectorFileWriter for shape
#Return: QgsVectorFileWriter
  def createShapeFileWriter(self, myTempShape, fields, geometryType):
    
    writer = QgsVectorFileWriter(str(myTempShape), "UTF-8", fields, geometryType, None)
    if writer.hasError() != QgsVectorFileWriter.NoError:
      message = self.writerErrorMessage(writer.hasError())
      QMessageBox.warning(None, QCoreApplication.translate("Geoprocessing","Buffer"), str(message))
      return 0
    return writer

#Creates a Spatial Index
#Return: QgsSpatialIndex    
  def createIndex(self, provider):
    feat = QgsFeature()
    index = QgsSpatialIndex()
    while provider.nextFeature(feat):
        index.insertFeature(feat)
    return index 
    
    
#Merges single Geometries to one Multi Geometry    
#Return: QgsGeometry
  def singleToMulti(self, vlayerA):
    provider = vlayerA.dataProvider()
    feat = QgsFeature()
    allAttrs = provider.attributeIndexes()
    provider.select(allAttrs)
    j = 1
    k= 1
    
    geom_array = []
    
    while provider.nextFeature(feat):
        geom = feat.geometry()
        multi_geom = QgsGeometry()
        if geom.type() == 0:
            geom_array.append(geom.asPoint())  
            if geom.isMultipart():
                multi_geom = geom.asMultiPoint()
                for i in multi_geom:
                    geom_array.append(i)
            else:
                geom_array.append(geom.asPoint())   
            
        elif geom.type() == 1:
            if geom.isMultipart():
                multi_geom = geom.asMultiPolyline()
                for i in multi_geom:
                    geom_array.append(i)
            else:
                geom_array.append(geom.asPolyline())   
                
        elif geom.type() == 2:
            if geom.isMultipart():
                multi_geom = geom.asMultiPolygon()
                for i in multi_geom:
                    geom_array.append(i)
            else:
                geom_array.append(geom.asPolygon())           

        else:
            QMessageBox.error(None, "Info", QCoreApplication.translate("Geoprocessing","unknown"))   

        
    if geom.type() == 0:
      return QgsGeometry.fromMultiPoint(geom_array)
    elif geom.type() == 1:       
      return QgsGeometry.fromMultiPolyline(geom_array)
    elif geom.type() == 2:       
      return QgsGeometry.fromMultiPolygon(geom_array)    
          

#Adds a path qualified Shape to canvas
#Return: void  
  def addShapeToCanvas(self, shapeFilePath):
      shapeFilePathList = shapeFilePath.split("/")
      layerName = shapeFilePathList[len(shapeFilePathList)-1]
      vlayer_new = QgsVectorLayer(shapeFilePath, layerName, "ogr")
  
      if vlayer_new.isValid():
        QgsMapLayerRegistry.instance().addMapLayer(vlayer_new)
        return 0
      else:   
        # vlayer_new is not valid -> exit plugin!
        return 1
      

     

#Gets the result geometry Type
#Return: QGis::WKBTYPE    
  def getResultGeometryType(self, vlayerA, vlayerB):
    providerA = vlayerA.dataProvider()
    providerB = vlayerB.dataProvider()   

    featA = QgsFeature()
    featB = QgsFeature()    
    allAttrsA = providerA.attributeIndexes()
    allAttrsB = providerB.attributeIndexes()    

    providerA.select(allAttrsA)
    providerB.select(allAttrsB)    
    
    providerA.nextFeature(featA)
    providerB.nextFeature(featB)    
    
    geomA = featA.geometry()
    geomB = featB.geometry()    
    
    if geomA.type() == QGis.Line:
      return providerA.geometryType()
    else:
      return providerB.geometryType()
      
#Get the Fieldnames of a Vector Layer
#Return: List of Fieldnames
  def getFieldNames(self, vLayer):
    provider = vLayer.dataProvider()      
    myList = self.getFeatureList(vLayer)

    fieldList = []    
    for (k,attr) in myList.iteritems():
       fieldList.append(unicode(attr.name(),'latin1'))

    return fieldList

#Get the List of Fields
#Return: QGsFieldMap
  def getFieldList(self, vlayer):
    fProvider = vlayer.dataProvider()

    feat = QgsFeature()
    allAttrs = fProvider.attributeIndexes()

# start data retrieval: all attributes for each feature
    fProvider.select(allAttrs, QgsRectangle(), False)

# retrieve every feature with its attributes
    myFields = fProvider.fields()
      
    return myFields
    

#Get the Features of a vector Layer
#Return: QgsFieldMap       
  def getFeatureList(self, vlayer):
    fProvider = vlayer.dataProvider()

    feat = QgsFeature()
    allAttrs = fProvider.attributeIndexes()

# start data retrieval: fetch all attributes for each feature
    fProvider.select(allAttrs, QgsRectangle(), False)

# retrieve every feature with its attributes
    myFields = fProvider.fields()
      
    return myFields
    
       
#Merges the Fields of two Vector Layer and adds a_ to the fieldnames of Layer A
#and adds b_ to the fieldnames of Layer B        
#Return: Sequence of Fieldnames
  def mergeFields(self, vlayerA, vlayerB):
    providerB = vlayerB.dataProvider()      
    
    myListA = self.getFeatureList(vlayerA)
    myListB = self.getFeatureList(vlayerB)
    
    maxAId = 0

    for (k,attr) in myListA.iteritems():
      if k > maxAId:
        maxAId = k
            
    for (k,attr) in myListA.iteritems():
       attr.setName("a_"+attr.name())
       
    for (k,attr) in myListB.iteritems():
       attr.setName("b_"+attr.name())
      
    for (k,attr) in myListB.iteritems():
      maxAId += 1
      myListA.update({int(maxAId):attr}) 
                
    return myListA  

    
#Merges the Attributes of two Vector Layer       
#Return: Sequence of Attribute values
  def mergeAttributes(self, attA, attB):
        
    myAttribs = {}
    maxAId = 0
    
    for (k,attr) in attA.iteritems():
      myAttribs.update({int(k):attr})
      if k > maxAId:
        maxAId = k
                
    for (k,attr) in attB.iteritems():
      maxAId += 1
      myAttribs.update({int(maxAId):attr})  
      
    return myAttribs
    
# Gets the list of unique attribute values
#Return List of unique Attribute Values    
  def getUniqueAttributeValues(self,vlayer, fieldID):
    myProvider = vlayer.dataProvider()
    feat = QgsFeature()
    attribList = []
    while myProvider.nextFeature(feat):
      attrs = feat.attributeMap()
      if attribList.count(attrs[fieldID].toString()) == 0:
        attribList.append(attrs[fieldID].toString())

    return attribList    
    
#Detect the number of all involved objects for later use
#with progressbar
#Return: Number of involved features (int)    
  def getNumFeatures(self, providerA, providerB):
    tmpIndexA = self.createIndex(providerA)
    tmpIntersectsA = tmpIndexA.intersects(vlayerB.extent())
    tmpIndexB = self.createIndex(providerB)
    tmpIntersectsB = tmpIndexB.intersects(vlayerA.extent())
    nFeat = len(tmpIntersectsA) + len(tmpIntersectsB)
    
    return nFeat    
    

  def makeBuffer(self, provider, mergeBool, bufferDistance): 
    first = True
    feat = QgsFeature()
    nFeat = provider.featureCount()
    
    self.geo_ctrl.progressBar.setValue(0)
    self.geo_ctrl.progressBar.setRange(0, nFeat)
    
    nElement = 0
    featureList=[]
    
    if mergeBool or self.geo_ctrl.cmbAttribA.currentIndex() > 0:
      while provider.nextFeature(feat):
        buff_geom = feat.geometry().buffer(float(bufferDistance),5)
        if first:
          unionBuff = buff_geom
          first = False
          nElement += 1  
          self.geo_ctrl.progressBar.setValue(nElement)  
        else: 
          unionBuff = unionBuff.combine(buff_geom)
          nElement += 1  
          self.geo_ctrl.progressBar.setValue(nElement)  
          
      fet = QgsFeature()
      fet.setGeometry(unionBuff)
      fet.addAttribute(0, QVariant(1))
      featureList.append(fet)      
    else:          
      while provider.nextFeature(feat):
        geom = feat.geometry()
        buff_geom = geom.buffer(float(bufferDistance),10)           
        nElement += 1  
        self.geo_ctrl.progressBar.setValue(nElement)              
        fet = QgsFeature()
        fet.setGeometry(buff_geom)
        fet.addAttribute(0, QVariant(1))
        
        featureList.append(fet)

    return featureList     


  def makeUnion(self, vlayerA, vlayerB):
    providerA = vlayerA.dataProvider()
    providerB = vlayerB.dataProvider()  
    
    featA = QgsFeature()
    featB = QgsFeature()
        
    allAttrsA = providerA.attributeIndexes()
    allAttrsB = providerB.attributeIndexes()    
        
    providerA.select(allAttrsA)
    providerB.select(allAttrsB)       
        
    index = self.createIndex(providerB)  
    
    first = True
    
    unionResult = self.makeIntersection(vlayerA, vlayerB)
    diffAResult = self.makeDifference(vlayerA, vlayerB)
    diffBResult = self.makeDifference(vlayerB, vlayerA)    


# Get and merge all attributes of Layer A    
    for fet in diffAResult:
      attA = fet.attributeMap()
      myAttribs = {}
      maxId = 0
      for (k,attr) in attA.iteritems():
        if k > maxId:
          maxId = k
        myAttribs.update({int(k):attr})
        
      attB = self.getFeatureList(vlayerB)

# Fill up all Layer B Attributes with dummy values           
      for (k,attr) in attB.iteritems():
        maxId += 1
        myAttribs.update({int(maxId):QVariant(0)})      

      fet.setAttributeMap(myAttribs)      
      unionResult.append(fet)

# Fill up all Layer A Attributes with dummy values    
    for fet in diffBResult:
      attA = self.getFeatureList(vlayerA)
      myAttribs = {}
      maxId = 0
      for (k,attr) in attA.iteritems():
        if k > maxId:
          maxId = k      
        myAttribs.update({int(k):QVariant(0)})     
          
# Get and merge all Layer B Attribute values
      attB = fet.attributeMap()    
      for (k,attr) in attB.iteritems():
        maxId += 1 
        myAttribs.update({int(maxId):attr})

      fet.setAttributeMap(myAttribs)        
      unionResult.append(fet)
        
    return unionResult
    
  def makeDifference(self, vlayerA, vlayerB):

    providerA = vlayerA.dataProvider()
    providerB = vlayerB.dataProvider()  
    
    featA = QgsFeature()
    featB = QgsFeature()
        
    allAttrsA = providerA.attributeIndexes()
    allAttrsB = providerB.attributeIndexes()    

#select only to the intersection square of the bounding boxes of Layer A
    providerA.select(allAttrsA) 
    providerB.select(allAttrsB, vlayerA.extent())       
        
    index = self.createIndex(providerB)
    
    resultList = []
    
    self.message = False
    
    while providerA.nextFeature(featA):
      geomA = featA.geometry()
      attribA = featA.attributeMap()

      intersects = index.intersects(geomA.boundingBox())                  

      for id in intersects:
        vlayerB.featureAtId(int(id),  featB)
        attribB = featB.attributeMap()
        try:
          geomA = geomA.difference(featB.geometry())
        except:
          if self.message==False:
            QMessageBox.warning(None, QCoreApplication.translate("Geoprocessing","Error"), self.topoErrorMessage)              

            self.message = True
          
      fet = QgsFeature()
      fet.setGeometry(geomA)

  
      fet.setAttributeMap(attribA)      

      if self.isValidGeometry(fet):
        resultList.append(fet)
      else:
        break

    return resultList

  def makeSymDifference(self, writer, vlayerA, vlayerB):
  
    providerA = vlayerA.dataProvider()
    providerB = vlayerB.dataProvider()  
      
    featA = QgsFeature()
    featB = QgsFeature()
           
    allAttrsA = providerA.attributeIndexes()
    allAttrsB = providerB.attributeIndexes()    
        
#select only to the intersection square of the bounding boxes of Layer A
    providerA.select(allAttrsA)    
    providerB.select(allAttrsB)    
    
#    index = self.createIndex(providerB)
   
    while providerA.nextFeature(featA):
      geomA = featA.geometry()
      attribA = featA.attributeMap()
#      intersects = index.intersects(geomA.boundingBox())                  

      while providerB.nextFeature(featB):
        geomA = geomA.symDifference(featB.geometry())

      fet = QgsFeature()
      fet.setGeometry(geomA)
      fet.setAttributeMap(attribA)

      if self.isValidGeometry(fet):
        writer.addFeature(fet)
      else:
        break
        
    return 0
    
  def makeIntersection(self, vlayerA, vlayerB):

    providerA = vlayerA.dataProvider()
    providerB = vlayerB.dataProvider()  

    featA = QgsFeature()
    featB = QgsFeature()
        
    allAttrsA = providerA.attributeIndexes()
    allAttrsB = providerB.attributeIndexes()    

#select only to the intersection square of the bounding boxes
    combinedExtent = vlayerB.extent().intersect(vlayerA.extent())
    
    providerA.select(allAttrsA, combinedExtent)
    providerB.select(allAttrsB, combinedExtent)    

    index = self.createIndex(providerB) 
    nElement = 0
    resultList = []
    
    self.geo_ctrl.progressBar.setValue(0)
    self.geo_ctrl.progressBar.setRange(0, -1)    


    while providerA.nextFeature(featA):
      geomA = featA.geometry()
      attribA = featA.attributeMap()    
      intersects = index.intersects(geomA.boundingBox())
      
      nElement += len(intersects)
      nElement += 1
      
#      self.geo_ctrl.progressBar.setValue(-1) 
      self.geo_ctrl.progressBar.setValue(nElement)          

      for id in intersects: 
        vlayerB.featureAtId(int(id), featB)
        attribB = featB.attributeMap()        
        result = geomA.intersection(featB.geometry())
        
        mAttributes = self.mergeAttributes(attribA, attribB)    
        
        fet = QgsFeature()
        fet.setGeometry(result)     
        fet.setAttributeMap(mAttributes)

        if self.isValidGeometry(fet):
            resultList.append(fet)
        else:
          break
          
    return resultList

    
  def makeDissolve(self, vlayerA, fieldID=-1, attribValue=""):
  
    providerA = vlayerA.dataProvider()   

    featA = QgsFeature()
    allAttrsA = providerA.attributeIndexes()    
        
    providerA.select(allAttrsA)         
    
    result = QgsFeature()

    first = True
    nElement = 0
    resultList = []        
       
    
    while providerA.nextFeature(featA):
      attrs = featA.attributeMap()
      if fieldID==-1:
        if first:
          result.setGeometry(featA.geometry())        
          first = False
        else:
           result.setGeometry(result.geometry().combine(featA.geometry()))     
  
        self.nElement += 1  
        self.geo_ctrl.progressBar.setValue(self.nElement)         
      else:
        if attrs[fieldID].toString() == unicode(attribValue,'latin1'):         
          if first:
            result.setGeometry(featA.geometry())        
            first = False
          else:
             result.setGeometry(result.geometry().combine(featA.geometry()))     
    
          self.nElement += 1  
          self.geo_ctrl.progressBar.setValue(self.nElement)
  
    result.addAttribute(fieldID, QVariant(attribValue))      

    if self.isValidGeometry(result):
        resultList.append(result)
    
    return resultList

          
          
  def makeMerge(self, vlayerA, vlayerB):

    providerA = vlayerA.dataProvider()  
    featA = QgsFeature()
    allAttrsA = providerA.attributeIndexes()
    providerA.select(allAttrsA)
    resultList = []
    
    self.geo_ctrl.progressBar.setValue(0)
    self.geo_ctrl.progressBar.setRange(0, -1)    


    while providerA.nextFeature(featA):
       resultList.append(featA)

    providerB = vlayerB.dataProvider()  
    featB = QgsFeature()
    allAttrsB = providerB.attributeIndexes()    
    providerB.select(allAttrsB)          

    while providerB.getNextFeature(featB):
       resultList.append(featB)
       
    for fet in resultList:
      print fet.geometry().exportToWkt()   
          
    return resultList
