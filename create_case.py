#!/usr/bin/python
import os
import random as R
import math

class pdf():
    def __init__(self,number,ipath,opath):
        self.number = number
        self.ipath = ipath
        self.opath = opath

    def get(self):
        ifile = self.ipath + R.choice(os.listdir(self.ipath))
        bytelar = bytearray(open(ifile, "rb").read())
        numara = R.randrange(math.ceil((float(len(bytelar)) / self.number))) + 1
        for _ in range(numara):
            rbyte = R.randrange(256)
            index = R.randrange(len(bytelar))
            bytelar[index] = rbyte
        identifer = "".join([R.choice("0123456789abcedf") for i in range(40)])
        newpath = self.opath+identifer+".pdf"
        open(newpath, "wb+").write(bytelar)
        return newpath


