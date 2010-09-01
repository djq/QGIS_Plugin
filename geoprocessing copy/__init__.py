# -*- coding: latin1 -*-
def name():
  return "Geoprocessing"

def description():
  return "Plugin for Geoprocessing"

def version():
  return "0.55"

def qgisMinimumVersion():
  return "1.0"

def classFactory(iface):
  from geoprocessing import Geoprocessing
  return Geoprocessing(iface)

