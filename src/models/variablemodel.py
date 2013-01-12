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

from PyQt4.QtCore import QAbstractItemModel, Qt, QModelIndex, QObject, QMimeData, QStringList
from PyQt4.QtGui import QPixmap, QBrush, QPainter
from variables import variable
import logging


class TreeItem(QObject):
    '''
    Base treeitem class
    '''
    def __init__(self):
        """ Constructor <br>
            Create a TreeItem for the VariableModel
        """
        QObject.__init__(self)

        ## @var parent
        #  TreeItem, parent TreeItem
        self.parent = None
        ## @var changed
        #  bool, changed state of TreeItem
        self.changed = False
        ## @var markChanged
        #  bool, changed state of TreeItem for color highlighting
        self.markChanged = False
        ## @var childItems
        #  TreeItem[], list of containing childitems
        self.childItems = []

    def setParent(self, parent):
        """ set parent item for TreeItem
        @param parent   TreeItem, item set as parent
        """
        self.parent = parent

    def getParent(self):
        """ get parent TreeItem
        @return   TreeItem, parent item
        """
        return self.parent

    def addChild(self, child):
        """ add a child TreeItem
        @param child   TreeItem, child to add
        """
        self.childItems.append(child)

    def getChildren(self, factory=None):
        """ return list of children
        @param factory   derived from VarWrapperFactory, factory to look in VariableList for children
        @return          TreeItem[], list of children
        """
        return self.childItems

    def removeChildren(self):
        """ remove all containing children
        """
        for child in self.childItems:
            child.removeChildren()
        del self.childItems[:]

    def getChildCount(self):
        """ get number of children
        @return   int, childcount
        """
        return self.childItems.__len__()

    def getRow(self, factory):
        """ get row index in VariableModel
        @param factory   derived from VarWrapperFactory, factory to look in VariableList for children
        @return          int, rowindex
        """
        if self.parent is not None:
            row = self.parent.getChildren(factory).index(self)
            return row
        return 0

    def getChanged(self):
        """ gets a bool value if TreeItem has changed
        @return   bool, changed state
        """
        return self.changed

    def setChanged(self, changed):
        """ sets changed variable of TreeItem if underlying Variable has changed
        @param changed   bool, changed state (true if value has changed)
        """
        self.changed = changed

    def getMarkChanged(self):
        """ gets get change state of TreeItem <br>
            this method is used to color a variable if its value has changed
        @return   bool, changed state for color highlighting
        """
        return self.markChanged

    def setMarkChanged(self, markChanged):
        """ sets a bool value if TreeItem is marked as changed <br>
            this method is used to color a variable if its value has changed
        @param markChanged   bool,  changed state (true if value has changed)
        """
        self.markChanged = markChanged

    def hasChanged(self):
        """ sets a TreeItems changed state
            this function is connected to the signal SignalProxy::changed()
        """
        self.setChanged(True)


class RootVarWrapper(TreeItem):
    """ dummy wrapper for root TreeItem <br>
        this item is not visible in view.
    """
    def __init__(self):
        """ Constructor <br>
            Create the root VarWrapper
        """
        TreeItem.__init__(self)
        ## @var header
        #  string[], displayed text in header columns
        self.header = ["Expression", "Type", "Value"]
        ## @var parent
        #  TreeItem, parent item for root is None
        self.parent = None

    def getHeader(self):
        """ get the header columns
        @return   string[], text for headercolumns
        """
        return self.header


class VariableModel(QAbstractItemModel):
    """Class for a model representing GDB's variables."""
    def __init__(self, controller, distributedObjects, parent=None):
        """ Constructor <br>
            Create a VariableModel derived from an QAbstractItemModel to display the <br>
            GDB variables in a treeview.<br>
            Listens to the following Signals: SignalProxy::inferiorStoppedNormally(PyQt_PyObject) <br>
                                              SignalProxy::inferiorHasExited(PyQt_PyObject) and <br>
                                              SignalProxy::executableOpened()
        @param controller            controllers.WatchController, Reference to the WatchController
        @param distributedObjects    distributedobjects.DistributedObjects, the DistributedObjects-Instance
        @param parent                parent for the QAbstractItemModel-Constructor, can be None
        """

        QAbstractItemModel.__init__(self, parent)

        self.distributedObjects = distributedObjects
        self.controller = controller

        ## @var root
        #  RootVarWrapper, root item of tree
        self.root = RootVarWrapper()

        self.distributedObjects.signalProxy.inferiorStoppedNormally.connect(self.update)
        self.distributedObjects.signalProxy.inferiorHasExited.connect(self.clear)
        self.distributedObjects.signalProxy.executableOpened.connect(self.clear)

    def addVar(self, var):
        """ Adds a variable to the VariableModel <br>
            clears highlighted TreeItems changed at previous stop<br>
            update TreeItem value and highlight state
        @par var   TreeItem, variable to be added
        """
        self.layoutAboutToBeChanged.emit()
        self.setUnmarked(var)
        self.updateData(var)
        self.layoutChanged.emit()

    def removeChildren(self, parent):
        """ remove all children for given TreeItem
        @param parent   TreeItem, parent item contains children
        """
        for item in parent.getChildren(self.controller.vwFactory):
            self.removeChildren(item)
        parent.removeChildren()

    def getVariables(self):
        """ return all TreeItems in VariableModel
        @return   TreeItem[], list of children
        """
        return self.root.getChildren()

    def index(self, row, column, parent):
        """ QAbstractItemModel index function
            if item is collapsible get children for it <br>
            just get children for one recursion depth for better performance
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.root
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.getChildren(self.controller.vwFactory)[row]
        if childItem is not None:

            # get children for childitem
            childItem.getChildren(self.controller.vwFactory)

            idx = self.createIndex(row, column, childItem)
            return idx
        else:
            return QModelIndex()

    def parent(self, index):
        """ QAbstractItemModel parent function
        """

        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()

        parentItem = childItem.getParent()

        if parentItem == self.root:
            return QModelIndex()

        return self.createIndex(parentItem.getRow(self.controller.vwFactory), 0, parentItem)

    def rowCount(self, parent):
        """ QAbstractItemModel rowCount function
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.root
        else:
            parentItem = parent.internalPointer()

        return parentItem.getChildCount()

    def columnCount(self, parent):
        """ QAbstractItemModel columnCount function
        """
        return 3

    def data(self, index, role):
        """ QAbstractItemModel data function <br>
            diplay expression, type and value of variables in columns <br>
            use different icons for collapsible vars, non-collapsible vars and out-of-scope vars <br>
            highlight items if attributs of Varialble chaned
        """
        if not index.isValid():
            return None
        item = index.internalPointer()
        ret = None
        if role == Qt.DisplayRole:
            if index.column() == 0:
                ret = item.exp
            elif index.column() == 1:
                ret = item.type
            elif index.column() == 2:
                ret = item.value

        elif role == Qt.EditRole:
            if index.column() == 2:
                ret = item.value

        elif role == Qt.DecorationRole:
            if index.column() == 0:
                if item.access in ['private', 'protected']:
                    iconprefix = item.access + "_"
                else:
                    iconprefix = ""

                icon = None
                if not item.inScope:
                    return QPixmap(":/icons/images/outofscope.png")
                elif item.getChildCount() != 0:  # child item
                    icon = QPixmap(":/icons/images/" + iconprefix + "struct.png")
                else:  # leave item
                    icon = QPixmap(":/icons/images/" + iconprefix + "var.png")

                # overlay for arguments
                if icon and item._v.arg:
                    ol = QPixmap(":/icons/images/overlay_arg.png")
                    p = QPainter(icon)
                    p.drawPixmap(ol.rect(), ol)
                elif icon and item._v.exp == "Return value":
                    ol = QPixmap(":/icons/images/overlay_ret.png")
                    p = QPainter(icon)
                    p.drawPixmap(ol.rect(), ol)
                return icon
            elif index.column() == 2:
                if item.inScope:
                    return QPixmap(":/icons/images/edit.png")

        elif role == Qt.ForegroundRole:
            if not item.inScope:
                return QBrush(Qt.gray)

            if index.column() == 2:
                if item.getMarkChanged() and item.inScope:
                    return QBrush(Qt.green)

            return QBrush(Qt.black)
        return ret

    def flags(self, index):
        """ QAbstractItemModel flags function <br>
            items are enabled, selectable and editable <br>
            out of scope variables are not editable
        """
        if not index.isValid():
            return Qt.ItemIsDropEnabled

        item = index.internalPointer()
        if not item.inScope:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        ret = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if index.column() == 2:
            ret |= Qt.ItemIsEditable

        if index.column() == 0:
            ret |= Qt.ItemIsDragEnabled

        return ret

    def headerData(self, section, orientation, role):
        """ QAbstractItemModel flags function
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root.getHeader()[section]
        return None

    def clear(self):
        """ Clear all TreeItems.
            this function is connected to the signal SignalProxy::executableOpened() and inferiorHasExited(PyQt_PyObject)
        """
        self.beginResetModel()
        self.clearData()
        self.endResetModel()

    def clearData(self):
        """ Clear all TreeItems
        """
        self.root.childItems = []

    def update(self):
        """ Clear all TreeItems.
            clears highlighted TreeItems changed at previous stop<br>
            update TreeItems value and highlight state
            this function is connected to the signal SignalProxy::inferiorStoppedNormally(PyQt_PyObject)
        """
        self.layoutAboutToBeChanged.emit()
        self.setUnmarked(self.root)
        self.updateData(self.root)
        self.layoutChanged.emit()

    def updateData(self, parent):
        """ update TreeItems value and highlight state
        @param parent   TreeItem, parent item, root to update the whole model
        """
        for item in parent.getChildren(self.controller.vwFactory):
            if item.getChanged():
                item.setMarkChanged(True)
                item.setChanged(False)
            if item.getChildCount() != 0:
                self.updateData(item)

    def setUnmarked(self, parent):
        """ clears highlighted TreeItems changed at previous stop
        @param parent   TreeItem, parent item, root to update the whole model
        """
        for item in parent.getChildren(self.controller.vwFactory):
            if item.getMarkChanged():
                item.setMarkChanged(False)
            if item.getChildCount() != 0:
                self.setUnmarked(item)

    def setData(self, index, value, role):
        """ QAbstractItemModel flags function
        """
        if index.isValid() and role == Qt.EditRole:
            index.internalPointer().assignValue(value.toString())
            return True
        return False

    def getItem(self, index):
        """ Gets an item  by index <br>
            if item has a valid index, dont delete it because its not the root item <br>
            only children of root can be deleted
        @param index   QModelIndex, index of item
        """
        if index.isValid():
            logging.error("Only toplevel items can be deleted!")
            return None
        else:
            return self.root

    def removeRows(self, position, rows, parent):
        """ removes the selected row in the model
        @param position   int, starting position of selection
        @param rows       int, number of rows to delete beginning at starting position
        @param parent     TreeItem, parent item containing items to delete
        """
        success = True
        parentItem = self.getItem(parent)
        assert parentItem is not None
        if parentItem != self.root:
            logging.error("Cannot remove a child variable.")
            return

        self.beginRemoveRows(parent, position, position + rows - 1)
        for p in xrange(position, position + rows):
            del self.root.childItems[p]
        self.endRemoveRows()
        return success

    def mimeTypes(self):
        return QStringList([variable.MIME_TYPE])

    def mimeData(self, indexes):
        if len(indexes) == 1:
            item = indexes[0].internalPointer()
            d = QMimeData()
            d.setData(variable.MIME_TYPE, item.uniqueName)
            return d
        else:
            return None
