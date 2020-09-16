#!/usr/bin/python
#
# This script requires suds that provides SOAP bindings for python.
#
# Download suds from https://fedorahosted.org/suds/
#
# unpack it and then run:
# python setup.py install
#
# This may require you to install setuptools (an .exe from python.org)

import sys
sys.path.append('../lib-py')
from os import path

import suds
from suds.client import Client
from suds.wsse import *

from optparse import OptionParser
import cgi

import logging
logging.basicConfig()

import time
import datetime
import csv

from collections import namedtuple

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------------------------------------------------
# Base class for all the web service clients
class WebServiceClient:
    def __init__(self, webservice_type, host, port, user, password):
        url = 'http://' + host + ':' + port

        if webservice_type == 'configuration':
            self.wsdlFile = url+'/ws/v9/configurationservice?wsdl'
        elif webservice_type == 'defect':
            self.wsdlFile = url+'/ws/v9/defectservice?wsdl'

        self.client = Client(self.wsdlFile, timeout=3600)
        self.security = Security()
        self.token = UsernameToken(user, password)
        self.security.tokens.append(self.token)
        self.client.set_options(wsse=self.security)

        if webservice_type != 'configuration':
            self.pageSpecDO = self.client.factory.create('pageSpecDataObj')
            self.pageSpecDO.pageSize = 2500
            self.pageSpecDO.sortAscending = False
            self.pageSpecDO.startIndex = 0

        def getwsdl(self):
            print(self.client)

# -----------------------------------------------------------------------------
# Class that implements webservices methods for Defects
class ConfigurationServiceClient(WebServiceClient):
    def __init__(self, host, port, user, password):
        WebServiceClient.__init__(self, 'configuration', host, port, user, password)

    # --------------------------------------
    def get_SnapshotsForStream(self, streamname):
        streamIdDO = self.client.factory.create('streamIdDataObj')
        snapshotFilterSpecDO = self.client.factory.create('snapshotFilterSpecDataObj')
        streamIdDO.name = streamname

        SnapshotIDs = self.client.service.getSnapshotsForStream(streamIdDO,snapshotFilterSpecDO)

        return SnapshotIDs

# -----------------------------------------------------------------------------
# Class that implements webservices methods for Defects
class DefectServiceClient(WebServiceClient):
    def __init__(self, host, port, user, password):
        WebServiceClient.__init__(self, 'defect', host, port, user, password)

    # --------------------------------------
    def get_MergedDefectsForStreams(self, streamname):
        streamIdDO = self.client.factory.create('streamIdDataObj')
        streamIdDO.name = streamname

        mergedDefectFilterSpecDO = self.client.factory.create('mergedDefectFilterSpecDataObj')
        snapshotScopeSpecDO = self.client.factory.create('snapshotScopeSpecDataObj')

        pageSpecDO = self.client.factory.create('pageSpecDataObj')
        pageSpecDO.pageSize = 1000
        pageSpecDO.startIndex = 0
        mergedDefects = []

        while True:
            print "getMergedDefectsForStreams startIndex : " + str(pageSpecDO.startIndex) + "  (pageSize:" + str(pageSpecDO.pageSize) +")"
            ret = self.client.service.getMergedDefectsForStreams(streamIdDO, mergedDefectFilterSpecDO, pageSpecDO, snapshotScopeSpecDO )
            if ret.totalNumberOfRecords == 0: break
            pageSpecDO.startIndex = pageSpecDO.startIndex + pageSpecDO.pageSize
            for md in ret.mergedDefects: mergedDefects.append(md)
            if ret.totalNumberOfRecords <= pageSpecDO.startIndex: break

        return mergedDefects

    # --------------------------------------
    def get_defectHistory(self, cid, streamname):

        mergedDefectIdDO = self.client.factory.create('mergedDefectIdDataObj')
        mergedDefectIdDO.cid = long(cid)

        streamDefectFilterSpecDO = self.client.factory.create('streamDefectFilterSpecDataObj')
        streamIdDO = self.client.factory.create('streamIdDataObj')
        streamIdDO.name = streamname
        streamDefectFilterSpecDO.streamIdList = streamIdDO
        streamDefectFilterSpecDO.includeDefectInstances = False
        streamDefectFilterSpecDO.includeHistory = True

        StreamDefects = self.client.service.getStreamDefects(mergedDefectIdDO, streamDefectFilterSpecDO)

        # set init value
        LastValues = namedtuple('TriageData', 'status classification action severity owner extref comment dateCreated')
        retVal = LastValues("","","","","","","","",)
        tLastUpdate        = datetime.datetime.strptime("2000-01-01 00:00:00.000000", '%Y-%m-%d %H:%M:%S.%f')

        for sd in StreamDefects:
            if hasattr( sd, "history" ) :
                for history in sd.history :
                    if hasattr( history, "defectStateAttributeValues" ) :
                        status         = ""
                        classification = "Unclassified"
                        severity       = "Unspecified"
                        action         = "Undecided"
                        owner          = ""
                        extref         = ""
                        comment        = ""

                        # get defectStateAttributeValue
                        for defectStateAttributeValue  in history.defectStateAttributeValues:
                            name  = defectStateAttributeValue.attributeDefinitionId.name
                            value = defectStateAttributeValue.attributeValueId.name
                            if  value is None : value = ""
                            if   name == "DefectStatus"  : status   = str(value)
                            elif name == "Classification": classification = str(value)
                            elif name == "Severity"      : severity = str(value)
                            elif name == "Action"        : action   = str(value)
                            elif name == "Owner"         : owner    = str(value)
                            elif name == "Ext. Reference": 
                                try: extref = str(value)
                                except UnicodeEncodeError: comment = "UnicodeEncodeError:"
                                except: comment = "Unexpected error: "
                            elif name == "Legacy"        : legacy   = str(value)
                            elif name == "Comment"       : 
                                try:
                                    comment = str(value)
                                    comment = comment.replace('\r\n',' ')
                                    comment = comment.replace('\r',' ')
                                    comment = comment.replace('\n',' ')
                                except UnicodeEncodeError: comment = "UnicodeEncodeError:"
                                except: comment = "Unexpected error: "

                    # If the triage information is updated manually
                    if( classification != "Unclassified" or severity != "Unspecified" or action != "Undecided" or comment != "" ): 
                        tstr = str(history.dateCreated)
                        if ( tstr != "0001-01-01 00:00:00" ):
                            # add microseconds  ex) 2014-02-26 16:37:40 -> 2014-02-26 16:37:40.000000
                            if ( len(tstr) == 19 ):
                                tstr = tstr + ".000000"
                            tdateCreated = datetime.datetime.strptime( tstr, '%Y-%m-%d %H:%M:%S.%f')
                            if ( tdateCreated > tLastUpdate ) : 
                                tLastUpdate = tdateCreated
                                retVal = LastValues(status,classification,action,severity,owner,extref,comment,str(tdateCreated))

                                #print "-------------------------------------------"
                                #print "[debug] tdateCreated > tLastUpdate"
                                #print "[debug] tLastUpdate  :" + str(tLastUpdate)
                                #print "[debug] tdateCreated :" + str(tdateCreated)
                                #print "[debug] Classification  : " + classification
                                #print "[debug] Severity        : " + severity
                                #print "[debug] Action          : " + action
                                #print "[debug] owner           : " + owner
                                #print "[debug] extref          : " + extref
                                #print "[debug] Comment         : " + comment

        return retVal

    # --------------------------------------
    def export_to_file(self, streamname, suffix):

        # Get all defect in stream
        print "Get all defect in stream"
        mergedDefects = defectServiceClient.get_MergedDefectsForStreams(streamname)

        if len(mergedDefects) == 0:
            print "no defect in " + streamname
            return ""
        print "found " + str(len(mergedDefects)) + " defects in " + streamname

        # Sort by CID
        mergedDefects.sort(cmp=lambda x, y: cmp(x.cid, y.cid))

        # output dir
        path = "./csv/"
        if os.path.exists(path) != True : os.makedirs(path)

        # Create CSV file
        # datetime for output csv file name
        if suffix == 'date' :
            d = datetime.datetime.today()
            filename = path + streamname + d.strftime("_Defects_%Y-%m-%d") + ".csv"
        else:
            filename = path + streamname + suffix + ".csv"

        if os.path.isfile(filename) == True: 
            print "[SKIP] output file: " + filename + " is already exsist!."
            return ""
            
        print "output file: " + filename
        writecsv = csv.writer(file(filename, 'w'), lineterminator="\n")
        writecsv.writerow(["cid", "mergeKey", "checkerName", "Classification","Owner", "Severity", "Action", "Ext. Reference", "Comment","dateCreated"])
        # for Progress
        count = 0
        skip = 0

        for md in mergedDefects:
            #print 
            #print "[debug] CID:" + str(md.cid) + ", mergeKey:" + md.mergeKey

            # get latest triage data
            ret = defectServiceClient.get_defectHistory(md.cid, options.stream)

            if ret.classification == "" : 
                #print "[debug] !! No Triage data !!"
                #if ( skip % 10 == 0 ) : print "writerow skip count :" + str(skip)
                if ( skip % 10 == 0 ) : 
                    print '\b.',
                    sys.stdout.flush()
                skip += 1
                continue

            #print "[debug] ==========================================="
            #print "[debug] LastUpdate     : " + ret.dateCreated
            #print "[debug] status         : " + ret.status
            #print "[debug] classification : " + ret.classification
            #print "[debug] severity       : " + ret.severity
            #print "[debug] action         : " + ret.action
            #print "[debug] owner          : " + ret.owner
            #print "[debug] extref         : " + ret.extref
            #print "[debug] comment        : " + ret.comment
            #print "[debug] ==========================================="

            # add microseconds  ex) 2014-02-26 16:37:40 -> 2014-02-26 16:37:40.000000
            dateCreated = ret.dateCreated
            if ( len(dateCreated) == 19 ):
                dateCreated = dateCreated + ".000000"

            # Write to csvfile
            writecsv.writerow([str(md.cid), md.mergeKey, md.checkerName, ret.classification, ret.owner, ret.severity, ret.action, ret.extref, ret.comment, dateCreated])
            count += 1

            #if ( count % 10 == 0 ) : print "writerow count :" + str(count)
            prog = "[%s]" % ("=" * (count/10) + ">")
            if ( count % 10 == 0 ) : 
                print '\b.',
                sys.stdout.flush()

        print ' Done!'

        return filename

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    myusage = "%prog [--host <hostname>] [--port <port>] [--user <user>] [--password <password>] [--stream <stream name>] [--csv <csvfile>] [-v]"
    parser = OptionParser(usage=myusage)

    parser.add_option("--host",     dest="host",     default='localhost',  help="host of CIM, default:localhost");
    parser.add_option("--port",     dest="port",     default='8080',       help="port of CIM, default: 8080");
    parser.add_option("--user",     dest="user",     default='admin',      help="CIM user, default:admin");
    parser.add_option("--password", dest="password", default='coverity',   help="CIM password, default:coverity");
    parser.add_option("--stream",   dest="stream",                         help="Required. Name of the stream");
    parser.add_option("--mode",     dest="mode",     default='stream',     help="(Option) stream or list, default:stream");
    parser.add_option("--csv",      dest="csv",                            help="Required for mode=list");
    parser.add_option("--suffix",   dest="suffix",   default='date',       help="(Option) suffix for output file name");

    (options, args) = parser.parse_args()
    if (not options.host or
        not options.port or
        not options.user or
        not options.password ):
        parser.print_help()
        sys.exit(-1)

    defectServiceClient = DefectServiceClient(options.host, options.port, options.user, options.password)
    configServiceClient = ConfigurationServiceClient(options.host, options.port, options.user, options.password)

    if options.mode == "stream" :
        if (not options.stream):
            parser.print_help()
            sys.exit(-1)

        defectServiceClient.export_to_file(options.stream, options.suffix)

    else:
        if (not options.csv):
            parser.print_help()
            sys.exit(-1)
 
        try:
            csvfile = open(options.csv, "rb")
        except:
            print "Failed to open ", options.csv
            sys.exit(1);

        # Output file name
        d = datetime.datetime.today()
        filename = path.splitext(__file__)[0] + d.strftime("_outputfiles_%Y-%m-%d") + ".csv"
        f = open(filename, 'w')

        # 0:ProjectName, 1:description, 2:StreamName, 3:language, 4:TriageStore, 5:latestSnapshot.id, 6:dateCreated
        reader  = csv.reader(csvfile)
        rownum = 0

        for row in reader:
            rownum += 1
            if row[0][0:1] == "#":
                print "[SKIP] Line:" + str(rownum) + " " + row[0]
            else:
                outputfile = defectServiceClient.export_to_file(row[2],options.suffix)
                print "[DEBUG]" + str(outputfile)
                if len(outputfile) != 0 : f.write( row[2] + "," + outputfile + "\n" )
            
        f.close()

#-----
