#!/usr/bin/python
#
# This script requires suds that provides SOAP bindings for python.
# Download suds from https://fedorahosted.org/suds/
#   unpack it and then run:
#     python setup.py install
#
#   or unpack the 'suds' folder and place it in the same place as this script

import sys
from suds.client import Client
from suds.wsse import Security, UsernameToken
import logging
logging.basicConfig()

# Uncomment to debug SOAP XML
# logging.getLogger('suds.client').setLevel(logging.DEBUG)
# logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#
# getFileContents result requires decompress and decoding
import base64, zlib


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
    #============================================================================
    # Connection details.   
    # To run these examples adjust these connection parameters to match your
    # instance URL and credentials
    #
    #
    host = 'localhost'
    port = '8080'
    ssl = False
    username = 'admin'
    password = 'sigpass'	    
    #============================================================================
    
    defectServiceClient = DefectServiceClient(host, port, ssl, username, password)
    configServiceClient = ConfigServiceClient(host, port, ssl, username, password)

    # Update users: remove visitor role at user level from every user. 
    userIdDO = configServiceClient.client.factory.create('userFilterSpecDataObj')
    userIdDO.namePattern='*'
    pageSpecDO = defectServiceClient.client.factory.create('pageSpecDataObj')
    pageSpecDO.pageSize=100
    pageSpecDO.startIndex=0
    v = configServiceClient.client.service.getUsers(userIdDO, pageSpecDO)

#    print '------------getUsers'
#    print v.totalNumberOfRecords

    # Go over all users and find the ones that have the visitor role assigned as
    # global user role. Put these into list usersToUpdate.
    usersToUpdate = []
    for u in v.users:
#        print u.username
#        print "  roles:"
        if hasattr(u, 'roleAssignments') and u.username != 'admin':
            for ra in u.roleAssignments:
#                print "    roleAssignmentType:  " + ra.roleAssignmentType
#                print "    roleId:              " + ra.roleId.name
#                print "    type:                " + ra.type
                if ra.roleAssignmentType == 'user' and ra.roleId.name == 'visitor' and ra.type == 'global':
#				    print "    username:            " + ra.username
                    usersToUpdate.append(u)
#        else:
#            print u.username + " has no role"

    # Print list of to-be-updated users
    print "[INFO] " + str(len(usersToUpdate)) + " users to be updated:"
    for u in usersToUpdate:
        print "    " + u.username

    # Go over list and remove global user role visitor from users in list
    for u in usersToUpdate:
        # Bail out should admin be in this list
        if u.username == 'admin':
            sys.exit("Fatal internal error, admin should not be in this list")
        # Create user spec that contains updated user information
        print "[INFO] updating '" + u.username + "'"
        us = configServiceClient.client.factory.create('userSpecDataObj')
        # Username attribute required
        us.username = u.username
        # Copy role assignments and remove visitor role
        us.roleAssignments = u.roleAssignments 
        for ra in u.roleAssignments:
            if ra.roleAssignmentType == 'user' and ra.roleId.name == 'visitor' and ra.type == 'global':
                us.roleAssignments.remove(ra)
        # I don't know how to remove the last role 
        # ... if I pass an empty list, the role assignment won't be updated
        if len(us.roleAssignments) == 0:
            print "[INFO]     cannot remove role, needs to be removed manually"
        else:
            print "[INFO]     removing global user role 'visitor'"
            usersToUpdate.remove(u)
        # The actual intrusive API call
        # *** DO NOT UNCOMMENT THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING ***
        configServiceClient.client.service.updateUser(u.username, us)

    # Print list of users that could not be updated				
    print "[INFO] " + str(len(usersToUpdate)) + " users need to be updated manually:"
    for u in usersToUpdate:
        print "    " + u.username

