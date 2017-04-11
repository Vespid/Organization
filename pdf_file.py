# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 08:47:53 2017

@author: Vincent
"""
import re,os,string,shutil
#user inputs
text="do\\eatshit\\myudog\\7052001_Rev NC.pdf"
inputDir=os.path.join("F:",os.sep,"Programming","Test","SortReady")
outputDir=os.path.join("F:",os.sep,"Programming","Test","PDF_Sorted")
#----------------------------------------------------------------
#Check if path of file exists and creates it if nonexistant
def create_path(filepath):
    test=os.path.dirname(filepath)      #extract dir only
    if not os.path.exists(test):
        print("Making dir: "+test)
        os.makedirs(test)
#----------------------------------------------------------------
#Regex to detect certain pdf file convention and save vars to global vars
def regex_pdf(path):
    fileRegex=re.compile(r"^(.*?)(([0-9]*)_Rev ([A-Z]{1,2})\.([a-zA-Z]{3,4}))$")
    global filePath,fileName,partNum,partRev,fileExt
    filegroups=fileRegex.search(path)
    filePath=filegroups.group(1)
    fileName=filegroups.group(2)
    partNum=filegroups.group(3)
    partRev=filegroups.group(4)
    fileExt=filegroups.group(5)
    return filegroups
#----------------------------------------------------------------
#create directory structure
def create_pdf_dir():
    global movePath
    subfolder1=partNum[:-len(partNum)+3]+"_"
    subfolder2=partNum[:-2]+"_"
    subfolder3=partNum
    movePath=os.path.join(outputDir,subfolder1,subfolder2,subfolder3,fileName)
    create_path(movePath)    
#----------------------------------------------------------------
def dec_Rev(rev):
    rev_list=["NC"]+list(string.ascii_uppercase)
    decRev=rev_list.index(rev)-1
    if decRev>=0:                     
        return rev_list[decRev]                    
#----------------------------------------------------------------
#creates obs folder and moves prev rev to obs folder
def move_obs(new_path):
    newDir=os.path.dirname(new_path)
    obsDir=os.path.join(newDir,"OBS\\")
    create_path(obsDir)
    if dec_Rev(partRev)==None:
        print("initial release, no obsoletion")
        return
    else:
        obsRev=dec_Rev(partRev) 
        obsFile=partNum+"_Rev "+obsRev+'.'+fileExt
        print("Obsoleting: "+obsFile)
        obsPath_old=os.path.join(newDir,obsFile)
        obsPath_new=os.path.join(obsDir,obsFile)
        if os.path.isfile(obsPath_old):
            print(obsPath_old,obsPath_new)
            shutil.move(obsPath_old,obsPath_new)
        else:
            print("obsolete file not found")
#----------------------------------------------------------------     
#Run through 
print("Working on: " + inputDir)
for item in os.listdir(inputDir):
    print('\n'+item)
    inputPath=os.path.join(inputDir,item)
    inputFile=item
    try:
        regex_pdf(inputPath)
        create_pdf_dir()
        move_obs(movePath)
    except AttributeError:
        print("Incorrect filename: " + inputFile)
        continue
    print("Moving: " + inputPath+" to " +movePath)
    shutil.move(inputPath,movePath)
#------------------------