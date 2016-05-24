#!/usr/bin/env python

#Use this to get ip of home computer in all cases.
#This is done so that an immutable state is enforced on the 
#global object and it only needs to be changed in code once
def getHomeIP():
    homeIP = '128.205.55.146' #New Computer
    #homeIP = '128.205.55.104' #Old Computer
    #homeIP = '128.205.55.189' #Local
    return homeIP
