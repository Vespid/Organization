# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:01:47 2017

@author: Vincent
"""

import os,re,sys,shutil
from mutagen.id3 import ID3
#----------------------------------------------------------------------
#Global Variables
#source_path=sys.argv[1]
#destination=sys.argv[2]
source_path=os.path.join('F:\Music\_Recovered')
destination="F:\\Programming\\Test\\Sorted\\"
failure="F:\\Programming\\Test\\Sorted\\Failure"

def id3_data(path):
    audio = ID3(path)
    artist=audio['TPE1'].text[0]
    song=audio["TIT2"].text[0]
    album=audio["TDRC"].text[0]
    track_num=audio["TRCK"].text[0]
#----------------------------------------------------------------------
def getMutagenTags(path):
    """"""
    audio = ID3(path)
 
    print("Artist: %s" % audio['TPE1'].text[0])
    print("Track: %s" % audio["TIT2"].text[0])
    print("Release Year: %s" % audio["TDRC"].text[0])
    print("Album: %s" % audio["TALB"].text[0])
    print("Track Number: %s" % audio["TRCK"].text[0])
#----------------------------------------------------------------------
def mp3FilePath(path):
    audio=ID3(path)
    track=get_track(path)
#    name=track+" - "+audio["TIT2"].text[0]+get_file_type(path)
    name=track+" - "+audio["TIT2"].text[0]+".mp3"
    album=audio["TALB"].text[0]
    artist=audio['TPE1'].text[0]
    invalidchars=['~','#','%','&','*','{','}','\\',":",'<','>','?','/','+','|','"']
    table=str.maketrans(dict.fromkeys(invalidchars))
    name=name.translate(table)
    album=album.translate(table)
    artist=artist.translate(table)
    final=os.path.join(destination,artist,album,name)
    return(final)
#----------------------------------------------------------------------
def get_track(mp3path):
    audio = ID3(mp3path)
    track_cond=re.compile(r'\d{1,2}')
    track=track_cond.search(audio["TRCK"].text[0])
    return(track.group())
#----------------------------------------------------------------------
def get_file_type(mp3path):
    file_cond=re.compile(r'\.\w{3,4}')
    file=file_cond.search(mp3path)
    return(file.group())
#----------------------------------------------------------------------
def create_dir(path):
    audio=ID3(path)
    album=audio["TALB"].text[0]
    artist=audio['TPE1'].text[0]
    invalidchars=['~','#','%','&','*','{','}','\\',":",'<','>','?','/','+','|','"']
    table=str.maketrans(dict.fromkeys(invalidchars))
    album=album.translate(table)
    artist=artist.translate(table)
    directory=os.path.join(destination,artist,album)
    if not os.path.exists(directory):
        os.makedirs(directory)
#----------------------------------------------------------------------
def fail_cond(x,y):
    failpath=os.path.join(failure,x)
    shutil.move(y,failpath)
#----------------------------------------------------------------------
for folderName, subfolders, filenames in os.walk(source_path):
    #print("The current folder is: " + folderName)
    for filename in filenames:
        filePath=os.path.join(folderName,filename)
        if ".com" in filePath:
            try:
                test=ID3(filePath)
            except:
                fail_cond(filename,filePath)
                continue
            requiredid3=['TPE1',"TIT2","TALB","TRCK"]
            if not set(test.keys()).issuperset(set(requiredid3)):
                fail_cond(filename,filePath)
                continue
            newfile=mp3FilePath(filePath)
            create_dir(filePath)
            print(filename)
            shutil.move(filePath,newfile)
        else:
#            fail_cond(filename,filePath)
            continue
#    print(' ')
