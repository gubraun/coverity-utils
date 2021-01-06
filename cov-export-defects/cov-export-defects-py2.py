#!/usr/bin/env python

# This script requires zeep that provides SOAP bindings for python.
#   pip install suds

from suds.client import Client
from suds.wsse import Security
from suds.wsse import UsernameToken

import logging
import sys
import datetime
import argparse
import getpass


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

        #self.client = Client(self.wsdlFile,
        #                     wsse=UsernameToken(username, password))
        self.client = Client(self.wsdlFile)
        self.security = Security()
        self.token = UsernameToken(username, password)
        self.security.tokens.append(self.token)
        self.client.set_options(wsse=self.security)
        
    def getwsdl(self):
        print(self.client)

class DefectServiceClient(WebServiceClient):
    def __init__(self, host, port, ssl, username, password):
        WebServiceClient.__init__(self, 'defect', host, port, ssl, username, password)

class ConfigServiceClient(WebServiceClient):
    def __init__(self, host, port, ssl, username, password):
        WebServiceClient.__init__(self, 'configuration', host, port, ssl, username, password)
    def getProjects(self):
        return self.client.service.getProjects()		


# Helper functions to get defect attributes

def print_defect_attribute_types(defect):
    defect_attributes = defect.defectStateAttributeValues
    for attribute in defect_attributes:
        print(attribute.attributeDefinitionId.name)

def get_defect_attribute(defect, attribute_name):
    defect_attributes = defect.defectStateAttributeValues
    for attribute in defect_attributes:
        if attribute.attributeDefinitionId.name == attribute_name:
            return attribute.attributeValueId.name
    # attribute not found
    return None

def get_defect_cid(defect):
    return str(defect.cid)

def get_defect_type(defect):
    return defect.displayType

def get_defect_impact(defect):
    return defect.displayImpact

def get_defect_status(defect):
    return get_defect_attribute(defect, "DefectStatus")

def get_defect_firstdetected(defect):
    return defect.firstDetected.strftime("%x")

def get_defect_owner(defect):
    return get_defect_attribute(defect, "Owner")

def get_defect_classification(defect):
    return get_defect_attribute(defect, "Classification")

def get_defect_severity(defect):
    return get_defect_attribute(defect, "Severity")

def get_defect_action(defect):
    return get_defect_attribute(defect, "Action")

def get_defect_component(defect):
    return defect.componentName

def get_defect_category(defect):
    return defect.displayCategory

def get_defect_file(defect):
    return defect.filePathname

def get_defect_function(defect):
    try:
        if not defect.functionDisplayName:
            return ""
        else:
            #return defect.functionDisplayName
            return defect.functionName
    except AttributeError:
        return ""

def get_defect_count(defect):
    return str(defect.occurrenceCount)

def get_defect_issuekind(defect):
    return defect.displayIssueKind


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="hostname of Coverity Connect server")
    parser.add_argument("--port", help="port of Coverity Connect server")
    parser.add_argument("--ssl", help="connect via HTTPS", action="store_true", default=0)
    parser.add_argument("--user", help="username for authentication")
    parser.add_argument("--password", help="password for authentication")
    parser.add_argument("--stream", help="stream name")
    parser.add_argument("--snapshot", help="optional snapshot id (default: last snapshot in stream)", type=int)
    parser.add_argument("--output-file", help="output file name for CSV output")
    parser.add_argument("--separator", help="separator for CSV", default=",")

    args = parser.parse_args()

    if args.stream == None:
        sys.stderr.write("[Error] This command requires a --stream option.\n")
        exit(1)

    if args.host == None:
        sys.stderr.write("[Error] Cannot connect to a server because --host is missing.\n")
        exit(1)
    else:
       cov_host = args.host

    if args.port == None:
        if args.ssl:
            cov_port = "8443"
        else:
            cov_port = "8080"
    else:
        cov_port = args.port

    if args.user == None:
        cov_user = getpass.getuser()
    else:
        cov_user = args.user

    if args.password == None:
        print("Enter the password for user " + cov_user + " on " + cov_host + ":" + cov_port + ".")
        cov_password = getpass.getpass("Password:")
    else:
        cov_password = args.password

    # Open connection to SOAP defect and configuration service
    defectServiceClient = DefectServiceClient(cov_host, cov_port, args.ssl, cov_user, cov_password)
    configServiceClient = ConfigServiceClient(cov_host, cov_port, args.ssl, cov_user, cov_password)

    stream_id = defectServiceClient.client.factory.create("streamIdDataObj")
    stream_id.name = args.stream

    # Check if stream passed as arg exists
    streams = configServiceClient.client.service.getStreams()
    stream_found = False
    for stream in streams:
        if stream.id.name == stream_id.name:
            stream_found = True
            break
    if not stream_found:
       sys.stderr.write("[Error] no such stream: " + stream_id.name + "\n")
       exit(1)
        
    
    # Get all defects from stream

    page_config = defectServiceClient.client.factory.create('pageSpecDataObj')
    page_config.pageSize = 1000
    page_config.startIndex = 0
    page_config.sortAscending = True

    snapshot_filt = defectServiceClient.client.factory.create("snapshotScopeSpecDataObj")
    snapshot_filt.showSelector = "last()"

    # If snapshot has been specified as arg, check if it exists
    if args.snapshot == None:
        print("No snapshot specified, using most recent one.")
    else:
        # Enumerate snapshots in specified stream
        snapshots = configServiceClient.client.factory.create("snapshotIdDataObj")
        snapshots = configServiceClient.client.service.getSnapshotsForStream(stream_id)
        snapshot_found = False
        for snapshot in snapshots:
            if snapshot.id == args.snapshot:
                snapshot_found = True
                break
        if snapshot_found:
            snapshot_filt.showSelector = args.snapshot
            print("Snapshot specified, will use " + str(args.snapshot))
        else:
           sys.stderr.write("[Error] stream " + stream_id.name + " doesn't have snapshot with id " + str(args.snapshot) + "\n")
           exit(1)

    defect_page = defectServiceClient.client.service.getMergedDefectsForStreams(stream_id, None, page_config, snapshot_filt)
    remaining_defects = defect_page.totalNumberOfRecords # all defects of all pages

    print("Found " + str(remaining_defects) + " defects to be written to report.")

    # Check and open output file late so we don't overwrite in case of other errors 
    if args.output_file == None:
        output_file = sys.stdout
    else:
        output_file = open(args.output_file, "w")

    fields = [
        "CID",
        "Type",
        "Impact",
        "Status",
        "First Detected",
        "Owner",
        "Classification",
        "Severity",
        "Action",
        "Component",
        "Category",
        "File",
        "Function",
        "Count",
        "Issue Kind"
        ]

    #print("CID,Type,Impact,Status,First Detected,Owner,Classification,Severity,Action,Component,Category,File,Function,Count,Issue Kind", file=output_file)
    output_file.write(args.separator.join(fields) + "\n")
 
    while remaining_defects > 0:
        defects_last_page = 0
        for defect in defect_page.mergedDefects:
            output_file.write(
                get_defect_cid(defect) + args.separator +
                "\"" + get_defect_type(defect) + "\"" + args.separator +
                get_defect_impact(defect) + args.separator +
                get_defect_status(defect) + args.separator +
                get_defect_firstdetected(defect) + args.separator +
                get_defect_owner(defect) + args.separator +
                get_defect_classification(defect) + args.separator +
                get_defect_severity(defect) + args.separator +
                get_defect_action(defect) + args.separator +
                get_defect_component(defect) + args.separator +
                get_defect_category(defect) + args.separator +
                get_defect_file(defect) + args.separator +
                "\"" + get_defect_function(defect) + "\"" + args.separator +
                get_defect_count(defect) + args.separator +
                get_defect_issuekind(defect) + "\n"
            )
            defects_last_page += 1
        # done with one page
        page_config.startIndex += defects_last_page
        remaining_defects -= defects_last_page
        defect_page = defectServiceClient.client.service.getMergedDefectsForStreams(stream_id, None, page_config, snapshot_filt)

    if not args.output_file == None:
        print("Wrote CSV output to file: " + args.output_file)
        output_file.close()

