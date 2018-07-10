#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BNTX Injector
# Version 0.1
# Copyright © 2018 AboodXD

# This file is part of BNTX Injector.

# BNTX Injector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# BNTX Injector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Python version: sanity check
minimum = 3.4
import sys

currentRunningVersion = sys.version_info.major + (.1 * sys.version_info.minor)
if currentRunningVersion < minimum:
    errormsg = 'Please update your copy of Python to ' + str(minimum) + \
               ' or greater. Currently running on: ' + sys.version[:5]

    raise Exception(errormsg)

import os.path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtWidgets
import time
import traceback

import bntx as BNTX
import globals


def _excepthook(*exc_info):
    """
    Custom unhandled exceptions handler
    """
    separator = '-' * 80
    logFile = "log.txt"
    notice = \
        """An unhandled exception occurred. This program will now exit. """\
        """Please report the problem to @MasterVermilli0n#7241 on Discord.\n"""\
        """A log will be written to "%s".\n\nError information:\n""" % logFile

    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    e = "".join(traceback.format_exception(*exc_info))
    sections = [separator, timeString, separator, e]
    msg = '\n'.join(sections)

    try:
        with open(logFile, "w") as f:
            f.write(msg)

    except IOError:
        pass

    errorbox = QtWidgets.QMessageBox()
    errorbox.setText(notice + msg)
    errorbox.exec_()

    sys.exit(1)


# Override the exception handler with ours
sys.excepthook = _excepthook


class MainWindow(QtWidgets.QWidget):
    class Separator(QtWidgets.QFrame):
        def __init__(self):
            super().__init__()

            self.setFrameShape(QtWidgets.QFrame.HLine)
            self.setFrameShadow(QtWidgets.QFrame.Sunken)

    def __init__(self):
        super().__init__()

        self.setupUi()
        self.textures = []

        self.setWindowIcon(QIcon('icon.ico'))

    def setupUi(self):
        self.setWindowTitle("BNTX Injector v%s - By AboodXD" % globals.Version)
        self.setMinimumSize(375, 0)

        Layout = QtWidgets.QGridLayout()

        self.openbtn = QtWidgets.QPushButton("Open")
        self.openbtn.clicked.connect(self.openFile)

        self.openLnEdt = QtWidgets.QLineEdit()
        self.openLnEdt.setEnabled(False)

        self.fnameLabel = QtWidgets.QLabel()
        self.fnameLabel.setText("File name:")

        self.fnameLnEdt = QtWidgets.QLineEdit()
        self.fnameLnEdt.setEnabled(False)

        self.targetLabel = QtWidgets.QLabel()
        self.targetLabel.setText("Target:")

        self.targetLnEdt = QtWidgets.QLineEdit()
        self.targetLnEdt.setEnabled(False)

        self.tileModeLabel = QtWidgets.QLabel()
        self.tileModeLabel.setText("Tiling mode:")

        self.tileModeLnEdt = QtWidgets.QLineEdit()
        self.tileModeLnEdt.setEnabled(False)

        self.dimLabel = QtWidgets.QLabel()
        self.dimLabel.setText("Dimension:")

        self.dimLnEdt = QtWidgets.QLineEdit()
        self.dimLnEdt.setEnabled(False)

        self.sparseBindingLabel = QtWidgets.QLabel()
        self.sparseBindingLabel.setText("Sparse Binding:")

        self.sparseBindingLnEdt = QtWidgets.QLineEdit()
        self.sparseBindingLnEdt.setEnabled(False)

        self.sparseResidencyLabel = QtWidgets.QLabel()
        self.sparseResidencyLabel.setText("Sparse Residency:")

        self.sparseResidencyLnEdt = QtWidgets.QLineEdit()
        self.sparseResidencyLnEdt.setEnabled(False)

        self.swizzleLabel = QtWidgets.QLabel()
        self.swizzleLabel.setText("Swizzle:")

        self.swizzleLnEdt = QtWidgets.QLineEdit()
        self.swizzleLnEdt.setEnabled(False)

        self.numMipsLabel = QtWidgets.QLabel()
        self.numMipsLabel.setText("Number of Mipmaps:")

        self.numMipsLnEdt = QtWidgets.QLineEdit()
        self.numMipsLnEdt.setEnabled(False)

        self.numSamplesLabel = QtWidgets.QLabel()
        self.numSamplesLabel.setText("Number of Multi Samples:")

        self.numSamplesLnEdt = QtWidgets.QLineEdit()
        self.numSamplesLnEdt.setEnabled(False)

        self.formatLabel = QtWidgets.QLabel()
        self.formatLabel.setText("Format:")

        self.formatLnEdt = QtWidgets.QLineEdit()
        self.formatLnEdt.setEnabled(False)

        self.accessFlagsLabel = QtWidgets.QLabel()
        self.accessFlagsLabel.setText("GPU Access Flag:")

        self.accessFlagsLnEdt = QtWidgets.QLineEdit()
        self.accessFlagsLnEdt.setEnabled(False)

        self.widthLabel = QtWidgets.QLabel()
        self.widthLabel.setText("Width:")

        self.widthLnEdt = QtWidgets.QLineEdit()
        self.widthLnEdt.setEnabled(False)

        self.heightLabel = QtWidgets.QLabel()
        self.heightLabel.setText("Height:")

        self.heightLnEdt = QtWidgets.QLineEdit()
        self.heightLnEdt.setEnabled(False)

        self.arrayLengthLabel = QtWidgets.QLabel()
        self.arrayLengthLabel.setText("Array Length:")

        self.arrayLengthLnEdt = QtWidgets.QLineEdit()
        self.arrayLengthLnEdt.setEnabled(False)

        self.blockHeightLabel = QtWidgets.QLabel()
        self.blockHeightLabel.setText("Block Height:")

        self.blockHeightLnEdt = QtWidgets.QLineEdit()
        self.blockHeightLnEdt.setEnabled(False)

        self.imgSizeLabel = QtWidgets.QLabel()
        self.imgSizeLabel.setText("Image Size:")

        self.imgSizeLnEdt = QtWidgets.QLineEdit()
        self.imgSizeLnEdt.setEnabled(False)

        self.alignmentLabel = QtWidgets.QLabel()
        self.alignmentLabel.setText("Alignment:")

        self.alignmentLnEdt = QtWidgets.QLineEdit()
        self.alignmentLnEdt.setEnabled(False)

        self.chan1Label = QtWidgets.QLabel()
        self.chan1Label.setText("Channel 1:")

        self.chan1LnEdt = QtWidgets.QLineEdit()
        self.chan1LnEdt.setEnabled(False)

        self.chan2Label = QtWidgets.QLabel()
        self.chan2Label.setText("Channel 2:")

        self.chan2LnEdt = QtWidgets.QLineEdit()
        self.chan2LnEdt.setEnabled(False)

        self.chan3Label = QtWidgets.QLabel()
        self.chan3Label.setText("Channel 3:")

        self.chan3LnEdt = QtWidgets.QLineEdit()
        self.chan3LnEdt.setEnabled(False)

        self.chan4Label = QtWidgets.QLabel()
        self.chan4Label.setText("Channel 4:")

        self.chan4LnEdt = QtWidgets.QLineEdit()
        self.chan4LnEdt.setEnabled(False)

        self.imgTypeLabel = QtWidgets.QLabel()
        self.imgTypeLabel.setText("Image type:")

        self.imgTypeLnEdt = QtWidgets.QLineEdit()
        self.imgTypeLnEdt.setEnabled(False)
        
        openLayout = QtWidgets.QHBoxLayout()
        openLayout.addWidget(self.openbtn)
        openLayout.addWidget(self.openLnEdt)
        
        fnameLayout = QtWidgets.QHBoxLayout()
        fnameLayout.addWidget(self.fnameLabel)
        fnameLayout.addWidget(self.fnameLnEdt)
        
        targetLayout = QtWidgets.QHBoxLayout()
        targetLayout.addWidget(self.targetLabel)
        targetLayout.addWidget(self.targetLnEdt)
        
        tileModeLayout = QtWidgets.QHBoxLayout()
        tileModeLayout.addWidget(self.tileModeLabel)
        tileModeLayout.addWidget(self.tileModeLnEdt)
        
        dimLayout = QtWidgets.QHBoxLayout()
        dimLayout.addWidget(self.dimLabel)
        dimLayout.addWidget(self.dimLnEdt)
        
        sparseBindingLayout = QtWidgets.QHBoxLayout()
        sparseBindingLayout.addWidget(self.sparseBindingLabel)
        sparseBindingLayout.addWidget(self.sparseBindingLnEdt)
        
        sparseResidencyLayout = QtWidgets.QHBoxLayout()
        sparseResidencyLayout.addWidget(self.sparseResidencyLabel)
        sparseResidencyLayout.addWidget(self.sparseResidencyLnEdt)
        
        swizzleLayout = QtWidgets.QHBoxLayout()
        swizzleLayout.addWidget(self.swizzleLabel)
        swizzleLayout.addWidget(self.swizzleLnEdt)
        
        numMipsLayout = QtWidgets.QHBoxLayout()
        numMipsLayout.addWidget(self.numMipsLabel)
        numMipsLayout.addWidget(self.numMipsLnEdt)
        
        numSamplesLayout = QtWidgets.QHBoxLayout()
        numSamplesLayout.addWidget(self.numSamplesLabel)
        numSamplesLayout.addWidget(self.numSamplesLnEdt)
        
        formatLayout = QtWidgets.QHBoxLayout()
        formatLayout.addWidget(self.formatLabel)
        formatLayout.addWidget(self.formatLnEdt)
        
        accessFlagsLayout = QtWidgets.QHBoxLayout()
        accessFlagsLayout.addWidget(self.accessFlagsLabel)
        accessFlagsLayout.addWidget(self.accessFlagsLnEdt)
        
        widthLayout = QtWidgets.QHBoxLayout()
        widthLayout.addWidget(self.widthLabel)
        widthLayout.addWidget(self.widthLnEdt)
        
        heightLayout = QtWidgets.QHBoxLayout()
        heightLayout.addWidget(self.heightLabel)
        heightLayout.addWidget(self.heightLnEdt)
        
        arrayLengthLayout = QtWidgets.QHBoxLayout()
        arrayLengthLayout.addWidget(self.arrayLengthLabel)
        arrayLengthLayout.addWidget(self.arrayLengthLnEdt)
        
        blockHeightLayout = QtWidgets.QHBoxLayout()
        blockHeightLayout.addWidget(self.blockHeightLabel)
        blockHeightLayout.addWidget(self.blockHeightLnEdt)
        
        imgSizeLayout = QtWidgets.QHBoxLayout()
        imgSizeLayout.addWidget(self.imgSizeLabel)
        imgSizeLayout.addWidget(self.imgSizeLnEdt)
        
        alignmentLayout = QtWidgets.QHBoxLayout()
        alignmentLayout.addWidget(self.alignmentLabel)
        alignmentLayout.addWidget(self.alignmentLnEdt)
        
        chan1Layout = QtWidgets.QHBoxLayout()
        chan1Layout.addWidget(self.chan1Label)
        chan1Layout.addWidget(self.chan1LnEdt)
        
        chan2Layout = QtWidgets.QHBoxLayout()
        chan2Layout.addWidget(self.chan2Label)
        chan2Layout.addWidget(self.chan2LnEdt)
        
        chan3Layout = QtWidgets.QHBoxLayout()
        chan3Layout.addWidget(self.chan3Label)
        chan3Layout.addWidget(self.chan3LnEdt)
        
        chan4Layout = QtWidgets.QHBoxLayout()
        chan4Layout.addWidget(self.chan4Label)
        chan4Layout.addWidget(self.chan4LnEdt)
        
        imgTypeLayout = QtWidgets.QHBoxLayout()
        imgTypeLayout.addWidget(self.imgTypeLabel)
        imgTypeLayout.addWidget(self.imgTypeLnEdt)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setEnabled(False)
        self.comboBox.currentIndexChanged.connect(self.updateTexInfo)

        self.exportButton = QtWidgets.QPushButton()
        self.exportButton.setEnabled(False)
        self.exportButton.setText("Export")
        self.exportButton.clicked.connect(self.exportTex)

        self.exportAsButton = QtWidgets.QPushButton()
        self.exportAsButton.setEnabled(False)
        self.exportAsButton.setText("Export As")
        self.exportAsButton.clicked.connect(self.exportTexAs)

        self.exportAllButton = QtWidgets.QPushButton()
        self.exportAllButton.setEnabled(False)
        self.exportAllButton.setText("Export All")
        self.exportAllButton.clicked.connect(self.exportTexAll)
        
        exportLayout = QtWidgets.QHBoxLayout()
        exportLayout.addWidget(self.exportButton)
        exportLayout.addWidget(self.exportAsButton)
        exportLayout.addWidget(self.exportAllButton)

        self.injectButton = QtWidgets.QPushButton()
        self.injectButton.setEnabled(False)
        self.injectButton.setText("Replace")
        self.injectButton.clicked.connect(self.injectTex)

        fileLayout = QtWidgets.QVBoxLayout()
        fileLayout.addLayout(openLayout)
        fileLayout.addLayout(fnameLayout)
        fileLayout.addLayout(targetLayout)
        fileLayout.addWidget(self.Separator())
        fileLayout.addLayout(tileModeLayout)
        fileLayout.addLayout(dimLayout)
        fileLayout.addLayout(sparseBindingLayout)
        fileLayout.addLayout(sparseResidencyLayout)
        fileLayout.addLayout(swizzleLayout)
        fileLayout.addLayout(numMipsLayout)
        fileLayout.addLayout(numSamplesLayout)
        fileLayout.addLayout(formatLayout)
        fileLayout.addLayout(accessFlagsLayout)
        fileLayout.addLayout(widthLayout)
        fileLayout.addLayout(heightLayout)
        fileLayout.addLayout(arrayLengthLayout)
        fileLayout.addLayout(blockHeightLayout)
        fileLayout.addLayout(imgSizeLayout)
        fileLayout.addLayout(alignmentLayout)
        fileLayout.addLayout(chan1Layout)
        fileLayout.addLayout(chan2Layout)
        fileLayout.addLayout(chan2Layout)
        fileLayout.addLayout(chan3Layout)
        fileLayout.addLayout(chan4Layout)
        fileLayout.addLayout(imgTypeLayout)
        fileLayout.addWidget(self.Separator())
        fileLayout.addWidget(self.comboBox)
        fileLayout.addWidget(self.Separator())
        fileLayout.addLayout(exportLayout)
        fileLayout.addWidget(self.injectButton)

        self.createPreviewer()

        Layout = QtWidgets.QGridLayout()
        Layout.addWidget(self.Viewer, 0, 1)
        Layout.addLayout(fileLayout, 0, 0)
        self.setLayout(Layout)

        self.setLayout(Layout)

    def createPreviewer(self):
        self.Viewer = QtWidgets.QGroupBox("Preview")

        self.preview = QtWidgets.QLabel()
        self.resetPreviewer()

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(self.preview, 0, 0)
        self.Viewer.setLayout(mainLayout)

    def resetPreviewer(self):
        pix = QPixmap(333, 333)
        pix.fill(Qt.transparent)
        self.preview.setPixmap(pix)

    def prepareOpenFile(self, file):
        globals.fileData = bytearray()
        globals.texSizes = []
        self.BFRESPath = os.path.dirname(os.path.abspath(file))

        self.openLnEdt.setText(file)
        self.fnameLnEdt.setText('')
        self.targetLnEdt.setText('')
        self.tileModeLnEdt.setText('')
        self.dimLnEdt.setText('')
        self.sparseBindingLnEdt.setText('')
        self.sparseResidencyLnEdt.setText('')
        self.swizzleLnEdt.setText('')
        self.numMipsLnEdt.setText('')
        self.numSamplesLnEdt.setText('')
        self.formatLnEdt.setText('')
        self.accessFlagsLnEdt.setText('')
        self.widthLnEdt.setText('')
        self.heightLnEdt.setText('')
        self.arrayLengthLnEdt.setText('')
        self.blockHeightLnEdt.setText('')
        self.imgSizeLnEdt.setText('')
        self.alignmentLnEdt.setText('')
        self.chan1LnEdt.setText('')
        self.chan2LnEdt.setText('')
        self.chan3LnEdt.setText('')
        self.chan4LnEdt.setText('')
        self.imgTypeLnEdt.setText('')

        self.comboBox.setEnabled(False)
        self.exportButton.setEnabled(False)
        self.exportAsButton.setEnabled(False)
        self.exportAllButton.setEnabled(False)
        self.injectButton.setEnabled(False)

        self.comboBox.clear()

    def openFile(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "", "BNTX (*.bntx)")[0]
        if not file:
            return False

        self.prepareOpenFile(file)

        bntxfile = BNTX.read(file)
        if bntxfile:
            name, target, textures, texNames = bntxfile

            if textures:
                self.fnameLnEdt.setText(name)
                self.targetLnEdt.setText(target)
                self.textures = textures
                self.comboBox.addItems(texNames)

                self.comboBox.setEnabled(True)
                self.exportButton.setEnabled(True)
                self.exportAsButton.setEnabled(True)
                self.exportAllButton.setEnabled(True)
                self.injectButton.setEnabled(True)

                self.comboBox.setCurrentIndex(0)

    def updateTexInfo(self, index):
        tex = self.textures[index]

        if tex.tileMode in globals.tileModes:
            self.tileModeLnEdt.setText(globals.tileModes[tex.tileMode])

        else:
            self.tileModeLnEdt.setText(str(tex.tileMode))

        self.dimLnEdt.setText(str(tex.dim))
        self.sparseBindingLnEdt.setText(str(bool(tex.sparseBinding)))
        self.sparseResidencyLnEdt.setText(str(bool(tex.sparseResidency)))
        self.swizzleLnEdt.setText(str(tex.info.swizzle))
        self.numMipsLnEdt.setText(str(tex.numMips - 1))
        self.numSamplesLnEdt.setText(str(tex.info.numSamples))

        if tex.format in globals.formats:
            self.formatLnEdt.setText(globals.formats[tex.format])

        else:
            self.formatLnEdt.setText(hex(tex.format))

        if tex.info.accessFlags in globals.accessFlags:
            self.accessFlagsLnEdt.setText(globals.accessFlags[tex.info.accessFlags])

        else:
            self.accessFlagsLnEdt.setText(hex(tex.info.accessFlags))

        self.widthLnEdt.setText(str(tex.width))
        self.heightLnEdt.setText(str(tex.height))
        self.arrayLengthLnEdt.setText(str(tex.arrayLength))
        self.blockHeightLnEdt.setText(str(1 << tex.blockHeightLog2))
        self.imgSizeLnEdt.setText(str(tex.imageSize))
        self.alignmentLnEdt.setText(str(tex.alignment))
        self.chan1LnEdt.setText(globals.compSels[tex.compSel2[3]])
        self.chan2LnEdt.setText(globals.compSels[tex.compSel2[2]])
        self.chan3LnEdt.setText(globals.compSels[tex.compSel2[1]])
        self.chan4LnEdt.setText(globals.compSels[tex.compSel2[0]])
        self.imgTypeLnEdt.setText(globals.types[tex.type])

        self.updatePreview(tex)

    def updatePreview(self, tex):
        if tex.format in [0x101, 0x201, 0x301, 0x501, 0x701, 0x901, 0xb01, 0xb06, 0xe01, 0x1a01, 0x1a06, 0x1b01, 0x1b06, 0x1c01, 0x1c06, 0x1d01, 0x1d02, 0x1e01, 0x1e02]:
            result, _, _ = BNTX.decode(tex)

            if tex.format == 0x101:
                data = result[0]

                format_ = 'la4'
                bpp = 1

            elif tex.format == 0x201:
                data = result[0]

                format_ = 'l8'
                bpp = 1

            elif tex.format == 0x301:
                data = result[0]

                format_ = 'rgba4'
                bpp = 2

            elif tex.format == 0x501:
                data = result[0]

                format_ = 'rgb5a1'
                bpp = 2

            elif tex.format == 0x701:
                data = result[0]

                format_ = 'rgb565'
                bpp = 2

            elif tex.format == 0x901:
                data = result[0]

                format_ = 'la8'
                bpp = 2

            elif (tex.format >> 8) == 0xb:
                data = result[0]

                format_ = 'rgba8'
                bpp = 4

            elif tex.format == 0xe01:
                data = result[0]

                format_ = 'bgr10a2'
                bpp = 4

            elif (tex.format >> 8) == 0x1a:
                data = BNTX.bcn.decompressDXT1(result[0], tex.width, tex.height)

                format_ = 'rgba8'
                bpp = 4

            elif (tex.format >> 8) == 0x1b:
                data = BNTX.bcn.decompressDXT3(result[0], tex.width, tex.height)

                format_ = 'rgba8'
                bpp = 4

            elif (tex.format >> 8) == 0x1c:
                data = BNTX.bcn.decompressDXT5(result[0], tex.width, tex.height)

                format_ = 'rgba8'
                bpp = 4

            elif (tex.format >> 8) == 0x1d:
                data = BNTX.bcn.decompressBC4(result[0], tex.width, tex.height, 0 if tex.format & 3 == 1 else 1)

                format_ = 'rgba8'
                bpp = 4

            elif (tex.format >> 8) == 0x1e:
                data = BNTX.bcn.decompressBC5(result[0], tex.width, tex.height, 0 if tex.format & 3 == 1 else 1)

                format_ = 'rgba8'
                bpp = 4

            data = BNTX.dds.formConv.torgba8(tex.width, tex.height, bytearray(data), format_, bpp, list(reversed(tex.compSel2)))
            img = QImage(data, tex.width, tex.height, QImage.Format_RGBA8888)

            if tex.width >= tex.height:
                pix = QPixmap(img.scaledToWidth(333, Qt.SmoothTransformation))

            else:
                pix = QPixmap(img.scaledToHeight(333, Qt.SmoothTransformation))

            self.preview.setPixmap(pix)

        else:
            self.resetPreviewer()

    def exportTex(self):
        tex = self.textures[self.comboBox.currentIndex()]
        BNTX.extract(tex, self.BFRESPath, 0)

    def exportTexAs(self):
        tex = self.textures[self.comboBox.currentIndex()]
        BNTX.extract(tex, self.BFRESPath, 1)

    def exportTexAll(self):
        for tex in self.textures:
            BNTX.extract(tex, self.BFRESPath, 0, True)

    def injectTex(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "", "DDS (*.dds)")[0]
        if not file:
            return False

        index = self.comboBox.currentIndex()
        tex = self.textures[index]

        optionsDialog = QtWidgets.QDialog(self)
        optionsDialog.setWindowTitle("Options")

        tileModeLabel = QtWidgets.QLabel()
        tileModeLabel.setText("Tiling mode:")

        tileModeComboBox = QtWidgets.QComboBox()
        tileModeComboBox.addItems(["Optimal", "Linear"])

        if tex.tileMode in globals.tileModes:
            tileModeComboBox.setCurrentIndex(tex.tileMode)
        
        tileModeLayout = QtWidgets.QHBoxLayout()
        tileModeLayout.addWidget(tileModeLabel)
        tileModeLayout.addWidget(tileModeComboBox)

        SRGBLabel = QtWidgets.QLabel()
        SRGBLabel.setText("Use SRGB when possible:")

        SRGBCheckBox = QtWidgets.QCheckBox()
        SRGBCheckBox.setChecked(tex.format & 0xFF == 6)
        
        SRGBLayout = QtWidgets.QHBoxLayout()
        SRGBLayout.addWidget(SRGBLabel)
        SRGBLayout.addWidget(SRGBCheckBox)

        sparseBindingLabel = QtWidgets.QLabel()
        sparseBindingLabel.setText("Sparse Binding:")

        sparseBindingCheckBox = QtWidgets.QCheckBox()
        sparseBindingCheckBox.setChecked(bool(tex.sparseBinding))
        
        sparseBindingLayout = QtWidgets.QHBoxLayout()
        sparseBindingLayout.addWidget(sparseBindingLabel)
        sparseBindingLayout.addWidget(sparseBindingCheckBox)

        sparseResidencyLabel = QtWidgets.QLabel()
        sparseResidencyLabel.setText("Sparse Residency:")

        sparseResidencyCheckBox = QtWidgets.QCheckBox()
        sparseResidencyCheckBox.setChecked(bool(tex.sparseResidency))
        
        sparseResidencyLayout = QtWidgets.QHBoxLayout()
        sparseResidencyLayout.addWidget(sparseResidencyLabel)
        sparseResidencyLayout.addWidget(sparseResidencyCheckBox)

        importMipsLabel = QtWidgets.QLabel()
        importMipsLabel.setText("Import mipmaps if possible:")

        importMipsCheckBox = QtWidgets.QCheckBox()
        importMipsCheckBox.setChecked(False)
        
        importMipsLayout = QtWidgets.QHBoxLayout()
        importMipsLayout.addWidget(importMipsLabel)
        importMipsLayout.addWidget(importMipsCheckBox)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(optionsDialog.accept)
        buttonBox.rejected.connect(optionsDialog.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(tileModeLayout)
        layout.addLayout(SRGBLayout)
        layout.addLayout(sparseBindingLayout)
        layout.addLayout(sparseResidencyLayout)
        layout.addLayout(importMipsLayout)
        layout.addWidget(buttonBox)

        optionsDialog.setLayout(layout)

        if optionsDialog.exec_() != QtWidgets.QDialog.Accepted:
            return False

        tileMode = tileModeComboBox.currentIndex()
        SRGB = SRGBCheckBox.isChecked()
        sparseBinding = 1 if sparseBindingCheckBox.isChecked() else 0
        sparseResidency = 1 if sparseResidencyCheckBox.isChecked() else 0
        importMips = importMipsCheckBox.isChecked()

        oldImageSize = globals.texSizes[index]
        oldNumMips = tex.numMips

        tex_ = BNTX.inject(tex, tileMode, SRGB, sparseBinding, sparseResidency, importMips, oldImageSize, file)
        if tex_:
            self.textures[index] = tex_
            BNTX.writeTex(self.openLnEdt.text(), tex_, oldImageSize, oldNumMips)

            self.updateTexInfo(index)


def main():
    app = QtWidgets.QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
