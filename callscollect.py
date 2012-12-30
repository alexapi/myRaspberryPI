#!/usr/bin/python
# -*- coding: utf-8
import re
import string
#import serial
import sqlite3
#ser = serial.Serial("/dev/ttyUSB0", 9600, rtscts=1)

def am_24h(c_time):
    c_time = c_time.replace("AM", "")
    tmparr = c_time.split(":")
    hh = int(tmparr[0].strip())
    if hh == 12:
       hh = "00"
    if hh <= 9:
       hh = "0" + str(hh)
    c_time  = str(hh) + ":" + tmparr[1]
    return c_time

def pm_24h(c_time):
    c_time = c_time.replace("PM", "")
    tmparr = c_time.split(":")
    hh = int(tmparr[0])
    if hh < 12:
       hh = hh + 12
    c_time  = str(hh) + ":" + tmparr[1]
    return c_time

def parse_line(myline):
    myline = myline.strip()
    myline = myline.replace("'", ":")
    myline = myline.replace("<    ", "")
    myline = myline.replace("    >", "")
    myline = myline.replace("/ ", "/0")
    myline = myline.replace("*", "1 ")
    if myline[9] != "1":
       myline = myline[0:9] + "0 " + myline[10:]
    myline = re.sub("\s+", " ", myline)
    myarray = myline.split(" ")
    idat = myarray[0]
    adat = idat.split("/")
    iday = int(adat[1])
    imonth = int(adat[0])
    iyear = 2000+int(adat[2])
    itr = myarray[1]
    itime = myarray[2]
    if itime.find("AM") != -1:
       itime = str(am_24h(itime))
    if itime.find("PM") != -1:
       itime = str(pm_24h(itime))
    iext = str(myarray[3])
    icol = str(myarray[4])
    inum = str(myarray[5])
    idur = myarray[6]
    adur = idur.split(":")
    idur = int(adur[0])*3600+int(adur[1])*60+int(adur[2])
    icod = str(myarray[7])
    return iday, imonth, iyear, itr, itime, iext, icol, inum, idur, icod

#myline = "--------------------------------------------------------------------------------"
#myline = "  Date      Time  Ext. CO      Dial number                      Duration  Code  "
myline = "12/17/12 * 7:56PM  14  07   0501111112                          00:14'13  ....  "


lerror = 0

if len(myline) < 80 or myline.find("Ext.") != -1 or myline.find("-") != -1:
    lerror = 1
    print "Error in string detected"

if lerror == 0:
    myline = parse_line(myline)
    print myline
    pbxdb = sqlite3.connect("/tmp/pbxcollect.db")
    curs = pbxdb.cursor()
    # Create new table
    #curs.execute("CREATE TABLE calls (cday integer(2) NOT NULL, cmonth integer(2) NOT NULL, cyear integer(4) NOT NULL, transfer text(1) NOT NULL, ctime text(5) NOT NULL, intline text(3) NOT NULL, coline text(2) NOT NULL, phonenum text(12) NOT NULL, colduration integer(5) NOT NULL, colcode text(4) NOT NULL)")
    # Insert new records to the table
    curs.execute('INSERT INTO calls VALUES (?,?,?,?,?,?,?,?,?,?)',myline)
#    for rows in curs.execute("SELECT * FROM calls ORDER BY cyear, cmonth, cday, ctime"):
#        print str(rows[0]) + "." + str(rows[1]) + "." + str(rows[2]), rows[3], rows[4], rows[5], rows[6], rows[7], rows[8]
    
    pbxdb.commit()
    pbxdb.close()
    print "OK"










