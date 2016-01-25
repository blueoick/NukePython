# -*- coding: utf-8 -*-

#######################################################
# # Original Author: Joe Chou
# # Cheer Digiart Inc.
# # version: 1.0.4
#######################################################

import nuke
import os
import glob 
import re 
import nukescripts

#log = None

def outputmov(src,out):
    #global log
    try:
        
        readNode = nuke.createNode('Read')
        writeNode = nuke.createNode('Write')
        readNode.knob('file').setValue(src)
        filePath = nukescripts.replaceHashes(readNode.knob('file').getValue()).replace('%d', '%01d')
        padRe = re.compile('%0(\d+)d')
        padMatch = padRe.search(filePath)
        padSize = int(padMatch.group(1)) 
   
        if padMatch:
            frameList = sorted(glob.iglob(padRe.sub('[0-9]' * padSize, filePath)))
            if frameList:
                missing = 0
                firstVal = os.path.splitext(frameList[0])[0][-padSize:] 
                lastVal = os.path.splitext(frameList[-1])[0][-padSize:] 
                readNode.knob('first').setValue(int(firstVal))
                readNode.knob('last').setValue(int(lastVal))
                readNode.knob('origfirst').setValue(int(firstVal))
                readNode.knob('origlast').setValue(int(lastVal))
            else:
                missing = 1
                errFlg = 1
    
        readNode.knob('colorspace').setValue("rec709")
        #readNode.knob("reload").execute()
        writeNode.knob('file_type').setValue("mov")
        writeNode.knob('file').setValue(out)
        writeNode.knob('colorspace').setValue("rec709")
        writeNode.knob('meta_codec').setValue("png")
        writeNode.knob('mov64_fps').setValue(25)
        nuke.execute('Write1', int(firstVal),int(lastVal))
        nuke.delete(writeNode)
        nuke.delete(readNode)
    except:
        print 'Error'
        nuke.delete(writeNode)
        nuke.delete(readNode)
        

    
def batch():
    #global log
    curdir = sys.argv[1]
    f = open(curdir+'/shot.txt', 'r')
    #log = open(curdir+'/log.txt','w+')
    for shotname in f.readlines():
        try:
            shotname = "".join(shotname.split())
            seq = shotname.split('_')
            print shotname
            verlist = sorted(glob.glob(r'//nas01/pj1/LSC/CGI/SceneFiles/'+seq[0]+'/'+shotname+'/Render/'+shotname+'/v*'))
            lastver = verlist[len(verlist)-1].replace('\\','/')
            if shotname :
                #print lastver
                if os.path.exists(lastver):
                    outputmov(lastver+'/'+shotname+'.####.png',r'S:/LSC/CGI/SceneFiles/'+seq[0]+'/all_mov/'+shotname+'.mov')
                    #print shotname        
                else:
                    break
        except:
            print 'Error:'+shotname
       
    f.close()
if __name__ == '__main__':
    
    batch()
