#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Description: List User Details
# Usage: list_users.py --host <Coverity Connect host>
# --port <Coverity Connect port> --user <login user>
#           --password <login password>

from __future__ import print_function

import os
import sys
import pdb
from optparse import OptionParser

from suds import WebFault
from suds.client import Client
from suds.wsse import Security
from suds.wsse import UsernameToken


def safeprint(s):
    try:
        print(s, end='')
    except UnicodeEncodeError:
        if sys.version_info >= (3,):
            print(s.encode('utf8').decode(sys.stdout.encoding), end='')
        else:
            print(s.encode('utf8'), end='')


# -----------------------------------------------------------------------------
# Base class for all the web service clients

class WebServiceClient:
    def __init__(self, webservice_type, host, port, user, password):
        url = 'http://' + host + ':' + port

        if webservice_type == 'configuration':
            self.wsdlFile = url + '/ws/v9/configurationservice?wsdl'
        elif webservice_type == 'defect':
            self.wsdlFile = url + '/ws/v9/defectservice?wsdl'

        self.client = Client(self.wsdlFile)
        self.security = Security()
        self.token = UsernameToken(user, password)
        self.security.tokens.append(self.token)
        self.client.set_options(wsse=self.security)

    def getwsdl(self):
        print(self.client)


# -----------------------------------------------------------------------------
# Class that implements webservices methods for Defects

class DefectServiceClient(WebServiceClient):
    def __init__(self, host, port, user, password):
        WebServiceClient.__init__(self, 'defect', host, port, user, password)


# -----------------------------------------------------------------------------
# Class that implements webservices methods for Configuration

class ConfigurationServiceClient(WebServiceClient):
    def __init__(self, host, port, user, password):
        WebServiceClient.__init__(self, 'configuration', host, port, user, password)

    # An initial call to this method wil craete a list of all groups in the server.
    # This list will be later be used to enable/disable a user without harming the group associated with the user

    def get_user_details(self, userName):
        self.userDataDO = self.client.factory.create('userDataObj')
        self.userDataDO.user = self.client.service.getUser(userName)
        return

    def print_users(self, options):
        userFilterSpecDO = self.client.factory.create('userFilterSpecDataObj')

        if options.disabled:
            userFilterSpecDO.disabled = True  # disabled users only
        if options.licensed:
            userFilterSpecDO.disabled = False  # enabled users only

        pageSpecDO = self.client.factory.create('pageSpecDataObj')

        pageSpecDO.pageSize = 1000
        pageSpecDO.sortAscending = "True"
        pageSpecDO.startIndex = 0

        usersDO = self.client.service.getUsers(userFilterSpecDO, pageSpecDO)

        userCount = 0

        if hasattr(usersDO, 'users'):
            for user in usersDO.users:
                if (options.licensed and user.username != "admin" and user.username != "reporter"):
                    print(user.username)
                    userCount += 1
                elif (options.all):
                    print(user.username)
                    userCount += 1

        print("Count: " + str(userCount))


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    myusage = "%prog --host=<CIM host> --port=<CIM port> --user=<login user> --password=<login password> --username=<CIM Username>"

    parser = OptionParser(usage=myusage)

    parser.add_option("--host", dest="host", default='localhost', help="host of CIM, default: localhost")
    parser.add_option("--port", dest="port", default='8080', help="port of CIM, default: 8080")
    parser.add_option("--user", dest="user", default='admin',
                      help="user for authentication on Coverity Connect Server, default: admin")
    parser.add_option("--password", dest="password", default='SIGpass8', help="password")
    parser.add_option("--all", dest="all", action="store_true", help="all users")
    parser.add_option("--licensed", dest="licensed", action="store_true",
                      help="users who are counted against licensed number of users")
#    parser.add_option("--recent", dest="recent", action="store_true",
#                      help="users who have recently logged in (within the last month)")
#    parser.add_option("--stale", dest="stale", action="store_true",
#                      help="users who haven't logged in within the last 6 months")
#    parser.add_option("--absent", dest="absent", action="store_true",
#                      help="users who have never logged in")
    parser.add_option("--disabled", dest="disabled", action="store_true", help="disabled users")

    (options, args) = parser.parse_args()

    # pdb.set_trace()
    try:
        configServiceClient = ConfigurationServiceClient(
            options.host,
            options.port,
            options.user,
            options.password)

        configServiceClient.print_users(options)

    except WebFault as err:
        print()
        sys.stderr.write("suds.WebFault caught: ")
        print(unicode(err))
        print()
        sys.exit(-1)
    except:  # here to hide our Python nature
        print()
        err = sys.exc_info()[1]
        print('Other error: ' + str(err))
        print()
        sys.exit(-1)

    sys.exit(0)
# end of main loop

