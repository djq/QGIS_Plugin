"""
/***************************************************************************
UrbanAnalysis
A QGIS plugin
This tool helps perform basic urban analysis
                             -------------------
begin                : 2010-06-23 
copyright            : (C) 2010 by David Quinn
email                : djq@mit.edu 
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
def name(): 
  return "Tool for urban analysis" 
def description():
  return "This tool helps perform basic urban analysis"
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "1.0"
def classFactory(iface): 
  # load UrbanAnalysis class from file UrbanAnalysis
  from UrbanAnalysis import UrbanAnalysis 
  return UrbanAnalysis(iface)


