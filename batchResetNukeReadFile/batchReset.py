# -*- coding: utf-8 -*-

#######################################################
# # Original Author: Joe Chou
# # Cheer Digiart Inc.
# # version: 1.0.1
# # Batch Replace Nuke Read Node file
#######################################################

import nuke
import glob 
import os 
import re 
import nukescripts

def scanForFiles(_dir):
    files = os.listdir(_dir)
    result={}
    sortedList = []
    validFiles=("tiff","tif","exr","jpg","jpeg","png")
    for file in files:
        try:
            prefix, frame, suffix = file.split('.')
            if suffix in validFiles:
                try:
                    result[prefix][0].append(frame)
                except KeyError:
                    result[prefix] = [[frame],suffix]
        except ValueError:
            #print ''
            print "ignoring file in directory %s" %(file)
    
    for file in result:
        fileName=file
        extention=result[file][1]
        minFrameValue=int(min(result[file][0]))
        maxFrameValue=int(max(result[file][0]))
        framePadSize=len(result[file][0][0])
        padString="%%0%dd" %(framePadSize)
        fileNameString="%s.%s.%s" %(fileName,padString,extention)
        sortedList.append([fileNameString,minFrameValue,maxFrameValue])
        sortedList.sort()
    return sortedList

def batchReset(src,out):
    print src
    errFlg = 0
    nuke.scriptOpen(src)
    for node in nuke.allNodes('Read'):
        if os.path.dirname(node.knob('file').getValue()) != r'S:/LSC/CGI/Asset/lightset/asset_checklight/nukeimages':
            print os.path.dirname(node.knob('file').getValue())           
            filelist = scanForFiles(os.path.dirname(node.knob('file').getValue()))
            print filelist
            node.knob('file').setValue(os.path.dirname(node.knob('file').getValue())+'/'+filelist[0][0])
            node.knob('first').setValue(filelist[0][1])
            node.knob('last').setValue(filelist[0][2])
            node.knob('origfirst').setValue(filelist[0][1])
            node.knob('origlast').setValue(filelist[0][2])
    if not errFlg:
        print 'All selected Read nodes were reset.'
    nuke.scriptSave(out)
    for allnode in nuke.allNodes():
        nuke.delete(allnode)

def batch():
    curdir = sys.argv[1]
    f = open(curdir+'/shot.txt', 'r')
    for shotname in f.readlines():
        shotname = "".join(shotname.split())
        #print shotname
        seq = shotname.split('_')
        verlist = sorted(glob.glob(r'S:/LSC/CGI/SceneFiles/'+seq[0]+'/'+shotname+'/Comp/Nuke/work/'+shotname+'_comp_bty_v*.nk'))
        #verlist = sorted(glob.glob(r'//nas01/pj1/LSC/Temp/jou/comptest/'+shotname+'_comp_bty_v*.nk'))
        lastver = verlist[len(verlist)-1].replace('\\','/')
        if shotname :
            #print lastver
            if os.path.exists(lastver):
                print '!!Ver:'+lastver
                #batchReset(lastver,'//nas01/pj1/LSC/Temp/jou/haha/'+shotname+'_comp.nk')                
                batchReset(lastver,lastver)               
            else:
                break
       
    f.close()

batch()
