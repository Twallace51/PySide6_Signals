""" Simple demo template - creating and using a new signal with one argument,  to update a QLabel ojject
    Also - see Final Comment below
"""

if "imports":
    from rich import print                         # https://rich.readthedocs.io/en/stable/introduction.html
    import PySide6.QtCore as C
    from PySide6.QtCore import Signal, Slot
    import PySide6.QtWidgets as W
    import PySide6.QtGui as G

class DemoWindow(W.QWidget):
    """
    The signal created below must be created here in classes's namespace,
    rather than locally to class in def __init__(self) below
    Note: the Signal(int) argument below requires that:
    - emit() is run with a single integer argument - see subclassed mousePressEvent() below
    - any connected slot functions must be compatible with a single int argument - see update_count() below
    """
    demo_signal =  Signal(int) # signals ~must~ be created here, in app's namespace/scope

    def __init__(self):
        """ """
        W.QWidget.__init__(self)
        #self.demo_signal =  C.Signal()  # this does ~not~ work - AttributeError: 'PySide6.QtCore.Signal' object has no attribute 'connect'
        self.default_window_init()
        self.demo_init()

    def demo_init(self):
        """following is demo specific code """
        self.count = 0
        self.setWindowTitle("custom Signal demo")
        self.window_grid_header.setText("click middle button to update click count")

        self.demo_signal.connect(self.update_count)

    def mousePressEvent(self, event):
        """this is an inherited event handler, initially void, now subclassed to run demo_signal.emit()"""

        if event.button() == C.Qt.MiddleButton:
            print(F"\n{event.button()} click detected")  # --> to terminal
            print("demo_signal emitted")                 # --> to terminal

            self.count += 1
            #self.demo_signal.emit()   --> TypeError: demo_signal(int) needs 1 argument(s), 0 given!
            self.demo_signal.emit(self.count)


    @Slot(int)   # decorator optional here, but required if slot will be connected to signals in other windows
    def update_count(self, _count):
        """this is the slot for updating the window_grid_header and is connected to demo_signal"""

        print("demo_signal slot update_count(count) was run")        # --> to terminal

        self.count_lbl.setText(F"Middle click count = {_count}")

    def default_window_init(self):
        """following rarely needs to be customized in demos"""

        self.setWindowTitle("Window Title")

        if "QGridLayout window layout for all content":
            self.window_grid_layout = W.QGridLayout()
            self.setLayout(self.window_grid_layout)
            self.window_grid_layout.setRowStretch(20, 100) # push all current and future widgets to top of window layout

        if "window grid header":
            self.window_grid_header = W.QLabel() #Note: does not generate mouseEvents, parent window does
            self.window_grid_header.setFont(G.QFont("Times", 14, G.QFont.Bold))
            self.window_grid_header.setText("subclass this for desired message")

            self.window_grid_layout.addWidget(self.window_grid_header, 1, 0, 1, 4)

        if "count field":
            self.count_lbl = W.QLabel() #Note: does not generate mouseEvents, parent window does
            self.count_lbl.setFont(G.QFont("Times", 14, G.QFont.Bold))
            self.count_lbl.setText("Current count = 0")

            self.window_grid_layout.addWidget(self.count_lbl, 2, 0, 1, 4)

if __name__ == "__main__":
    import sys
    app = W.QApplication(sys.argv)

    window = DemoWindow()
    window.show()

    app.exec()

"""Final Comment:
The above code works and is great for understanding how a Signal works.

Obviously however, in this example, it would have been a whole lot easier to simply subclass mousePressEvent()
to run the following directly

    self.update_count(self.count)

On the other hand,  it would now also be very simple to subclass mousePressEvent() in another window,
create and connect a signal in that window to update_count() above,
and count mouse clicks in the other window,  here in this window.
"""
