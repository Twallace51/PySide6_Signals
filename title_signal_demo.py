""" Simple demo of using windowTitleChanged signal, inherited from QWidget.
See below for Final Comments
"""

if "imports":
    import PySide6.QtWidgets as W
    import PySide6.QtGui as G
    from random import random

class DemoWindow(W.QWidget):
    """The emit() function of windowTitleChanged signal, has a single string argument corresponding to new window title """
    def demo_code_init(self):
        """following is demo specific code """

        self.window_grid_header.setText("Click any mouse button to test windowTitleChanged signal")

        self.windowTitleChanged.connect(print)   # connect windowTitleChanged.signal to print()

    def mousePressEvent(self, event):
        """following is simply an an easy way to change the window title and test the signal """

        print("\nmousePressEvent() has updated window title")    # --> to terminal

        self.setWindowTitle(F"Window Title {str(random())}")

    def default_window_init(self):
        """following rarely needs to be customized in demos"""

        self.setWindowTitle("Window Title")

        if "QGridLayout window layout for all content":
            self.window_grid_layout = W.QGridLayout()
            self.setLayout(self.window_grid_layout)
            self.window_grid_layout.setRowStretch(20, 100) # push all current and future widgets to top of window layout

        if "window grid header":
            self.window_grid_header = W.QLabel() #Note: QLabel does not handle mouseEvents, event propagated to parent
            self.window_grid_header.setFont(G.QFont("Times", 14, G.QFont.Bold))
            self.window_grid_layout.addWidget(self.window_grid_header, 1, 0, 1, 4)
            #self.window_grid_header.setText("default message")

    def __init__(self):
        W.QWidget.__init__(self)
        self.default_window_init()
        self.demo_code_init()

if __name__ == "__main__":
    import sys
    app = W.QApplication(sys.argv)

    window = DemoWindow()
    window.show()

    app.exec()


""" Final Comments
By itself,  this is not a good demo for learning about signals,  because so much is hidden.
Only one line above, in demo_code_init() section,  actually deals with signals.

Note that all the rest is hidden (as private functions) in the QWidget class:
- instance name of window title widget
- WindowTitleChangedEvent()
- the corresponding event() handler,
  that runs the `windowTitleChanged.emit(self.windowTitle())` statement

Therefore,  you cannot subclass the handler nor use an event filter to intercept the event.

However,  the code is safer and more readable,  since
- the code is simpler and
- you are prevented from messing with the internals of QWidget code
"""
