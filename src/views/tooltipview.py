# ricodebug - A GDB frontend which focuses on visually supported
# debugging using data structure graphs and SystemC features.
#
# Copyright (C) 2011  The ricodebug project team at the
# Upper Austrian University Of Applied Sciences Hagenberg,
# Department Embedded Systems Design
#
# This file is part of ricodebug.
#
# ricodebug is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further information see <http://syscdbg.hagenberg.servus.at/>.

from PyQt4.QtCore import Qt, QTimer, QModelIndex
from PyQt4.QtGui import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
        QSizeGrip, QSpacerItem, QSizePolicy, QStylePainter, QStyleOptionFrame, QStyle, QToolTip

from .treeitemview import TreeItemView
from helpers.icons import Icons


class ToolTipView(QWidget):
    ICON_SIZE = 22

    def __init__(self, distributedObjects, parent=None):
        QWidget.__init__(self, parent, Qt.Tool | Qt.FramelessWindowHint)
        self.setPalette(QToolTip.palette())

        self.__do = distributedObjects
        self.__allowHide = True
        self.treeItemView = TreeItemView()
        self.hide()

        self.exp = None

        addToWatchButton = QPushButton(Icons.watch, "")
        addToWatchButton.setMinimumSize(self.ICON_SIZE, self.ICON_SIZE)
        addToWatchButton.setMaximumSize(self.ICON_SIZE, self.ICON_SIZE)
        addToWatchButton.setToolTip("Add to Watch")
        addToWatchButton.clicked.connect(self.__addToWatch)
        addToDatagraphButton = QPushButton(Icons.datagraph, "")
        addToDatagraphButton.setMinimumSize(self.ICON_SIZE, self.ICON_SIZE)
        addToDatagraphButton.setMaximumSize(self.ICON_SIZE, self.ICON_SIZE)
        addToDatagraphButton.setToolTip("Add to Data Graph")
        addToDatagraphButton.clicked.connect(self.__addToDatagraph)
        setWatchpointButton = QPushButton(Icons.wp, "")
        setWatchpointButton.setMinimumSize(self.ICON_SIZE, self.ICON_SIZE)
        setWatchpointButton.setMaximumSize(self.ICON_SIZE, self.ICON_SIZE)
        setWatchpointButton.setToolTip("Set Watchpoint")
        setWatchpointButton.clicked.connect(self.__setWatchpoint)

        self.__layout = QHBoxLayout(self)
        self.__layout.addWidget(self.treeItemView)
        l = QVBoxLayout()
        l.addWidget(addToWatchButton)
        l.addWidget(addToDatagraphButton)
        l.addWidget(setWatchpointButton)
        l.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # show a size grip in the corner to allow the user to resize the window
        l.addWidget(QSizeGrip(self))
        l.setSpacing(0)
        self.__layout.addLayout(l)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)

        self.__hideTimer = QTimer()
        self.__hideTimer.setSingleShot(True)
        self.__hideTimer.timeout.connect(self.hideNow)

        self.treeItemView.contextMenuOpen.connect(self.__setDisallowHide)
        self.treeItemView.setRootIsDecorated(False)
        self.treeItemView.setHeaderHidden(True)

    def hideNow(self):
        if self.__allowHide:
            QWidget.hide(self)
            self.treeItemView.model().clear()

    def __setDisallowHide(self, x):
        self.__allowHide = not x

    def enterEvent(self, _):
        self.__hideTimer.stop()

    def hideLater(self):
        self.__hideTimer.start(250)

    # hide the widget when the mouse leaves it
    def leaveEvent(self, _):
        self.hideLater()

    def __addToWatch(self):
        self.__do.signalProxy.addWatch(self.exp)

    def __addToDatagraph(self):
        self.__do.datagraphController.addWatch(self.exp)

    def __setWatchpoint(self):
        self.__do.breakpointModel.insertWatchpoint(self.exp)

    def show(self, exp):
        self.resize(300, 90)

        # store the expression for __addToWatch and __addToDatagraph
        self.exp = exp

        # expand the item shown in the tool tip to save the user some work ;)
        self.treeItemView.setExpanded(self.treeItemView.model().index(0, 0, QModelIndex()), True)
        self.updateGeometry()

        QWidget.show(self)

    def setModel(self, model):
        self.treeItemView.setModel(model)

    def paintEvent(self, _):
        # this makes the tool tip use the system's tool tip color as its background
        painter = QStylePainter(self)
        opt = QStyleOptionFrame()
        opt.initFrom(self)
        painter.drawPrimitive(QStyle.PE_PanelTipLabel, opt)
