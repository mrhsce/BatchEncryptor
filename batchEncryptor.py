#!/usr/bin/env python3.4
###########################################################################
# MM          MM            HH      HH                  CCCCCCC  EEEEEEEE #
# MMMMM     MMMM  rr  rr    HH      HH     ssss        C         E        #
# MM  MM  MM  MM  rrrr  rr  HHHHHHHHHH  ss            C          EEEEEEEE #
# MM    MM    MM  rrr       HHHHHHHHHH    s           C          EEEEEEEE #
# MM          MM  rr        HH      HH     s  ss       C         E        #
# MM          MM  rr        HH      HH  sssss           CCCCCCC  EEEEEEEE #
###########################################################################
##                        Written in python 3.4
'''Program number: 61 Date: 25/2/2015 DtD: 350 Copyright:(c)MrHs 2015'''
#Comment :This is a script for batch encrypting the source code used when 
#	uploading code in unsafe environments and also when transferring through unsafe passages
import os
import random
from Crypto.Cipher import AES
import base64
from shutil import copyfile
import sys
import urllib.parse


valErrCount=0

def encryption(case,publicKey,rawText): # publicKey and case are integer    
    
    PADDING = ' '
    BLOCK_SIZE = 32
    
    pad = lambda s: s + (BLOCK_SIZE - (len(s)) % BLOCK_SIZE) * PADDING
    #prepare crypto method
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s))).decode("utf-8")
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).decode("utf-8").rstrip(PADDING)
    cipher = AES.new(publicKey)
    
    encText=""
    ENCRYPT_THE_MESSAGE=1
    if case==ENCRYPT_THE_MESSAGE:
        while(rawText!=""):
            try:
                encText+=EncodeAES(cipher,quote(rawText.partition("\n")[0],ENCRYPT_THE_MESSAGE))+'\n' 
            except ValueError:
                valErrCount+=1
                print("Unknown character error....")                    
            rawText=rawText.partition('\n')[2]   
    DECRYPT_THE_MESSAGE=2
    if case==DECRYPT_THE_MESSAGE:
        while(rawText!=""):
            encText+=quote(DecodeAES(cipher,rawText.partition("\n")[0]),DECRYPT_THE_MESSAGE)+'\n' 
            rawText=rawText.partition('\n')[2]            
    
    return(encText)

def quote(rawText,case):
    ENCRYPT_THE_MESSAGE=1
    DECRYPT_THE_MESSAGE=2
    SPECIAL_SEQUENCE = "%*.Quoted-->"
    if(len(rawText)==0):
        return rawText
    if(case==ENCRYPT_THE_MESSAGE and (sys.getsizeof(rawText)-sys.getsizeof(""))/(len(rawText))>1):
        return str(SPECIAL_SEQUENCE + urllib.parse.quote(rawText))
    if(case==DECRYPT_THE_MESSAGE and rawText.startswith(SPECIAL_SEQUENCE)):
        return str(urllib.parse.unquote(rawText.partition(SPECIAL_SEQUENCE)[2]))
    else:
        return rawText

def file(name,copy=False):
    if(copy==True):
        copyfile(srcAdr+name, dstAdr+name)      
        return(0)
    currAdr=os.getcwd()
    os.chdir(srcAdr+'/'+name.rpartition('/')[0])
    fileSrc=open(name.rpartition('/')[2],'r')
    rawText=(fileSrc.readlines())
    fileSrc.close()
    os.chdir(dstAdr+'/'+name.rpartition('/')[0])
    fileDst=open(name.rpartition('/')[2],'w')
    for iii in rawText:                
        fileDst.writelines(encryption(case, publicKey, iii))
               
    fileDst.close()
    os.chdir(currAdr)

def folder(name):
    currAdr=os.getcwd()   
    try:
        os.chdir(dstAdr+'/'+name.rpartition('/')[0])      
        if(not os.path.exists(name.rpartition('/')[2])):
            os.mkdir(name.rpartition('/')[2])
    except os.error as e:
                    file(name,True)
    os.chdir(currAdr)
def iterate():
    currAdr=os.getcwd()
    print("Addr:")
    print(currAdr)
    for i in os.listdir(): 
        print(i)       
        if(os.path.isfile(os.path.join(currAdr,i))):
            if(i.rpartition(".")[2] in extensions):
                file(currAdr.partition(srcAdr)[2]+'/'+i)
            else:                  
                file(currAdr.partition(srcAdr)[2]+'/'+i,True)
        if(os.path.isdir(os.path.join(currAdr,i))):
            folder(currAdr.partition(srcAdr)[2]+'/'+i)
            os.chdir(currAdr+'/'+i)
            iterate() 
    print("end")        
    os.chdir(currAdr)
if __name__ == '__main__':
    if(len(sys.argv)>1):
        directory= sys.argv[1]
    else:               
        directory=input("Please insert the directory : ")    
    extensions="txt cpp h xml java py md php html js"       
    extensions=extensions.split(" ")
    
    if( len(sys.argv)>2):
        publicKey= sys.argv[2]
    else:               
        publicKey=input("Please insert the key : ")
    random.seed(publicKey)
    publicKey=''
    for jjj in range(16):
        publicKey+=str(random.randrange(0,9))
    
    if(directory.endswith("/")): # This is to prevent from having a slash at the end of the address
        directory = directory.rpartition("/")[0]

    if( directory.endswith("-enc")):
        case=2
    else:
        case=1
    
    
    #For linux
    TYPE_LOCAL=0
    TYPE_GLOBAL=1
    if(not directory.startswith("/home/")):
        type=TYPE_LOCAL
        srcAdr=os.getcwd()+'/'+directory
        if(case==1):
            dstAdr=os.getcwd()+'/'+directory+"-enc"
            print(os.path.exists(dstAdr))
            if(not os.path.exists(dstAdr)):
                os.mkdir(dstAdr)
        if(case==2):
            dstAdr=os.getcwd()+'/'+directory.rpartition("-enc")[0]
            if(not os.path.exists(dstAdr)):
                os.mkdir(dstAdr) 
            
    else:
        type=TYPE_GLOBAL
        srcAdr=directory
        if(case==1):
            dstAdr=directory+"-enc"
            if(not os.path.exists(dstAdr)):
                os.mkdir(dstAdr)
        if(case==2):
            dstAdr=directory.rpartition("-enc")[0]
            if(not os.path.exists(dstAdr)):
                os.mkdir(dstAdr)
              
    print("Destination: ") 
    print(dstAdr)   
    os.chdir(srcAdr)
    iterate()
    print("%s ValueError(s) happened......."%valErrCount)  
