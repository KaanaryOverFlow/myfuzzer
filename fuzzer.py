#!/usr/bin/python
import sys
import os
import threading as th
import create_case as cs
import time
import subprocess

# Web server: apache
# /var/www/html/pdf linked pdf_output
# sudo ln -s `pwd`/pdf_outputs /var/www/html/pdf
adb = "/usr/bin/adb"


def run(command):
    os.popen(command)

path = os.getcwd()
icase = path+"/pdf_files/" # input cases
ocase = path+"/pdf_outputs/" # output cases
pdf = cs.pdf(250,icase,ocase)

testnumber = 0

def fuzz():
    global testnumber
    run("adb logcat -c")
#    run("adb shell input keyevent 82")
    identifer = pdf.get()
    print(f"Test sayisi: {testnumber} \t\t\t\tfile: {identifer}")
    google_pdf = f'adb shell "am start -a application/pdf -n com.google.android.apps.pdfviewer/com.google.android.apps.viewer.PdfViewerActivity -t application/pdf -d http://192.168.1.106/pdf/{identifer}"'
    run(google_pdf)
    close = "adb shell am force-stop com.google.android.apps.pdfviewer"
    time.sleep(0.01)
    run(close)
    logargs = [adb, 'logcat', '-d']
    logcat = subprocess.Popen(logargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    logargs = [adb, 'logcat', '-c']
    subprocess.call(logargs)
    if b"SIGSEGV" in logcat or b"SIGFPE" in logcat or b"SIGILL" in logcat or b"sigsegv" in logcat or b"sigfpe" in logcat or b"sigill" in logcat:
        print("\n\n\n[+] Good. We have an crash :D\n\n\n")
        run(f"mv pdf_outputs/{identifer} crashes/")
    else:
        run(f"rm pdf_outputs/{identifer}")
    testnumber += 1


while True:
    fuzz()




