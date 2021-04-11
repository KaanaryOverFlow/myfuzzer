#!/usr/bin/python
import sys
import os
import ayarlar
import create_case as cs
import time
import subprocess


try:
    raw = sys.argv[1].split(":") # pdf:google
    application = raw[1]
except:
    print("argv[1] eg. pdf:google")
    exit()

# Web server: apache
# /var/www/html/pdf linked pdf_output
# sudo ln -s `pwd`/pdf_outputs /var/www/html/pdf

adb = ayarlar.adbikili
devid = ayarlar.deviceid


def initalize(apps):
    subprocess.call([adb, "-s", devid, "wait-for-device"])
    try:
        for app in apps:
            subprocess.call([adb, "-s", devid, "shell", "am", "force-stop", app])
        print("initalize successfull")
    except:
        pass




def run(command):
    os.popen(command)

path = os.getcwd()
icase = path+"/pdf_files/" # input cases
ocase = path+"/pdf_outputs/" # output cases
pdf = cs.pdf(150,icase,ocase)

testnumber = 0

def clear():
    logargs = [adb, "-s", devid, 'logcat', '-c']
    subprocess.call(logargs)

def fuzz(application):
    global testnumber
    clear()
    identifer = pdf.get()
    url = f"http://192.168.1.106/pdf/{identifer}"
    print(f"Test sayisi: {testnumber}\t\t\t\t\tfile: {identifer}")
    if application == "google":
        argumans = args = [adb, "-s", devid, "shell"] + ayarlar.pdf_o_args["google"] + [url]
        subprocess.call([adb, "-s", devid, "shell", "am", "force-stop", "com.google.android.apps.pdfviewer"])
    out = subprocess.Popen(argumans, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    if ayarlar.debug:
#        print(out)
        print(" ".join(argumans))
    time.sleep(ayarlar.bekle)
    logargs = [adb, "-s", devid, 'logcat', '-d']
    logcat = subprocess.Popen(logargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    clear()
    if sum([i in logcat for i in ayarlar.crashids]) != 0:
        print("\n\n\n[+] Good. We have an crash :D\n\n\n")
        run(f"mv pdf_outputs/{identifer} crashes/")
    else:
        run(f"rm pdf_outputs/{identifer}")
    testnumber += 1

initalize(ayarlar.pdf_okuyucular)
while True:
    try:
        fuzz(application)
    except:
        print("cikiliyor")
        exit()


