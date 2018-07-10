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

import struct


class BNTXHeader(struct.Struct):
    def __init__(self, bom):
        super().__init__(bom + '8sIH2BI2H2I')

    def data(self, data, pos):
        (self.magic,
         self.version,
         self.bom,
         self.alignmentShift,
         self.targetAddrSize,
         self.fileNameAddr,
         self.flag,
         self.firstBlkAddr,
         self.relocAddr,
         self.fileSize) = self.unpack_from(data, pos)


class TexContainer(struct.Struct):
    def __init__(self, bom):
        super().__init__(bom + '4sI5qI4x')

    def data(self, data, pos):
        (self.target,
         self.count,
         self.infoPtrsAddr,
         self.dataBlkAddr,
         self.dictAddr,
         self.memPoolAddr,
         self.memPoolPtr,
         self.baseMemPoolAddr) = self.unpack_from(data, pos)


class BlockHeader(struct.Struct):
    def __init__(self, bom):
        super().__init__(bom + '4s2I4x')

    def data(self, data, pos):
        (self.magic,
         self.nextBlkAddr,
         self.blockSize) = self.unpack_from(data, pos)


class TextureInfo(struct.Struct):
    def __init__(self, bom):
        super().__init__(bom + '2B4H2x2I3i3I20x3IB3x8q')

    def data(self, data, pos):
        (self.flags,
         self.dim,
         self.tileMode,
         self.swizzle,
         self.numMips,
         self.numSamples,
         self.format_,
         self.accessFlags,
         self.width,
         self.height,
         self.depth,
         self.arrayLength,
         self.textureLayout,
         self.textureLayout2,
         self.imageSize,
         self.alignment,
         self.compSel,
         self.type_,
         self.nameAddr,
         self.parentAddr,
         self.ptrsAddr,
         self.userDataAddr,
         self.texPtr,
         self.texViewPtr,
         self.descSlotDataAddr,
         self.userDictAddr) = self.unpack_from(data, pos)


class TexInfo:
    pass
