#!/usr/bin/python
import sys
import os
import create_case as cs
path = os.getcwd()
pdf = cs.pdf(250,path+"/pdf_files/",path+"/pdf_outputs/")
print(pdf.get())
