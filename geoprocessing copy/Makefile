
all: resources.py ui_geoprocessing.py

clean:
	rm -f ui_geoprocessing.py resources.py
	rm -f *.pyc

ui_geoprocessing.py: geoprocessing.ui
	pyuic4 -o ui_geoprocessing.py geoprocessing.ui

resources.py: resources.qrc
	pyrcc4 -o resources.py resources.qrc

