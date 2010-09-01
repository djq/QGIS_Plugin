/****************************************************************************
** ui.h extension file, included from the uic-generated form implementation.
**
** If you wish to add, delete or rename functions or slots use
** Qt Designer which will update this file, preserving your code. Create an
** init() function in place of a constructor, and a destroy() function in
** place of a destructor.
*****************************************************************************/


void Form1::AddEntry()
{
    # get the text typed in the line edit
    e = self.lineEdit1.text().ascii()

    # add that text to the list box
    self.listBox1.insertItem(e)

    # clear the line edit
    self.lineEdit1.clear()
}
