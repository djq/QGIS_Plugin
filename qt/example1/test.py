from PyQt4 import *
from untitled import *
import sys
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Form1()
    f.show()
    app.setMainWidget(f)
    app.exec_loop()