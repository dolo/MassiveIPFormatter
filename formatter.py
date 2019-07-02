#!/usr/bin/python
#coding:utf-8
import os
import sys
import re
import time


# grab txt files in spesfic dir
def getDirList(p):
    files = os.listdir(p)
    txts = []
    for f in files:
        file_post = str(f.split('.')[-1])
        if(file_post == "txt"):
            txts.append(f)
    return txts


def writeFile(filename, data):
    file_write_obj = open("\\output\\" + filename, 'w')
    for var in data:
        file_write_obj.writelines(var)
        file_write_obj.writelines("\n")
    file_write_obj.close()


# detect ip address format
def isIPAddress(str):
    ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if ip.match(str):
        return True
    else:
        return False


# detect public address
def isPublicAddress(str):
    illigal = re.compile('^(127\.0\.0\.1)|(localhost)|(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|(172\.((1[6-9])|(2\d)|(3[01]))\.\d{1,3}\.\d{1,3})|(192\.168\.\d{1,3}\.\d{1,3})$')
    if illigal.match(str):
        return False
    else:
        return True


# detect network/broadcast address
def isHostAddress(str):
    ip_split_list = str.strip().split('.')
    if 4 != len(ip_split_list):
        return False
    try:
        ip_split_list[3] = int(ip_split_list[3])
    except:
        print("IP invalid:" + str)
        return False
    if(ip_split_list[3] < 255 and ip_split_list[3] > 0):
        return True
    else:
        return False


def removeChinese(strdata):
    chinese = re.compile(r'[^\x00-\x7f]')
    nochinese = re.sub(chinese, '', strdata)
    if(nochinese is not None):
        return(nochinese)


def removeEnglish(strdata):
    English = re.compile(r'[a-zA-Z]+')
    noEnglish = re.sub(English, '', str(strdata))
    if(noEnglish is not None):
        return(noEnglish)


def removeSymbol(strdata):
    strdata = strdata.replace(' ', '')
    return strdata


def multipleParse(filelist):
    for province in filelist:
        print("[+]parsing " + str(province))
        newParse(str(province))


def newParse(province):
    start = time.time()
    postIPList = []
    file = open(province, "r", encoding = 'utf-8')
    for line in file:
        line = removeChinese(line)
        line = str(line).replace('/', ',')
        line = str(line).replace(';', ',')
        line = str(line).replace('-', ',')
        line = str(line).replace('\r\n', '')
        line = str(line).replace('\n', '')
        splitResult = splitMultiIP(line, ',')
        if isinstance(splitResult, list):
            postIPList.extend(splitResult)
        else:
            postIPList.append(splitResult)
    IPList = []
    for postIP in postIPList:
        postIP = removeEnglish(postIP)
        postIP = removeSymbol(postIP)
        if(isIPAddress(postIP) and isPublicAddress(postIP) and isHostAddress(postIP)):
            IPList.append(postIP)
        # else:
            # print("[*]illegal address: " + postIP)
    writeFile(province, IPList)
    operationTime = time.time()-start
    print("[+]parse complete [" + province + "] " + str(len(IPList)) + " records found in " + str('%.2f' % operationTime) + "s")


def splitMultiIP(strData, symbol):
    if(symbol in strData):
        sline = strData.split(symbol)
        return sline
    else:
        return strData


def runRelease():
    print("[*]dolo ip address parser 0.2")
    if(len(sys.argv) == 2):
        if(".txt" in sys.argv[1]):
            print("[+]found txt file, run single file parse...")
            newParse(sys.argv[1])
        if("\\" in sys.argv[1]):
            print("[+]found directory, run multiple file parse...")
            os.chdir(sys.argv[1])
            multipleParse(getDirList(sys.argv[1]))
    else:
        print("[*]usage: python formatter.py [syntax]")
        print("[*]syntax = single filename(txt) or directory with multiple txt files")


if __name__ == "__main__":
    runRelease()
