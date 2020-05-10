from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui

import sys
import os
sys.path.append(os.getcwd())
from retiming import RetimingTool



class RetimingUI(QtWidgets.QDialog):
    WINDOW_TITLE = "Maya Retiming Tool"
    ABSOLUTE_BUTTON_WIDTH = 50
    RELATIVE_BUTTON_WIDTH = 64
    RETIMING_PROPERTY_NAME = 'retiming_data'

    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(RetimingUI, self).__init__(self.maya_main_window())
        self.setWindowTitle(self.WINDOW_TITLE)
        
        # set different flags based on OS
        if cmds.about(ntOS=True):
            # windows: remove question mark
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            # mac: set as tool so it appears infront of window
            self.setWindowFlags(QtCore.Qt.Tool)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.absolute_buttons = []
        # create buttons that will be linked to absolute changes
        for i in range(1,7):
            btn = QtWidgets.QPushButton('{0}f'.format(i))
            btn.setFixedWidth(self.ABSOLUTE_BUTTON_WIDTH)
            # propert is is name and increment
            btn.setProperty(self.RETIMING_PROPERTY_NAME, [i, False])
            self.absolute_buttons.append(btn)
        
        self.relative_buttons = []
        for i in [-2, -1, 1, 2]:
            btn = QtWidgets.QPushButton('{0}f'.format(i))
            btn.setFixedWidth(self.RELATIVE_BUTTON_WIDTH)
            btn.setProperty(self.RETIMING_PROPERTY_NAME, [i, True])
            self.relative_buttons.append(btn)
        self.move_to_next_cb = QtWidgets.QCheckBox("Move to Next Frame")

    def create_layouts(self):
        # make both absolute and relative buttons horizontal boxes
        absolute_retime_layout = QtWidgets.QHBoxLayout()
        absolute_retime_layout.setSpacing(2)
        for i in self.absolute_buttons:
            absolute_retime_layout.addWidget(i)
            
        relative_retime_layout = QtWidgets.QHBoxLayout()
        relative_retime_layout.setSpacing(2)

        for i in self.relative_buttons: 
            relative_retime_layout.addWidget(i)
            if relative_retime_layout.count() == 2:
                relative_retime_layout.addStretch()
        
        # create a main layout to host the button layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addLayout(absolute_retime_layout)
        main_layout.addLayout(relative_retime_layout)
        main_layout.addWidget(self.move_to_next_cb)

    def create_connections(self):
        # create conenctions for each button to call the retime function
        for i in self.absolute_buttons:
            i.clicked.connect(self.retime)
        for i in self.relative_buttons:
            i.clicked.connect(self.retime)

    def retime(self):
        # get who called the function
        btn = self.sender()
        # null check
        if btn:
            # get the property which has [name, iterative]
            retiming_data = btn.property(self.RETIMING_PROPERTY_NAME)
            mtn = self.move_to_next_cb.isChecked()
            # call retiming method
            RetimingTool.retime_keys(retiming_data[0], retiming_data[1], mtn)


if __name__ == "__main__":

    try:
        retiming_ui.close()
        retiming_ui.deleteLater()
    except:
        pass

    retiming_ui = RetimingUI()
    retiming_ui.show()
