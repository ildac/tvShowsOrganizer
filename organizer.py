#!/usr/bin/python

## This was created by Marco Da Col.
## Project started in 11/2011
## Version 0.2.5
## Last Update 03-11-2012

#-----LIBRARY IMPORT--
import dircache
import re
import os.path
import os
import shutil
import ConfigParser
import time
#from xattr import xattr
from struct import unpack
from struct import pack
#--------------------

#-----EPISODE CLASS----------
class episode:
    def __init__(self, serie, season, episode, file_name):
        self.serie = re.sub('\.', ' ', serie[:-1])     #the last char is a .
        self.season = re.sub('[s,S]', '', season)
        self.episode = re.sub('[e,E]', '', episode)    #actually this isn't used...
        self.file_name = file_name

##Check path is ok, here is where i've to add the check for file
    def okToCopy(self, origin, destination):
        self.destination = destination    #normalize path
        self.origin = origin        #normalize path
        if not os.path.exists(self.destination):    #check if path exist
            try:
                os.makedirs(self.destination)
            except OSError:
                print 'There is an error making the dir'
                return 0
            else:
                if os.path.exists(self.destination):
                    return 1
                else:
                    return 0
        else:
        #here if path exist, i've to check if the file exist too
            if os.path.isfile(self.destination+'/'+self.file_name):
                return 0
            else:
                return 1

##Copy the file
    def doCopy(self, ori_path, dest_path):
        if self.okToCopy(ori_path, dest_path):
            shutil.move(ori_path+self.file_name, dest_path)
           # setColorLabel('yellow', libraryPath+e.getSerie())
        # else:
           # setColorLabel('red', ori_path+'/'+self.file_name)


#-----GETTERS----------
    def getSeason(self):
        return self.season

    def getSerie(self):
        return self.serie

    def getEpisode(self):
        return self.episode

    def getFileName(self):
        return self.file_name

#--------------------

#-----COLOR LABEL FUNCTION----------
def setColorLabel (color, item):
    #used for the coloring settings
    colorNames = { 0: 'none', 1: 'gray', 2 : 'green', 3 : 'purple', 4 : 'blue', 5 : 'yellow', 6 : 'red', 7 : 'orange' }
    colorCodes = { 'none':0, 'gray':1, 'green':2, 'purple':3, 'blue':4, 'yellow':5, 'red':6, 'orange':7 }
    #print item
    #the color that you want for the label
    theColor = color

    flags = ()
    attrs = xattr(item)

    #reader part
    try:
      finder_attrs = attrs[u'com.apple.FinderInfo']
      flags = unpack(32*'B', finder_attrs)
    except KeyError:
      flags = ()

    #this will be the new label color
    newColor = colorCodes[theColor]*2

    #check if there is some attribute, in positive case add the new color Label and codify all flags
    if len(flags) > 0:
        flags = flags[0:9]+(newColor,)+flags[10:]
        finder_attrs = pack(32*'B', flags[0], flags[1], flags[2], flags[3], flags[4], flags[5], flags[6], flags[7], flags[8], flags[9],
    flags[10], flags[11], flags[12], flags[13], flags[14], flags[15], flags[16], flags[17], flags[18], flags[19], flags[20],
    flags[21], flags[22], flags[23], flags[24], flags[25], flags[26], flags[27], flags[28], flags[29], flags[30], flags[31])
    else:
        finder_attrs = pack(32*'B', 0, 0, 0, 0, 0, 0, 0, 0, 0, newColor, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0)

    #register the new attribute
    attrs[u'com.apple.FinderInfo'] = finder_attrs

#-----ESCAPING STRINGS FOR SHELL------------
def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

#-----MAIN-----------
#initialize the configuration option
#config=ConfigParser.ConfigParser()
#config.read("config.cfg")

#downloadPath=config.get('directorySetup', downloadPath, 1)
#libraryPath=config.get('directorySetup', completePath, 1)

#downloadPath='/Users/marco/Documents/Labs/Python/do-it-for-me/testfolder/download/'
#libraryPath='/Users/marco/Documents/Labs/Python/do-it-for-me/testfolder/storage/'

#downloadPath='/Users/marco/Dropbox/torrent/complete/'
#libraryPath='/Volumes/Candy/Telefilm/'

downloadPath='/dac/Downloads/torrents/'
libraryPath='/media/candy/Telefilm/'

#this is an ls on donwload folder
dir = dircache.listdir(downloadPath)

i=0

for file in dir:
    if (file[-4:]=='.avi') or (file[-4:]=='.mp4') or (file[-4]=='.3gp'):
        #TODO Optimizing the REGEX, future optimization
        data = re.match('([A-Z,a-z,\.,201\d{1}]+(?=[s,S][0-9]{2}))([s,S][0-9]{2})([e,E][0-9]{2})', file)
        e = episode(data.group(1), data.group(2), data.group(3), file)
        destination_path = libraryPath + e.getSerie() + '/' + 'Season ' + e.getSeason()

        #sys.stdout.write('test')

        #TODO Implement usefull error handling
        e.doCopy(downloadPath, destination_path)

        ### ---- SolEol is a dead project at this time ----
        #Download Subtitle Using SolEol_Cli
        # commandForSubtitles='/Applications/SolEol/SolEol\ Extras/SolEol_CLI --language="en" --file="' +  destination_path + '/' + e.getFileName() + '" --file="' + destination_path + '" ' + '--user="stardacs" --password="trinity"'
        #print "Finished!"

        ### ---- Subtitles is the new tool: http://subtitlesapp.com/
        #if os.path.isfile(self.destination+'/'+self.file_name):
        #    commandForSubtitles = '/Applications/Subtitles.app/Contents/MacOS/Subtitles ' +  shellquote( destination_path + '/' + e.getFileName() )
        #    os.system(commandForSubtitles)
#--------------------
