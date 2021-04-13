#!/usr/bin/python
import sys
import os
import ayarlar
import create_case as cs
import time
import subprocess


try:
    raw = sys.argv[1].split(":") # pdf:google
    uzanti = raw[0]
    application = raw[1]
    chatmi = raw[2]
    assert chatmi == "0" or chatmi == "1"
except:
    print("argv[1] eg. pdf:google:0 or gif:signal:1 (if is a chat app then is 1 else 0)")
    exit()

# Web server: apache
# /var/www/html/pdf linked pdf_output
# sudo ln -s `pwd`/pdf_outputs /var/www/html/pdf
# sudo ln -s `pwd`/gif_o /var/www/html/gif

adb = ayarlar.adbikili
devid = ayarlar.deviceid
path = os.getcwd()
testnumber = 0

def run(command):
    os.popen(command)

def initalizegifsignal():
    subprocess.call([adb, "-s", devid, "wait-for-device"])
    subprocess.call([adb, "-s", devid, "shell", "am", "force-stop", "org.thoughtcrime.securesms"])
    subprocess.call([adb, "-s", devid, "shell", "rm", "/storage/emulated/0/Pictures/*"])
    subprocess.call([adb, "-s", devid, "shell", "monkey", "-p", "org.thoughtcrime.securesms", "1"])
    input("press enter after pass lock and login chat screen")
    print("initalization successfull")

def initalizepdfgoogle(apps):
    subprocess.call([adb, "-s", devid, "wait-for-device"])
    try:
        for app in apps:
            subprocess.call([adb, "-s", devid, "shell", "am", "force-stop", app])
        print("initalize successfull")
    except:
        pass

def clear():
    logargs = [adb, "-s", devid, 'logcat', '-c']
    subprocess.call(logargs)

def fuzzgifforsignal(gen):
    global testnumber
    identifer = gen.get("gif")
    print(f"Test sayisi: {testnumber}\t\t\t\t\tFile: {identifer}")
    subprocess.call([adb, "-s", devid, "push", f"gif_o/{identifer}", "/storage/emulated/0/Pictures/"])
    time.sleep(0.1)
    subprocess.call([adb, "-s", devid, "shell", "input", "tap", "980","1730"]) # press +
    time.sleep(0.1)
    subprocess.call([adb, "-s", devid, "shell", "input", "tap", "580","1675"]) # select file
    time.sleep(0.1)
    clear()
    subprocess.call([adb, "-s", devid, "shell", "input", "tap", "380","530"]) # press file
    time.sleep(0.1)
    subprocess.call([adb, "-s", devid, "shell", "input", "tap", "980","1730"]) # press send
    time.sleep(ayarlar.bekle)
    logargs = [adb, "-s", devid, 'logcat', '-d']
    logcat = subprocess.Popen(logargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    if sum([i in logcat for i in ayarlar.crashids]) != 0:
        print("\n\n\n[ ^-^ ] We have an crash.\n\n\n")
        run(f"mv gif_o/{identifer} crashes/")
        open(f"crashes/{identifer}.log", "wb").write(logcat)
    else:
        run(f"rm gif_o/{identifer}")
        subprocess.call([adb, "-s", devid, "shell", "rm", f"/storage/emulated/0/Pictures/{identifer}"]) # press send
    testnumber += 1


def signalgiffuzz():
    initalizegifsignal()
    gifgen = cs.creator(800,path+"/gif_i/",path+"/gif_o/")
    while True:
        try:
            fuzzgifforsignal(gifgen)
        except:
            print("cikiliyor")
            break

def fuzzp(pdf, application):
    global testnumber
    clear()
    identifer = pdf.get("pdf")
    url = f"http://192.168.1.106/pdf/{identifer}"
    print(f"Test sayisi: {testnumber}\t\t\t\t\tfile: {identifer}")
    if application == "google":
        argumans = args = [adb, "-s", devid, "shell"] + ayarlar.pdf_o_args["google"] + [url]
        subprocess.call([adb, "-s", devid, "shell", "am", "force-stop", "com.google.android.apps.pdfviewer"])
    out = subprocess.Popen(argumans, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    time.sleep(ayarlar.bekle)
    logargs = [adb, "-s", devid, 'logcat', '-d']
    logcat = subprocess.Popen(logargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    if ayarlar.debug:
        print(lotcat)
    clear()
    if sum([i in logcat for i in ayarlar.crashids]) != 0:
        print("\n\n\n[+] Good. We have an crash :D\n\n\n")
        run(f"mv pdf_outputs/{identifer} crashes/")
    else:
        run(f"rm pdf_outputs/{identifer}")
    testnumber += 1


def pdffuzz():
    icase = path+"/pdf_files/" # input cases
    ocase = path+"/pdf_outputs/" # output cases
    pdf = cs.creator(900,icase,ocase)
    initalizepdfgoogle(ayarlar.pdf_okuyucular)
    while True:
        try:
            fuzzp(pdf, application)
        except:
            print("cikiliyor")
            break

if chatmi == "0":
    if uzanti == "pdf":
        pdffuzz()
elif chatmi == "1":
    signalgiffuzz()



