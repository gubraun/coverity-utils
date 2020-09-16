#!/usr/bin/python
'''
usage: getLastTriagedSinceCutoff.py [-h] [-s SERVER] [-p PORT] [-u USER]
                                    [-c PASSWORD] [-n PROJECTNAME]
                                    [-d LASTTRIAGED]

getMergedDefects for all streams in a projects which were triaged more
recently than the lasttriaged date

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        server (default: localhost)
  -p PORT, --port PORT  port (default: 8080)
  -u USER, --user USER  user (default: admin)
  -c PASSWORD, --password PASSWORD
                        password (default: coverity)
  -n PROJECTNAME, --projectname PROJECTNAME
                        projectname (default: "*", meaning all)
  -d LASTTRIAGED, --lasttriaged LASTTRIAGED
                        last triaged after (default:"2016-10-10T01:01:01")

'''
# This script requires suds that provides SOAP bindings for python.
# Download suds from https://fedorahosted.org/suds/
#   unpack it and then run:
#     python setup.py install
#
#   or unpack the 'suds' folder and place it in the same place as this script
from suds.client import Client
from suds.wsse import Security, UsernameToken
#
#For basic logging
import logging
logging.basicConfig()
#Uncomment to debug SOAP XML
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#
import argparse
#import os
import json
# -----------------------------------------------------------------------------
class WebServiceClient:
    def __init__(self, webservice_type, host, port, ssl, username, password):
        url = ''
        if (ssl):
            url = 'https://' + host + ':' + port
        else:
            url = 'http://' + host + ':' + port
        if webservice_type == 'configuration':
            self.wsdlFile = url + '/ws/v9/configurationservice?wsdl'
        elif webservice_type == 'defect':
            self.wsdlFile = url + '/ws/v9/defectservice?wsdl'
        else:
            raise "unknown web service type: " + webservice_type

        self.client = Client(self.wsdlFile)
        self.security = Security()
        self.token = UsernameToken(username, password)
        self.security.tokens.append(self.token)
        self.client.set_options(wsse=self.security)

    def getwsdl(self):
        print(self.client)

# -----------------------------------------------------------------------------
class DefectServiceClient(WebServiceClient):
    def __init__(self, host, port, ssl, username, password):
        WebServiceClient.__init__(self, 'defect', host, port, ssl, username, password)

# -----------------------------------------------------------------------------
class ConfigServiceClient(WebServiceClient):
    def __init__(self, host, port, ssl, username, password):
        WebServiceClient.__init__(self, 'configuration', host, port, ssl, username, password)
    def getProjects(self):
        return self.client.service.getProjects()		

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(description='getMergedDefects for all streams in a projects which were triaged more recently than the lasttriaged date')
    parser.add_argument('-s','--server',  default= 'localhost', help='server (default: localhost)')    
    parser.add_argument('-p','--port',  default= '8080', help='port (default: 8080)')    
    parser.add_argument('-u','--user',  default= 'admin', help='user (default: admin)')    
    parser.add_argument('-c','--password',  default= 'coverity', help='password (default: coverity)')    
    parser.add_argument('-n','--projectname',  default= '*', help='projectname (default: "*", meaning all)')    
    parser.add_argument('-d','--lasttriaged',  default= '2016-10-10T01:01:01', help='last triaged after (default:"2016-10-10T01:01:01")')    
    args = parser.parse_args()
    #
    host = args.server #'localhost'
    port = args.port   #'8080'
    ssl = False
    username = args.user #'admin'
    password = args.password #'coverity'       
    #
    projectpattern=args.projectname
    cutoffdate=args.lasttriaged
    #
    defectServiceClient = DefectServiceClient(host, port, ssl, username, password)
    configServiceClient = ConfigServiceClient(host, port, ssl, username, password)
    print '------------getProjects'
    projectIdDO = configServiceClient.client.factory.create('projectFilterSpecDataObj')
    projectIdDO.namePattern='ACCSHARED'
    projectIdDO.includeStreams=True
    results = configServiceClient.client.service.getProjects(projectIdDO)
    for v in results:
        for s in v.streams:
            print '------------getMergedDefectsForStreams'
            pageSpecDO = defectServiceClient.client.factory.create('pageSpecDataObj')
            pageSpecDO.pageSize=1
            pageSpecDO.startIndex=0
            mergedDefectFilterDO=defectServiceClient.client.factory.create('mergedDefectFilterSpecDataObj')
            mergedDefectFilterDO.lastTriagedStartDate='2010-09-05'
            mergedDefectFilterDO.statusNameList=["New","Triaged","Dismissed"]
            mergedDefects = defectServiceClient.client.service.getMergedDefectsForStreams(s.id, mergedDefectFilterDO, pageSpecDO)
            print mergedDefects.totalNumberOfRecords
            for md in mergedDefects.mergedDefects:
                print md.cid
            for mdid in mergedDefects.mergedDefectIds:
                print mdid.cid,mdid.mergeKey
                print '------------getMergedDefectDetectionHistory'
                defectDetectionHistory = defectServiceClient.client.service.getMergedDefectDetectionHistory(mdid, s.id)
                for mdh in defectDetectionHistory:
                    print mdh.userName, mdh.defectDetection, mdh.detection, mdh.snapshotId, mdh.streams[0].name
                print '------------getMergedDefectHistory'
                defectChanges = defectServiceClient.client.service.getMergedDefectHistory(mdid, s.id)
                for dc in defectChanges:
                    print dc.userModified, dc.dateModified, dc.comments

            
            
            
            
            
    

 