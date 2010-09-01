from PyQt4 import *
import at_auto

class at(at_auto):
    def __init__(self, parent=None, name=None, fl=0):
        at_auto.__init__(self,parent,name,fl)

if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = at()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
    
    
    désaccord