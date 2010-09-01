"""
/***************************************************************************
UrbanAnalysisDialog
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
"""

from PyQt4 import QtCore, QtGui 
from Ui_UrbanAnalysis import Ui_UrbanAnalysis
# create the dialog for zoom to point
class UrbanAnalysisDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_UrbanAnalysis()
    self.ui.setupUi(self) 

