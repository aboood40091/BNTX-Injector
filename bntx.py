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

import os.path
from PyQt5 import QtWidgets

from bytes import bytes_to_string
import dds
import bcn
import globals
from structs import struct, BNTXHeader, TexContainer, BlockHeader, TextureInfo, TexInfo

try:
    import pyximport; pyximport.install()
    import swizzle_cy as swizzle

except:
    import swizzle


DIV_ROUND_UP = swizzle.DIV_ROUND_UP
round_up = swizzle.round_up
pow2_round_up = swizzle.pow2_round_up


def read(file):
    with open(file, "rb") as inf:
        f = inf.read()

    pos = 0

    if f[0xc:0xe] == b'\xFF\xFE':
        bom = '<'

    elif f[0xc:0xe] == b'\xFE\xFF':
        bom = '>'

    else:
        QtWidgets.QMessageBox.warning(None, "Error", "Invalid BOM!")
        return False

    header = BNTXHeader(bom)
    header.data(f, pos)
    pos += header.size

    if header.magic != b'BNTX\0\0\0\0':
        QtWidgets.QMessageBox.warning(None, "Error", "Invalid file header!")
        return False

    fnameLen = struct.unpack(bom + 'H', f[header.fileNameAddr - 2:header.fileNameAddr])[0]
    fname = bytes_to_string(f[header.fileNameAddr:header.fileNameAddr + fnameLen], fnameLen)

    texContainer = TexContainer(bom)
    texContainer.data(f, pos)
    pos += texContainer.size

    if texContainer.target not in [b'NX  ', b'Gen ']:
        QtWidgets.QMessageBox.warning(None, "Error", "Unsupported target platform!")
        return False

    target = 0 if texContainer.target == b'Gen ' else 1

    textures = []
    texNames = []
    texSizes = []

    for i in range(texContainer.count):
        pos = struct.unpack(bom + 'q', f[texContainer.infoPtrsAddr + i * 8:texContainer.infoPtrsAddr + i * 8 + 8])[0]

        infoHeader = BlockHeader(bom)
        infoHeader.data(f, pos)
        pos += infoHeader.size

        info = TextureInfo(bom)
        info.data(f, pos)

        if infoHeader.magic != b'BRTI':
            continue

        nameLen = struct.unpack(bom + 'H', f[info.nameAddr:info.nameAddr + 2])[0]
        name = bytes_to_string(f[info.nameAddr + 2:info.nameAddr + 2 + nameLen], nameLen)

        compSel = []
        compSel2 = []
        for i in range(4):
            value = (info.compSel >> (8 * (3 - i))) & 0xff
            compSel2.append(value)
            if value == 0:
                value = 5 - len(compSel)

            compSel.append(value)

        if info.type_ not in globals.types:
            globals.types[info.type_] = "Unknown"

        dataAddr = struct.unpack(bom + 'q', f[info.ptrsAddr:info.ptrsAddr + 8])[0]
        mipOffsets = {0: 0}

        for i in range(1, info.numMips):
            mipOffset = struct.unpack(bom + 'q', f[info.ptrsAddr + (i * 8):info.ptrsAddr + (i * 8) + 8])[0]
            mipOffsets[i] = mipOffset - dataAddr

        tex = TexInfo()

        tex.infoAddr = pos
        tex.info = info
        tex.bom = bom
        tex.target = target

        tex.name = name

        tex.readTexLayout = info.flags & 1
        tex.sparseBinding = info.flags >> 1
        tex.sparseResidency = info.flags >> 2
        tex.dim = info.dim
        tex.tileMode = info.tileMode
        tex.numMips = info.numMips
        tex.width = info.width
        tex.height = info.height
        tex.format = info.format_
        tex.arrayLength = info.arrayLength
        tex.blockHeightLog2 = info.textureLayout & 7
        tex.imageSize = info.imageSize

        tex.compSel = compSel
        tex.compSel2 = compSel2

        tex.alignment = info.alignment
        tex.type = info.type_

        tex.mipOffsets = mipOffsets
        tex.dataAddr = dataAddr

        tex.data = f[dataAddr:dataAddr + info.imageSize]

        textures.append(tex)
        texNames.append(name)
        texSizes.append(info.imageSize)

    globals.fileData = bytearray(f)
    globals.texSizes = texSizes

    return fname, texContainer.target.decode('utf-8'), textures, texNames


def decode(tex):
    if (tex.format >> 8) in globals.blk_dims:
        blkWidth, blkHeight = globals.blk_dims[tex.format >> 8]

    else:
        blkWidth, blkHeight = 1, 1

    bpp = globals.bpps[tex.format >> 8]

    result_ = []

    linesPerBlockHeight = (1 << tex.blockHeightLog2) * 8
    blockHeightShift = 0

    for mipLevel in tex.mipOffsets:
        width = max(1, tex.width >> mipLevel)
        height = max(1, tex.height >> mipLevel)

        size = DIV_ROUND_UP(width, blkWidth) * DIV_ROUND_UP(height, blkHeight) * bpp

        if pow2_round_up(DIV_ROUND_UP(height, blkHeight)) < linesPerBlockHeight:
            blockHeightShift += 1

        mipOffset = tex.mipOffsets[mipLevel]

        result = swizzle.deswizzle(
            width, height, blkWidth, blkHeight, tex.target, bpp, tex.tileMode,
            max(0, tex.blockHeightLog2 - blockHeightShift), tex.data[mipOffset:],
        )

        result_.append(result[:size])

    return result_, blkWidth, blkHeight


def extract(tex, BFRESPath, exportAs, dontShowMsg=False):
    if tex.format in globals.formats and tex.dim == 2 and tex.arrayLength < 2 and tex.tileMode in globals.tileModes:
        if tex.format == 0x101:
            format_ = "la4"

        elif tex.format == 0x201:
            format_ = "l8"

        elif tex.format == 0x301:
            format_ = "rgba4"

        elif tex.format == 0x401:
            format_ = "abgr4"

        elif tex.format == 0x501:
            format_ = "rgb5a1"

        elif tex.format == 0x601:
            format_ = "a1bgr5"

        elif tex.format == 0x701:
            format_ = "rgb565"

        elif tex.format == 0x801:
            format_ = "bgr565"

        elif tex.format == 0x901:
            format_ = "la8"

        elif (tex.format >> 8) == 0xb:
            format_ = "rgba8"

        elif (tex.format >> 8) == 0xc:
            format_ = "bgra8"

        elif tex.format == 0xe01:
            format_ = "bgr10a2"

        elif (tex.format >> 8) == 0x1a:
            format_ = "BC1"

        elif (tex.format >> 8) == 0x1b:
            format_ = "BC2"

        elif (tex.format >> 8) == 0x1c:
            format_ = "BC3"

        elif tex.format == 0x1d01:
            format_ = "BC4U"

        elif tex.format == 0x1d02:
            format_ = "BC4S"

        elif tex.format == 0x1e01:
            format_ = "BC5U"

        elif tex.format == 0x1e02:
            format_ = "BC5S"

        elif tex.format == 0x1f05:
            format_ = "BC6H_SF16"

        elif tex.format == 0x1f0a:
            format_ = "BC6H_UF16"

        elif (tex.format >> 8) == 0x20:
            format_ = "BC7"

        elif tex.format == 0x3b01:
            format_ = "bgr5a1"

        result_, blkWidth, blkHeight = decode(tex)

        if exportAs:
            if (tex.format >> 8) in globals.ASTC_formats:
                file = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "ASTC (*.astc)")[0]

            else:
                file = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "DDS (*.dds)")[0]

            if not file:
                return False

        elif (tex.format >> 8) in globals.ASTC_formats:
            file = os.path.join(BFRESPath, tex.name + '.astc')

        else:
            file = os.path.join(BFRESPath, tex.name + '.dds')

        if (tex.format >> 8) in globals.ASTC_formats:
            outBuffer = b''.join([
                b'\x13\xAB\xA1\x5C', blkWidth.to_bytes(1, "little"),
                blkHeight.to_bytes(1, "little"), b'\1',
                tex.width.to_bytes(3, "little"),
                tex.height.to_bytes(3, "little"), b'\1\0\0',
                result_[0],
            ])

            with open(file, "wb+") as output:
                output.write(outBuffer)

        else:
            hdr = dds.generateHeader(
                tex.numMips, tex.width, tex.height, format_, list(reversed(tex.compSel)),
                len(result_[0]), (tex.format >> 8) in globals.BCn_formats,
            )

            with open(file, "wb+") as output:
                output.write(b''.join([hdr, b''.join(result_)]))

    elif not dontShowMsg:
        msg = "Can't convert: " + tex.name

        if tex.format not in globals.formats:
            context = "Unsupported format."

        elif tex.tileMode not in globals.tileModes:
            context = "Unsupported tiling mode."

        elif tex.dim != 2:
            context = "Unsupported image storage dimension."

        else:
            context = "Unsupported array length."

        QtWidgets.QMessageBox.warning(None, "Error", '\n'.join([msg, context]))
        return False


def getCurrentMipOffset_Size(width, height, blkWidth, blkHeight, bpp, currLevel):
    offset = 0

    for mipLevel in range(currLevel):
        width_ = DIV_ROUND_UP(max(1, width >> mipLevel), blkWidth)
        height_ = DIV_ROUND_UP(max(1, height >> mipLevel), blkHeight)

        offset += width_ * height_ * bpp

    width_ = DIV_ROUND_UP(max(1, width >> currLevel), blkWidth)
    height_ = DIV_ROUND_UP(max(1, height >> currLevel), blkHeight)

    size = width_ * height_ * bpp

    return offset, size


def inject(tex, tileMode, SRGB, sparseBinding, sparseResidency, importMips, oldImageSize, f):
    width, height, format_, fourcc, dataSize, compSel, numMips, data = dds.readDDS(f, SRGB)

    if 0 in [width, dataSize] and data == []:
        QtWidgets.QMessageBox.warning(None, "Error", "Unsupported DDS file!")
        return False

    if format_ not in globals.formats:
        QtWidgets.QMessageBox.warning(None, "Error", "Unsupported DDS format!")
        return False

    if not importMips:
        numMips = 1

    else:
        if tex.numMips < numMips + 1:
            QtWidgets.QMessageBox.warning(
                None, "Warning",
                "This DDS file has more mipmaps (%d) than the original image (%d)!"
                "\n%d mipmaps will be imported." % (numMips, tex.numMips - 1, tex.numMips - 1),
            )

        numMips = max(1, min(tex.numMips, numMips + 1))

    if tileMode == 1:
        alignment = 1

    else:
        alignment = 512

    if (format_ >> 8) in globals.blk_dims:
        blkWidth, blkHeight = globals.blk_dims[format_ >> 8]

    else:
        blkWidth, blkHeight = 1, 1

    bpp = globals.bpps[format_ >> 8]

    if tileMode == 1:
        blockHeight = 1
        blockHeightLog2 = 0

        linesPerBlockHeight = 1

    else:
        blockHeight = swizzle.getBlockHeight(DIV_ROUND_UP(height, blkHeight))
        blockHeightLog2 = len(bin(blockHeight)[2:]) - 1

        linesPerBlockHeight = blockHeight * 8

    blockHeightShift = 0
    surfSize = 0

    for mipLevel in range(numMips):
        width_ = DIV_ROUND_UP(max(1, width >> mipLevel), blkWidth)
        height_ = DIV_ROUND_UP(max(1, height >> mipLevel), blkHeight)

        dataAlignBytes = b'\0' * (round_up(surfSize, alignment) - surfSize)
        surfSize += len(dataAlignBytes)

        if tileMode == 1:
            pitch = width_ * bpp

            if tex.target == 1:
                pitch = round_up(pitch, 32)

            surfSize += pitch * height_

        else:
            if pow2_round_up(height_) < linesPerBlockHeight:
                blockHeightShift += 1

            pitch = round_up(width_ * bpp, 64)
            surfSize += pitch * round_up(height_, max(1, blockHeight >> blockHeightShift) * 8)

    if surfSize > oldImageSize:
        QtWidgets.QMessageBox.warning(
            None, "Error",
            'This DDS has a larger filesize than the original image!'
            '\nFor lowest filesize possible, use tiling mode "Linear".',
        )

        return False

    result = []
    surfSize = 0
    mipOffsets = {}
    blockHeightShift = 0

    for mipLevel in range(numMips):
        offset, size = getCurrentMipOffset_Size(width, height, blkWidth, blkHeight, bpp, mipLevel)
        data_ = data[offset:offset + size]

        width_ = max(1, width >> mipLevel)
        height_ = max(1, height >> mipLevel)

        width__ = DIV_ROUND_UP(width_, blkWidth)
        height__ = DIV_ROUND_UP(height_, blkHeight)

        dataAlignBytes = b'\0' * (round_up(surfSize, alignment) - surfSize)
        surfSize += len(dataAlignBytes)
        mipOffsets[mipLevel] = surfSize

        if tileMode == 1:
            pitch = width__ * bpp

            if tex.target == 1:
                pitch = round_up(pitch, 32)

            surfSize += pitch * height__

        else:
            if pow2_round_up(height__) < linesPerBlockHeight:
                blockHeightShift += 1

            pitch = round_up(width__ * bpp, 64)
            surfSize += pitch * round_up(height__, max(1, blockHeight >> blockHeightShift) * 8)

        result.append(bytearray(dataAlignBytes) + swizzle.swizzle(
            width_, height_, blkWidth, blkHeight, tex.target, bpp, tileMode,
            max(0, blockHeightLog2 - blockHeightShift), data_,
        ))

    tex.readTexLayout = 1 if tileMode == 0 else 0
    tex.sparseBinding = sparseBinding
    tex.sparseResidency = sparseResidency
    tex.dim = 2
    tex.tileMode = tileMode
    tex.numMips = numMips
    tex.mipOffsets = mipOffsets
    tex.width = width
    tex.height = height
    tex.format = format_
    tex.accessFlags = 0x20
    tex.arrayLength = 1
    tex.blockHeightLog2 = blockHeightLog2
    tex.imageSize = surfSize
    tex.compSel = compSel; tex.compSel.reverse()
    tex.compSel2 = tex.compSel.copy()
    tex.alignment = alignment
    tex.type = 1
    tex.data = b''.join(result)

    return tex


def writeTex(file, tex, oldImageSize, oldNumMips):
    compSel = tex.compSel[0] << 24 | tex.compSel[1] << 16 | tex.compSel[2] << 8 | tex.compSel[3]

    if not tex.readTexLayout:
        textureLayout = 0

    else:
        textureLayout = tex.sparseResidency << 5 | tex.sparseBinding << 4 | tex.blockHeightLog2

    infoHead = TextureInfo(tex.bom).pack(
        tex.sparseResidency << 2 | tex.sparseBinding << 1 | tex.readTexLayout,
        tex.dim,
        tex.tileMode,
        tex.info.swizzle,
        tex.numMips,
        tex.info.numSamples,
        tex.format,
        tex.info.accessFlags,
        tex.width,
        tex.height,
        tex.info.depth,
        tex.arrayLength,
        textureLayout,
        tex.info.textureLayout2,
        tex.imageSize,
        tex.alignment,
        compSel,
        tex.type,
        tex.info.nameAddr,
        tex.info.parentAddr,
        tex.info.ptrsAddr,
        tex.info.userDataAddr,
        tex.info.texPtr,
        tex.info.texViewPtr,
        tex.info.descSlotDataAddr,
        tex.info.userDictAddr,
    )

    globals.fileData[tex.infoAddr:tex.infoAddr + 144] = infoHead

    ptrs = bytearray(oldNumMips * 8)

    for mipLevel in tex.mipOffsets:
        mipOffset = tex.mipOffsets[mipLevel]
        ptrs[mipLevel * 8:mipLevel * 8 + 8] = struct.pack(tex.bom + 'q', tex.dataAddr + mipOffset)

    globals.fileData[tex.info.ptrsAddr:tex.info.ptrsAddr + oldNumMips * 8] = ptrs

    data = b''.join([tex.data, b'\0' * (oldImageSize - tex.imageSize)])
    globals.fileData[tex.dataAddr:tex.dataAddr + oldImageSize] = data

    with open(file, "wb+") as out:
        out.write(globals.fileData)
