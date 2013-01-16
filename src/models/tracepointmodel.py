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

from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt4.QtGui import QItemDelegate
from operator import attrgetter
from .breakpointmodel import ExtendedBreakpoint
from variables.variablelist import VariableList
from variables.varwrapperfactory import VarWrapperFactory
from helpers.tools import cpp2py
import logging


class ValueList():
    """This class provides a name and a list of
    Values
    """
    def __init__(self, name, type_):
        self.name = name
        self.values = []
        self.type = type_

    def addValue(self, type_, val):
        if self.type != type_:
            self.type = type_
        if type_ == "int":
            self.values.append(int(val))
        elif type_ == "bool":
            self.values.append(cpp2py(val))
        elif type_ == "float" or self.type == "double":
            self.values.append(float(val))

    def clear(self):
        self.values = []


class Tracepoint(ExtendedBreakpoint):
    """This class is used as a tracepoint in tracepointmodel.
    Basically Tracpoints are Breakpoint but they are extended
    with tracedVariables (list of Variable-Value-Pairs).
    Every Tracepoint contains some variables that are traced.
    Tracepoints are breakpoints and stop program then get
    information of asked variables and then continue program
    """

    def __init__(self, distObjects, sensitiveVariable, nr):
        """Init Tracepoint
        @param sensitiveVariable: is the sensitive variable.
        Use extendedBreakpoints for this. If extBP occures
        then the variables and their values will be stored.
        """
        ExtendedBreakpoint.__init__(self, sensitiveVariable, distObjects.gdb_connector)
        self.name = "TP #%s" % nr
        """here are the traced variables stored with their values"""
        self.gdb_connector = distObjects.gdb_connector
        self.distObjects = distObjects
        self.vwFactory = VarWrapperFactory()
        self.variableList = VariableList(self.vwFactory, distObjects)
        self.wave = []

    def addVar(self, variableToTrace):
        """ add a var to trace its value
        @param variableToTrace: variable name of the variable that should be traced"""
        vw = self.variableList.addVarByName(variableToTrace)
        newValueList = ValueList(variableToTrace, vw.type)
        self.wave.append(newValueList)

    def recordData(self):
        """tracepoint occurred: get values of all traced variables then continue debugging """
        for varList in self.wave:
            for v in self.variableList.list:
                if v.uniqueName == varList.name:
                    varList.addValue(v.type, v.value)


class TracepointModel(QAbstractTableModel):
    """This class provides the TracpointModel to View
    """

    def __init__(self, distObjects, parent=None):
        """Init TracepointModel
        """
        QAbstractTableModel.__init__(self, parent)
        QItemDelegate.__init__(self, parent)
        self.tracepoints = []
        self.distObjects = distObjects
        self.connector = distObjects.gdb_connector

    def insertTracepoint(self, file, line):
        """insert a tracepoint on sepcified place/line
         @param file: (str) name of file where tracepoint should be inserted
         @param line: (int) line of file where tracepoint should be inserted
        """
        res = self.connector.insertBreakpoint(file, line)
        self.beginInsertRows(QModelIndex(), len(self.tracepoints),
                             len(self.tracepoints))
        "sensitiveVariable has to be a Extended Breakpoint"
        tracepoint = Tracepoint(self.distObjects, res.bkpt, self.__getTpNumber(0))
        self.tracepoints.append(tracepoint)
        self.endInsertRows()

        return int(tracepoint.line)

    def deleteTracepoint(self, file, line):
        """delete a tracepoint on sepcified place/line
         @param file: (str) name of file where tracepoint should be deleted
         @param line: (int) line of file where tracepoint should be deleted
        """
        for tp in self.tracepoints:
            if tp.fullname == file and int(tp.line) == line:
                self.connector.deleteBreakpoint(tp.number)
                idx = self.tracepoints.index(tp)
                self.beginRemoveRows(QModelIndex(), idx, idx)
                self.tracepoints.remove(tp)
                self.endRemoveRows()
                break

    def __getTpNumber(self, nr):
        '''@return int - lowest, not used tp number'''
        for tp in self.tracepoints:
            if tp.name.endswith(str(nr)):
                return self.__getTpNumber(nr + 1)
        return nr

    def clearTracepoints(self):
        '''Delete all tracepoints after opening new executable'''
        while len(self.tracepoints) > 0:
            tp = self.tracepoints.pop()
            self.deleteTracepoint(tp.file, tp.line)

    def clearTracepointData(self):
        ''' Clear traced data of tracepoints'''
        for tp in self.tracepoints:
            for val in tp.wave:
                val.clear()

    def toggleTracepoint(self, fullname, line):
        """toggles tracepoint in file fullname on line line
        @param fullname: (str) full name of file
        @param line: (int) line number of tracepoint
        """
        if self.isTracepointByLocation(fullname, line):
            self.deleteTracepoint(fullname, line)
            return -1
        else:
            return self.insertTracepoint(fullname, line)

    def enableTracepoint(self, number):
        """enabled tracepoint in line number
        @param number: (int) number of line
        """
        self.connector.enableBreakpoint(number)

    def disableTracepoint(self, number):
        """disable tracepoint in line number
        @param number: line of number
        """
        self.connector.disableBreakpoint(number)

    def handleTracepoint(self, bpInfo):
        """handles occured tracepoint
        @param bpInfo: bpInfo.fullname = filename  bpInfo.line = line of tracepoint
        """
        for tp in self.tracepoints:
            if tp.fullname == bpInfo.fullname and int(tp.line) == int(bpInfo.line):
                tp.tracePointOccured()

    def isTracepointByNumber(self, number):
        for tp in self.tracepoints:
            if int(tp.number) == int(number):
                return tp
        return None

    def isTracepointByLocation(self, fullname, line):
        """ search for tracepoint in file fullname on linenumber line
        @param fullname: (string), name of file
        @param line: (int), number of line
        @return: tracepoint if tracepoint found in list, None else
        """
        for tp in self.tracepoints:
            if tp.fullname == fullname and int(tp.line) == int(line):
                return tp
        return None

    def getTracepoints(self):
        return self.tracepoints

    def rowCount(self, parent):
        return len(self.tracepoints)

    def columnCount(self, parent):
        return 10

    def data(self, index, role):
        assert(index.row() < len(self.tracepoints))

        ret = None

        tp = self.tracepoints[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                ret = tp.file
            elif index.column() == 1:
                ret = tp.line
            elif index.column() == 2:
                ret = tp.fullname
            elif index.column() == 3:
                ret = tp.number
            elif index.column() == 5:
                ret = tp.addr
            elif index.column() == 6:
                ret = tp.condition
            elif index.column() == 7:
                ret = tp.skip
            elif index.column() == 8:
                # TODO: return value with all elements
                pass
            elif index.column() == 9:
                ret = tp.name
        elif role == Qt.CheckStateRole:
            if index.column() == 4:
                ret = Qt.Checked if tp.enabled == 'y' else Qt.Unchecked

        return ret

    def headerData(self, section, orientation, role):
        ret = None

        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    ret = "File"
                elif section == 1:
                    ret = "Line"
                elif section == 2:
                    ret = "Full name"
                elif section == 3:
                    ret = "Number"
                elif section == 4:
                    ret = "Enabled"
                elif section == 5:
                    ret = "Address"
                elif section == 6:
                    ret = "Condition"
                elif section == 7:
                    ret = "Skip"
                elif section == 8:
                    ret = "Traced Variables"
                elif section == 9:
                    ret = "Name"

        return ret

    def sort(self, column, order):
        if order == Qt.AscendingOrder:
            rev = False
        else:
            rev = True

        if column == 0:
            key = 'file'
        elif column == 1:
            key = 'line'
        elif column == 2:
            key = 'fullname'
        elif column == 3:
            key = 'number'
        elif column == 4:
            key = 'enabled'
        elif column == 5:
            key = 'addr'
        elif column == 6:
            key = 'condition'
        elif column == 7:
            key = 'skip'
        elif column == 8:
            key = 'tracedVariables'
        elif column == 9:
            key = 'name'

        self.beginResetModel()
        self.tracepoints.sort(key=attrgetter(key), reverse=rev)
        self.endResetModel()

    def flags(self, index):
        f = Qt.ItemIsSelectable | Qt.ItemIsEnabled

        if index.column() == 0:
            pass
        elif index.column() == 1:
            pass
        elif index.column() == 2:
            pass
        elif index.column() == 3:
            pass
        elif index.column() == 4:
            f |= Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        elif index.column() == 5:
            pass
        elif index.column() == 6:
            f |= Qt.ItemIsEnabled | Qt.ItemIsEditable
        elif index.column() == 7:
            f |= Qt.ItemIsEnabled | Qt.ItemIsEditable
        elif index.column() == 8:
            pass
        elif index.column() == 9:
            f |= Qt.ItemIsEnabled | Qt.ItemIsEditable

        return f

    def setData(self, index, value, role):
        bp = self.tracepoints[index.row()]

        # """index.column() == 6 -> condition"""
        if index.column() == 6:
            try:
                bp.condition = str(value.toString())
                self.changeCondition(bp.number, bp.condition)
            except:
                logging.error("setData: data type mismatch bp.condition is str and value is not")
                return False

        # """index.column() == 7 -> skip"""
        elif index.column() == 7:
            validSkip = QVariant(value).toInt()
            if not validSkip[1]:
                logging.error("setData: value from user is not int")
                return False
            bp.skip = int(validSkip[0])
            self.changeSkip(bp.number, str(bp.skip))

        # """index.column() == 4 -> enabled"""
        elif index.column() == 4:
            if role == Qt.CheckStateRole:
                # breakpoint is active, set inactive
                if not QVariant(value).toBool():
                    bp.enabled = 'n'
                    self.disableTracepoint(bp.number)
                # breakpoint is inactive, set active
                else:
                    bp.enabled = 'y'
                    self.enableTracepoint(bp.number)

        # """index.column() == 9 -> name of tracepoint"""
        elif index.column() == 9:
            bp.name = str(value.toString())

        return True

    def selectionMade(self, index):
        """ called if row in TracepointView is clicked, start to update wave in tracepointWaveView
        @param index: index of row that was clicked
        """
        tp = self.tracepoints[index.row()]
        self.distObjects.tracepointwaveController.updateTracepointWaveView(tp.wave)
