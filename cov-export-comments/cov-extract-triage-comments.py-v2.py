#!/usr/bin/python
# -*- coding: utf-8 -*-
# Desc:     Script to find qualifying defects in Coverity
# Author:   Designed and coded by Ian Ashworth
# Date:     August 2016
# Version:  1.0.6

# General
import argparse
import ConfigParser
import re
import datetime
import string
import os
import csv

# For Coverity - SOAP
from suds.client import *
from suds.wsse import *

# For Jira - REST
import urllib2
import base64
import json
import requests



# -- Default values -- and global settings

# -- Coverity -- system defaults, override with config or command line arg
defCoverityTransport = "http"
defCoverityHostname = "localhost"
defCoverityPort = "8080"

# account for accessing Web Service
defCoverityUsername = "reporter"
defCoverityPassword = "coverity"            #@TODO -change?
# could also record this as an env var
#defCoverityPassword = "${COVERITY_PASSWORD}"

# Coverity built in Impact statuses
covImpactsList = {'High', 'Medium', 'Low'}

covKindsList = {'QUALITY', 'SECURITY', 'TEST'}

# Coverity built in Classifications
covClassificationsList = {'Unclassified', 'Pending', 'False Positive', 'Intentional', 'Bug', 'Untested', 'No Test Needed'}

# Coverity built in Actions
covActionsList = {'Undecided', 'Fix Required', 'Fix Submitted', 'Modeling Required', 'Ignore', 'On hold', 'For Interest Only'}

# map Kind to a readable label
covIssueKindLabel = {'QUALITY': 'Quality', 'SECURITY': 'Security', 'Various': 'Quality/Security', 'TEST' : 'Testing'}


# Coverity Web Services version
wsVersion = 'v9'

# names of Coverity Triage/Attribute fields
nameOfExtReferenceAttribute = "Ext. Reference"
nameOfDefectStatusAttribute = "DefectStatus"
nameOfClassificationAttribute = "Classification"
nameOfActionAttribute = "Action"
nameOfCommentAttribute = "Comment"



# -- general --

# counters
cntResults = 0
cntValidResults = 0
cntDefects = 0
cntErrors = 0
cntWarnings = 0
cntWorkDone = 0

# assume success - manipulate with --exitcode 
exitCode = 0

hLog = None
hOutput = None

# derive a default config filename from the script name
scriptName = os.path.basename(__file__)
defConfigPath = os.path.dirname(os.path.realpath(__file__))

# split into filename and path to this file
defConfigFilename = os.path.splitext(scriptName)[0]+'.config'
# fully qualified with path
defConfigFile = os.path.join(defConfigPath, defConfigFilename)

# default log file
defLogFilename = os.path.splitext(scriptName)[0]+'.log'
# fully qualified with path
defLogFile = os.path.join(defConfigPath, defLogFilename)


def enum(**enums):
    return type('Enum', (), enums)

exitCodes = enum(INTERNAL_ERROR=-11, PROC_ERROR=-5, JIRA_COMMS_ERROR=-4, COV_COMMS_ERROR=-3, INVALID_ARG=-2, MISSING_ARG=-1, SUCCESS_NO_RESULTS=0, SUCCESS_RESULTS=1)

dataType = enum(STRING=1, INTEGER=2)
dataTypeLabel = ["string", "integer"]

dataScopeType = enum(ALL2=-1, ALL=0, NEWLY_DETECTED=1, NEWLY_ELIMINATED=2, NEWLY_DISMISSED=3, COMMON=4)
dataScopeTypeLabel = ["All2", "All", "Newly detected (discovered)", "Newly eliminated (fixed)", "Newly dismissed", "Common"]
dataScopeTypeCaveat = ["", "", "", "", "(needs further filtering)", ""]

# usually with -1, 0, +1 (adj by 1)
positionLabel = ["last", "all", "first"]

# modes can be tested for absolute or bit values in combination
# e.g.  NORMAL operation but IGNORE_SNAPSHOT_COUNTS = 0x01 + 0x10 = 0x11 = 17
modeTypes = enum(NORMAL=0x1, FORCE_JIRA_TICKET=0x2, CLEAR_COV_EXT_REF=0x4, BUILD_JAUTH=0x8,
                 IGNORE_SNAPSHOT_COUNT=0x10, SUMMARISE=0x20, SUPPRESS_COV_UPDATE=0x40, DUMP=0x80)


# --- helper functions ---
def RepMsg(msgtype="" , msg="", repExitCode=0, useExitCode=0):
    repMsg = ""
    if msgtype:
        repMsg += msgtype + ": "
    repMsg += msg
    if useExitCode:
        repMsg += ' <' + str(repExitCode) + '>'
    # if a log file defined, send it here, otherwise to stdout
    if hLog:
        hLog.write(repMsg + '\n')
    elif not hasattr(options, 'silent') or options.silent != 1:
        # if not suppressing screen output
        print repMsg
    if useExitCode:
        exit(repExitCode)

def RepError(msg, repExitCode=0, useExitCode=1):
    global cntErrors
    cntErrors += 1
    RepMsg("ERROR(" + str(cntErrors) + ")", msg, repExitCode, useExitCode)

def RepWarning(msg, repExitCode=0, useExitCode=0):
    global cntWarnings
    cntWarnings += 1
    RepMsg("WARNING(" + str(cntWarnings) + ")", msg, repExitCode, useExitCode)

def RepNote(msg, repExitCode=0, useExitCode=0):
    RepMsg("Note", msg, repExitCode, useExitCode)

def RepTx(msg):
    # Only Log transmissions
    if hLog:
        RepMsg("TX", msg)

def Pad(seq, num):
    pad = ''
    while num:
        num -= 1
        pad += seq
    return pad

def RepDebug(level, msg):
    if hasattr(options, 'debug') and level <= options.debug:
        indent = Pad('---',level)
        RepMsg("dbg{" + str(level) + "}" + indent, msg)
        return True
    return False


# progress bar
barBackground = "----+----+----+----+----+----+----+----+----+----+"
barForeground1 = barBackground.replace('-', ':')
barForeground = barForeground1.replace('+', '|')

# show screen progress
def ShowProgressBar(title, at, total):
    if not hLog:
        perc = at * 100 / total
        maxBarLength = len(barBackground)

        cntDone  = perc * maxBarLength / 100
        # if debug - line feeds are likely to affect output of a bar
        if bool(options.debug):
            # simplify it
            print "%s %3d%% (%d/%d)" % (title, perc, at, total)
        else:
            progressBar = barForeground[:cntDone] + barBackground[cntDone:]
#            if at == 0:
#                print("%s  %s" % (Pad(" ", len(title)), barBackground))
#                sys.stdout.write("\r%s [%s] %3d%% (%d/%d)   " % (title, progressBar, perc, at, total))
            sys.stdout.write("\r%s [%s] %3d%% (rem=%d)   " % (title, progressBar, perc, total-at))
            sys.stdout.flush()
            if at == total:
                print " - Done!"

# parse a term assuming [ [part1],[part2] ]
def parseTwoPartTerm(term, delim=','):
    valid = False
    part1 = ""
    part2 = ""
    if term.find(delim) != -1:
        valid = True
        field1 = term.split(delim, 1)[0]
        if bool(field1):
            part1 = field1
        field2 = term.rsplit(delim, 1)[-1]
        if bool(field2):
            part2 = field2
    return valid,part1,part2


# compare strings for equivalence - some leniency allowed such as spaces and casing
def CompareStrings(inpstr, pat):
    if re.match(pat, inpstr, flags=re.IGNORECASE):
        return True
    # ignore embedded spaces and some odd punctuation characters ("todo" = "To-Do")
    inpstr2 = re.sub(r'[.:\-_ ]', '', inpstr)
    pat2 = re.sub(r'[:\-_ ]', '', pat)  # don't remove dot (part of regex?)
    if re.match(pat2, inpstr2, flags=re.IGNORECASE):
        return True
    return False

def StringsMatch(strValue, patValue):
    RepDebug(6, '? match [%s] ~ <%s>' % (strValue, patValue))
    match = CompareStrings(strValue, patValue)
    if match:
        RepDebug(6, 'yes!')
    return match

def AdjustKey(myDict, myKey, incValue):
    if incValue:
        # if no key to work with - assume 'none' or equiv
        if myKey is None or len(myKey.strip()) == 0:
            myKey = 'n/a'
        try:
            if myDict[myKey]:
                # get the current count
                currValue = myDict[myKey]
                myDict[myKey] = (currValue + incValue)
        except:
            # key wasn't present, create it now
            myDict[myKey] = incValue
        return myDict[myKey]
    return 0

def IncrementCounterForKey(myDict, myKey, myIncValue=1):
    # maintain a total count for this dictionary?
#    AdjustKey(myDict, 'Total', myIncValue)
    return AdjustKey(myDict, myKey, myIncValue)


def DumpKeys(title, myDict):
    RepMsg("", "\n%s:" % title)
    if len(myDict) > 0:
        for i in sorted(myDict):
            RepMsg("", "  %s = %d" % (i, myDict[i]))
    else:
        RepMsg("", "  none")

def InterpretNumeric(phrase, silent=0):
    try:
        return True,eval(str(phrase))
    except:
        if not silent:
            RepWarning('Invalid numeric term [%s] - treating as if ZERO' % phrase)
        return False,0

def ExpandAnyEnvVars(value):
    try:
        value = string.Template(value).substitute(os.environ)
        RepDebug(4, '  which expands into [%s]' % (value))
    except:
        e = sys.exc_info()[0]
        RepDebug(4, "Unable to expand [%s]\nException %s" % (value, e))
    return value



    # if an embedded $ environment variable (system default)
opts = enum(EXPAND_ENVVARS=0x1,
            REMOVE_QUOTES=0x2,
            NONE_IS_NONE=0x4,
            ALL=0xFF)

# interpret the value of a supplied string (could be env var or a complex integer expression)
def InterpretValue(param, inpValue, inpType=dataType.STRING, opt=opts.ALL):
    retValue = inpValue

    # first expand any env vars
    if (opt & opts.EXPAND_ENVVARS) and bool(inpValue) and isinstance(inpValue, basestring) and inpValue.find('$') != -1:
        inpValue = ExpandAnyEnvVars(inpValue)

    # now remove any double or single quotes
    if (opt & opts.REMOVE_QUOTES) and bool(inpValue) and isinstance(inpValue, basestring) and \
            ((inpValue[0] == '"' and inpValue[-1] == '"') or
                 (inpValue[0] == "'" and inpValue[-1] == "'")):
        inpValue = inpValue[1:-1]

    if inpType == dataType.STRING:
        if inpValue is None:
            if (opt & opts.NONE_IS_NONE):
                retValue = None
            else:
                # interpret None as empty string
                retValue = ""
        else:
            retValue = str(inpValue)

    elif inpType == dataType.INTEGER:
        # if still no value
        if inpValue is None and (opt & opts.NONE_IS_NONE):
            retValue = None
        else:
            # support hexadecimal formats and simple summations, inpValue can also be an empty string
            intValid, retValue = InterpretNumeric(inpValue)
            if not intValid:
                RepWarning("Check validity of [%s] value [%s] - treating as zero" % (param, inpValue))
    else:
        RepError('bad arg type enum [%d]' % inpType, exitCodes.INTERNAL_ERROR)

    RepDebug(5, "Evaluating [%s] %s value [%s] as [%s]" % (param, dataTypeLabel[inpType-1], inpValue, retValue))

    return retValue


def AssignNumeric(param, argValue, cfgValue=None, unknown = False):
    intValue = 0
    # if arg value supplied, use this
    if argValue is not None:
        intValue = InterpretValue(param, argValue, dataType.INTEGER)
    # any config value
    elif cfgValue is not None:
        intValue = InterpretValue(param, cfgValue, dataType.INTEGER)
    return intValue






# - - - - - - - - - - - - - - - - - - - - - - - -
# Config file parsing

def ConfigSectionString(reqSection, argOption):
    argName = argOption.lstrip('-')
    try:
        value = configFile.get(reqSection, argName)
        RepDebug(3, 'Config - [%s] [%s] = [%s]' % (reqSection, argName, value))
        # if embedded $ environment variable
        if value and value.find('$') != -1:
            value = ExpandAnyEnvVars(value)
    except:
        value = None
        RepDebug(4, 'Config - undefined [%s] [%s] ' % (reqSection, argName ))
    return value

def RegisterArg(argOption, argConfigSection, argDescription, argSystemDefault, argType):
    argName = argOption.lstrip('-')
    # see if there is a [default] value in the config file - our preferred value source
    cfgDefault = ConfigSectionString(argConfigSection, argName)

    # if a blank config value (xyz="") defined (treat as if None but do not use any system default)
    if cfgDefault == "":
        cfgDefault = None

    # if no config value defined, use whatever our 'hardcoded' system default is - could also be a blank
    elif cfgDefault is None:
        RepDebug(4, 'Using system default [%s]' % argSystemDefault)
        cfgDefault = argSystemDefault

    # interpret the value supplied in the config file (envvars will already have been expanded)
    cfgDefault = InterpretValue(argName, cfgDefault, argType)

    # NOTE: anything supplied on the command line will override these 'defaults'
    if argType == dataType.STRING:
        argParser.add_argument(argOption,
                               help=argDescription,
                               default=cfgDefault)
    elif argType == dataType.INTEGER:
        argParser.add_argument(argOption,
                               help=argDescription,
                               type=int,
                               default=cfgDefault)
    else:
        RepError('bad arg type enum [%d]' % argType, exitCodes.INTERNAL_ERROR)


def RegisterStringArg(argOption, argConfigSection, argDescription, argSystemDefault=None):
    return RegisterArg(argOption, argConfigSection, argDescription, argSystemDefault, dataType.STRING)


def RegisterIntegerArg(argOption, argConfigSection, argDescription, argSystemDefault=None):
    return RegisterArg(argOption, argConfigSection, argDescription, argSystemDefault, dataType.INTEGER)


# - - - - - - - - - - - - - - - - - - - - - - - -
# Basic endpoint Service

# generic
class Service:

    def __init__(self):
        self.transport = 'http'
        self.hostname = 'localhost'
        self.port = '8080'

    def setTransport(self, inTransport):
        self.transport = inTransport

    def getTransport(self):
        return self.transport

    def setHostname(self, inHost):
        self.hostname = inHost

    def getHostname(self):
        return self.hostname

    def setPort(self, inPort):
        self.port = inPort

    def getPort(self):
        return self.port

    def getServiceURL(self, inServicePath = ''):
        url = self.transport + '://' + self.hostname
        if bool(self.port):
            url += ':' + self.port
        if inServicePath:
            url += inServicePath
        return url

    def getWSURL(self, inService):
        # note version of WS we are using
        return self.getServiceURL('/ws/' + wsVersion + '/' + inService + '?wsdl')

    def setServicesSecurity(self, client, inUser, inPassword):
        security = Security()
        token = UsernameToken(inUser, inPassword)
        security.tokens.append(token)
        client.set_options(wsse=security)


# - - - - - - - - - - - - - - - - - - - - - - - -
# Coverity Configuration Service (WebServices)

class CoverityConfigurationService(Service):

    # constructor
    def __init__(self, inTransport, inHostname, inPort):
        self.setTransport(inTransport)
        self.setHostname(inHostname)
        self.setPort(inPort)
        self.knownCheckers = None
        fqUrl = self.getWSURL('configurationservice')
        try:
            self.client = Client(fqUrl)
            RepDebug(3, "Validated presence of Coverity Configuration Service [%s]" % fqUrl)
        except:
            self.client = None
            RepError("No such Coverity Configuration Service [%s]" % fqUrl, exitCodes.COV_COMMS_ERROR)

    def setSecurity(self, inUser, inPassword):
        self.setServicesSecurity(self.client, inUser, inPassword)
        versionDO    = self.getVersion()
        if versionDO is None:
            RepError("Authentication to [%s] FAILED for [%s] account - check password" % (self.getServiceURL(), inUser), exitCodes.COV_COMMS_ERROR)
        else:
            RepDebug(3, "Authentication to [%s] using [%s] account was OK - version [%s]" % (self.getServiceURL(), inUser,versionDO.externalVersion))

    def getVersion(self):
        try:
            return self.client.service.getVersion()
        except:
            return None

    def create(self, in_obj):
        return self.client.factory.create(in_obj)

    def getProjectName(self, thisStreamDO):
        return thisStreamDO.primaryProjectId.name

    def getTriageStore(self, thisStreamDO):
        return thisStreamDO.triageStoreId.name

    def getStreamDO(self, stream_name):
        filterSpec = self.client.factory.create('streamFilterSpecDataObj')

        # use stream name as an initial glob pattern
        filterSpec.namePattern = stream_name

        # get all the streams that match
        resStreamDOList = self.client.service.getStreams(filterSpec)

        # find the one with a matching name
        for thisStream in resStreamDOList:
            if StringsMatch(thisStream.id.name, stream_name):
                return thisStream
        return None

    # get a list of the snapshots in a named stream
    def getSnapshotsForStream(self, stream_name):
        streamIdDO = self.client.factory.create('streamIdDataObj')
        streamIdDO.name = stream_name
        # optional filter specification
        filterSpec = self.client.factory.create('snapshotFilterSpecDataObj')
        # return a list of snapshotDataObj
        return self.client.service.getSnapshotsForStream(streamIdDO, filterSpec)

    # get the nth snapshot (base 1) - minus numbers to count from the end backwards (-1 = last)
    def getSnapshotId(self, listOfSnapshotDO, whichSnapshot=1):
        if bool(whichSnapshot):
            numSnapshots = len(listOfSnapshotDO)
            if whichSnapshot < 0:
                required = numSnapshots + whichSnapshot + 1
            else:
                required = whichSnapshot

            if abs(required) > 0 and abs(required) <= numSnapshots:
                # base zero
                reqSnapshot = listOfSnapshotDO[required-1]
                return reqSnapshot.id
        return 0

    # get detailed information about a single snapshot
    def getSnapshotDetail(self, snapshotId):
        snapshotIdDO = self.client.factory.create('snapshotIdDataObj')
        snapshotIdDO.id = snapshotId
        # return a snapshotInfoDataObj
        return self.client.service.getSnapshotInformation(snapshotIdDO)

    def getListOfCheckers(self):
        if not self.knownCheckers:
            self.knownCheckers = self.client.service.getCheckerNames()
        return self.knownCheckers

    # lookup the listed checker names, validate and add to filter spec, return a validated, expanded list
    def validateCheckerReqAndAdd(self, reqCheckers, filterSpecDO):
        RepDebug(4, 'Validate list of required checker(s) [%s]' % reqCheckers)
        cntCheckers = 0
        validatedCheckers = ""
        delim = ""
        # ensure we are primed
        self.getListOfCheckers()
        inputList = [reqCheckers]
        parser = csv.reader(inputList)
        # walk the list of all possible Coverity checkers once only - its a long list
        for fields in parser:
            for thisChecker in self.knownCheckers:
                # walk the list of required checkers until exhausted or a match
                for i, thisField in enumerate(fields):
                    # if we want this Coverity checker
                    if StringsMatch(thisChecker, thisField):
                        RepDebug(5, '[%s] yields (%s)' % (thisField, thisChecker))
                        if filterSpecDO:
                            cntCheckers += 1
                            filterSpecDO.checkerList.append(thisChecker)
                        validatedCheckers += delim + thisChecker
                        delim = ","
                        # try the next named Coverity checker
                        break
        return cntCheckers, validatedCheckers

    # lookup the list of impact statuses, add to filter spec and return a validated list
    def validateImpactStatusReqAndAdd(self, reqImpact, filterSpecDO):
        RepDebug(4, 'Validate required impact status [%s]' % reqImpact)
        cntImpacts = 0
        validatedImpact = ""
        delim = ""
        inputList = [reqImpact]
        parser = csv.reader(inputList)
        # walk the list of all possible impact statuses
        for fields in parser:
            for thisImpact in covImpactsList:
                # walk the list of required impact status until exhausted or a match
                for i, thisField in enumerate(fields):
                    # if we want this impact status
                    if StringsMatch(thisImpact, thisField):
                        RepDebug(5, '[%s] is valid (%s)' % (thisField, thisImpact))
                        if filterSpecDO:
                            filterSpecDO.impactNameList.append(thisImpact)
                            cntImpacts += 1
                            validatedImpact += delim + thisImpact
                        delim = ","
                        # try the next impact status
                        break
        return cntImpacts,validatedImpact

    # lookup the list of issue kinds, add to filter spec and return a validated list
    def validateKindReqAndAdd(self, reqKind, filterSpecDO):
        RepDebug(4, 'Validate required issue kind [%s]' % reqKind)
        cntKinds = 0
        validatedKind = ""
        delim = ""
        inputList = [reqKind]
        parser = csv.reader(inputList)
        # walk the list of all possible kinds
        for fields in parser:
            for thisKind in covKindsList:
                # walk the list of required kinds until exhausted or a match
                for i, thisField in enumerate(fields):
                    # if we want this kind
                    if StringsMatch(thisKind, thisField):
                        RepDebug(5, '[%s] is valid (%s)' % (thisField, thisKind))
                        if filterSpecDO:
                            filterSpecDO.issueKindList.append(thisKind)
                            cntKinds += 1
                            validatedKind += delim + thisKind
                        delim = ","
                        # try the next kind
                        break
        return cntKinds,validatedKind

    # lookup the list of classifications, add to filter spec and return a validated list
    def validateClassificationReqAndAdd(self, reqClassification, filterSpecDO):
        RepDebug(4, 'Validate required classification [%s]' % reqClassification)
        cntClassifications = 0
        validatedClassification = ""
        delim = ""
        inputList = [reqClassification]
        parser = csv.reader(inputList)
        # walk the list of all possible classifications
        for fields in parser:
            for thisClassification in covClassificationsList:
                # walk the list of required classifications until exhausted or a match
                for i, thisField in enumerate(fields):
                    # if we want this classification
                    if StringsMatch(thisClassification, thisField):
                        RepDebug(5, '[%s] is valid (%s)' % (thisField, thisClassification))
                        if filterSpecDO:
                            filterSpecDO.classificationNameList.append(thisClassification)
                            cntClassifications += 1
                            validatedClassification += delim + thisClassification
                        delim = ","
                        # try the next classification
                        break
        return cntClassifications,validatedClassification

    # lookup the list of actions, add to filter spec and return a validated list
    def validateActionReqAndAdd(self, reqAction, filterSpecDO):
        RepDebug(4, 'Validate required action [%s]' % reqAction)
        cntActions = 0
        validatedAction = ""
        delim = ""
        inputList = [reqAction]
        parser = csv.reader(inputList)
        # walk the list of all possible actions
        for fields in parser:
            for thisAction in covActionsList:
                # walk the list of required actions until exhausted or a match
                for i, thisField in enumerate(fields):
                    # if we want this actions
                    if StringsMatch(thisAction, thisField):
                        RepDebug(5, '[%s] is valid (%s)' % (thisField, thisAction))
                        if filterSpecDO:
                            filterSpecDO.actionNameList.append(thisAction)
                            cntActions += 1
                            validatedAction += delim + thisAction
                        delim = ","
                        # try the next action
                        break
        return cntActions,validatedAction


    def getSystemConfig(self):
        return self.client.service.getSystemConfig()


# - - - - - - - - - - - - - - - - - - - - - - - -
# Coverity Defect Service (WebServices)

class CoverityDefectService(Service):

    # constructor
    def __init__(self, inTransport, inHostname, inPort):
        self.setTransport(inTransport)
        self.setHostname(inHostname)
        self.setPort(inPort)
        self.covCS = None
        self.filters = ""
        self.snapshotEarlier = 0
        self.snapshotLater = 0

        fqUrl = self.getWSURL('defectservice')
        try:
            self.client = Client(fqUrl)
            RepDebug(3, "Validated presence of Coverity Defect Service [%s]" % fqUrl)
        except:
            self.client = None
            RepError("No such Coverity Defect Service [%s]" % fqUrl, exitCodes.COV_COMMS_ERROR)

    def setSecurity(self, inUser, inPass):
        self.setServicesSecurity(self.client, inUser, inPass)

    def setConfigurationService(self, covCS):
        self.covCS = covCS

    def create(self, in_obj):
        return self.client.factory.create(in_obj)

    def checkSnapshotIds(self):
        # not sure which snapshots we are referring to yet
        snapshotID1 = None
        snapshotID2 = None

        # if specific snapshot defn(s) have been supplied
        if bool(options.csnapshots):
            valid,snapshotID1,snapshotID2=parseTwoPartTerm(options.csnapshots)
            if not valid:
                RepError("Invalid csnapshots definition [%s] - must be [ [defn1],[defn2] ] " % options.csnapshots,
                         exitCodes.INVALID_ARG)

        # if no snap shots defined - assume the last and one before the last in the stream
        if bool(snapshotID1):
            self.snapshotEarlier = snapshotID1
        else:
            # default earlier snapshot - the one before last in the stream
            self.snapshotEarlier = 'lastBefore(last())'

        if bool(snapshotID2):
            self.snapshotLater = snapshotID2
        else:
            # default later snapshot - the last one in the stream
            self.snapshotLater = 'last()'

        # must be different
        if self.snapshotEarlier == self.snapshotLater:
            RepError("Defined snapshots must be different [%s]?" % snapshotEarlier, exitCodes.INVALID_ARG)

        RepDebug(2, "Earlier snapshot [%s]" % self.snapshotEarlier)
        RepDebug(2, "Later snapshot   [%s]" % self.snapshotLater)

        return self.snapshotEarlier,self.snapshotLater


    def getMergedDefectsForProjectAndStream(self, projectName, streamName, dataScope):
        RepDebug(3, 'Querying Coverity for cscope [%d] defects in project [%s] stream [%s] ...' %(dataScope, projectName, streamName))

        # define the project
        projectIdDO = self.client.factory.create('projectIdDataObj')
        projectIdDO.name = projectName

        # and the stream
        streamIdDO = self.client.factory.create('streamIdDataObj')
        streamIdDO.name = streamName

        # create filter spec
        filterSpecDO = self.client.factory.create('snapshotScopeDefectFilterSpecDataObj')

        # only for this stream
        filterSpecDO.streamIncludeNameList.append(streamIdDO)

        # apply any filter on checker names
        if bool(options.checker):
            RepDebug(3, 'Using checker filter [%s]' % options.checker)
            # pass entire list of requirements to be validated and selected
            cntCheckers,validatedCheckers = self.covCS.validateCheckerReqAndAdd(options.checker, filterSpecDO)
            if not cntCheckers:
                RepError('Invalid checker requirement [%s]' % options.checker, exitCodes.INVALID_ARG)
            else:
                RepDebug(4, 'Resolves to [%s]' % validatedCheckers)
                self.filters += ("<checkers(%d)> " % cntCheckers)

        # apply any filter on impact status
        if bool(options.impact):
            RepDebug(3, 'Using impact status filter [%s]' % options.impact)
            # pass entire list of requirements to be validated and selected
            cntImpact,validatedImpact = self.covCS.validateImpactStatusReqAndAdd(options.impact, filterSpecDO)
            if not cntImpact:
                RepError('Invalid impact status requirement [%s]' % options.impact, exitCodes.INVALID_ARG)
            else:
                RepDebug(4, 'Resolves to [%s]' % validatedImpact)
                self.filters += ( "<impacts(%d)> " % cntImpact)

        # apply any filter on issue kind
        if bool(options.kind):
            RepDebug(3, 'Using issue kind filter [%s]' % options.kind)
            # pass entire list of requirements to be validated and selected
            cntKind,validatedKind = self.covCS.validateKindReqAndAdd(options.kind, filterSpecDO)
            if not cntKind:
                RepError('Invalid issue kind requirement [%s]' % options.kind, exitCodes.INVALID_ARG)
            else:
                RepDebug(4, 'Resolves to [%s]' % validatedKind)
                self.filters += ( "<kind(%d)> " % cntKind)

        # apply any filter on classification
        if bool(options.classification):
            RepDebug(3, 'Using classification filter [%s]' % options.classification)
            # pass entire list of requirements to be validated and selected
            cntClassification,validatedClassification = self.covCS.validateClassificationReqAndAdd(options.classification, filterSpecDO)
            if not cntClassification:
                RepError('Invalid classification requirement [%s]' % options.classification, exitCodes.INVALID_ARG)
            else:
                RepDebug(4, 'Resolves to [%s]' % validatedClassification)
                self.filters += ( "<classifications(%d)> " % cntClassification)

        # apply any action filter
        if bool(options.action):
            RepDebug(3, 'Using action filter [%s]' % options.action)
            # pass entire list of requirements to be validated and selected
            cntAction,validatedAction = self.covCS.validateActionReqAndAdd(options.action, filterSpecDO)
            if not cntAction:
                RepError('Invalid action requirement [%s]' % options.action, exitCodes.INVALID_ARG)
            else:
                RepDebug(4, 'Resolves to [%s]' % validatedAction)
                self.filters += ( "<actions(%d)> " % cntAction)

        # apply any filter on Components
        if bool(options.component):
            RepDebug(3, 'Using Component filter [%s]' % options.component)
            inputList = [options.component]
            parser = csv.reader(inputList)

            for fields in parser:
                for i, thisField in enumerate(fields):
                    thisField = thisField.strip()
                    RepDebug(4, "Component (%d) = [%s] " % (i+1, thisField))
                    componentIdDO = self.client.factory.create('componentIdDataObj')
                    componentIdDO.name = thisField
                    filterSpecDO.componentIdList .append(componentIdDO)
            self.filters += ("<components(%d)> " % (i+1))

        # apply any filter on CWE values
        if bool(options.cwe):
            RepDebug(3, 'Using CWE filter [%s]' % options.cwe)
            inputList = [options.cwe]
            parser = csv.reader(inputList)

            for fields in parser:
                for i, thisField in enumerate(fields):
                    thisField = thisField.strip()
                    RepDebug(4, "cwe (%d) = [%s] " % (i+1, thisField))
                    filterSpecDO.cweList.append(thisField)
            self.filters += ("<CWEs(%d)> " % (i+1))

        # apply any filter on CID values
        if bool(options.cid):
            RepDebug(3, 'Using CID filter [%s]' % options.cid)
            inputList = [options.cid]
            parser = csv.reader(inputList)

            for fields in parser:
                for i, thisField in enumerate(fields):
                    thisField = thisField.strip()
                    RepDebug(4, "cid (%d) = [%s] " % (i+1, thisField))
                    filterSpecDO.cidList.append(thisField)
            self.filters += ("<CIDs(%d)> " % (i+1))

        # if a special custom attribute value requirement
        if bool(options.custom):
            RepDebug(3, 'Using attribute filter [%s]' % options.custom)
            # split the name:value[;name:value1[,value2]]
            inputList = [options.custom]
            defnParser = csv.reader(inputList, delimiter=';')

            for fields in defnParser:
                for i, thisDefn in enumerate(fields):
                    thisDefn = thisDefn.strip()
                    valid, name, compValue = parseTwoPartTerm(thisDefn, ':')
                    if valid:
                        RepDebug(4, "attr (%d) [%s] = any of ..." % (i + 1, name))

                        attributeDefinitionIdDO = self.client.factory.create('attributeDefinitionIdDataObj')
                        attributeDefinitionIdDO.name = name

                        attributeDefinitionValueFilterMapDO = self.client.factory.create('attributeDefinitionValueFilterMapDataObj')
                        attributeDefinitionValueFilterMapDO.attributeDefinitionId = attributeDefinitionIdDO

                        # if there are multiple values delimited with comma
                        valueList = [compValue]
                        valueParser = csv.reader(valueList, delimiter=',')

                        for valueFields in valueParser:
                            for i, thisValue in enumerate(valueFields):
                                RepDebug(4, "             [%s]" % thisValue)

                                attributeValueIdDO = self.client.factory.create('attributeValueIdDataObj')
                                attributeValueIdDO.name = thisValue

                                attributeDefinitionValueFilterMapDO.attributeValueIds.append(attributeValueIdDO)

                        filterSpecDO.attributeDefinitionValueFilterMap.append(attributeDefinitionValueFilterMapDO)
                    else:
                        RepError('Invalid custom attribute definition [%s]' % thisDefn, exitCodes.INVALID_ARG)
            self.filters += ("<Attrs(%d)> " % (i + 1))

        # create page spec
        pageSpecDO = self.client.factory.create('pageSpecDataObj')
        pageSpecDO.pageSize = 2500
        pageSpecDO.sortAscending = True
        pageSpecDO.startIndex = 0

        # create snapshot scope
        snapshotScopeDO = self.client.factory.create('snapshotScopeSpecDataObj')

        snapshotScopeDO.showOutdatedStreams = False
        snapshotScopeDO.compareOutdatedStreams = False

        if dataScope == dataScopeType.ALL2:
            snapshotScopeDO.showSelector = self.snapshotEarlier
            snapshotScopeDO.compareSelector = self.snapshotLater

        # union? of all issues - not sure this actually does what the docs say
        # if issueComparison is unset == ABSENT & PRESENT
        # just get all those that are still current in the last snapshot
        elif dataScope == dataScopeType.ALL:
            snapshotScopeDO.showSelector = self.snapshotLater
            snapshotScopeDO.compareSelector = self.snapshotEarlier

        # newly detected
        elif dataScope == dataScopeType.NEWLY_DETECTED:
            filterSpecDO.issueComparison = 'ABSENT'
            snapshotScopeDO.showSelector = self.snapshotLater
            snapshotScopeDO.compareSelector = self.snapshotEarlier
            # only want new or triaged issues that are still "outstanding"
            filterSpecDO.statusNameList.append('New')
            filterSpecDO.statusNameList.append('Triaged')

        # newly eliminated
        elif dataScope == dataScopeType.NEWLY_ELIMINATED:
            filterSpecDO.issueComparison = 'ABSENT'
            snapshotScopeDO.showSelector = self.snapshotEarlier
            snapshotScopeDO.compareSelector = self.snapshotLater

        # newly dismissed (dismissed since the earlier snapshot)
        elif dataScope == dataScopeType.NEWLY_DISMISSED:
            # was still present in the later snapshot
            filterSpecDO.issueComparison = 'PRESENT'
            # might have to change these if we use non default snapshot grammar @TODO
            snapshotScopeDO.showSelector = self.snapshotLater
            snapshotScopeDO.compareSelector = self.snapshotLater
            # and currently marked as Dismissed, we just don't know when this state change occurred
            # will have to be filtered later
            filterSpecDO.statusNameList.append('Dismissed')

        # common to the 2 snapshots
        elif dataScope == dataScopeType.COMMON:
            filterSpecDO.issueComparison = 'PRESENT'
            snapshotScopeDO.showSelector = self.snapshotEarlier
            snapshotScopeDO.compareSelector = self.snapshotLater

        RepDebug(1, 'Running Coverity query...')
        resMergedDefectsPageDO = self.client.service.getMergedDefectsForSnapshotScope(projectIdDO, filterSpecDO,
                                                                                      pageSpecDO, snapshotScopeDO)

        return resMergedDefectsPageDO


    # get the details pertaining a specific CID - it may not have defect instance details if newly eliminated (fixed)
    def getStreamDefectsForCID(self, cid, streamName):
        RepDebug(4, 'Fetching data for CID [%s] in stream [%s] ...' %(cid, streamName))

        mergedDefectIdDO = self.client.factory.create('mergedDefectIdDataObj')
        mergedDefectIdDO.cid = cid

        filterSpec = self.client.factory.create('streamDefectFilterSpecDataObj')
        filterSpec.includeDefectInstances = True
        filterSpec.includeHistory = True

        streamIdDO = self.client.factory.create('streamIdDataObj')
        streamIdDO.name = streamName
        filterSpec.streamIdList.append(streamIdDO)

        return self.client.service.getStreamDefects(mergedDefectIdDO, filterSpec)

    def AddAttributeNameAndValue(self, defectStateSpecDO, attrName, attrValue):

        # name value pair to update
        attributeDefinitionIdDO = self.client.factory.create('attributeDefinitionIdDataObj')
        attributeDefinitionIdDO.name = attrName

        attributeValueIdDO = self.client.factory.create('attributeValueIdDataObj')
        attributeValueIdDO.name = attrValue

        # wrap the name/value pair
        defectStateAttributeValueDO = self.client.factory.create('defectStateAttributeValueDataObj')
        defectStateAttributeValueDO.attributeDefinitionId = attributeDefinitionIdDO
        defectStateAttributeValueDO.attributeValueId = attributeValueIdDO

        # add to our list
        defectStateSpecDO.defectStateAttributeValues.append(defectStateAttributeValueDO)


    # update the external reference id to a third party
    def updateExtReferenceAttributeForCID(self, cid, triageStore, extRefId):
        RepDebug(2, 'Updating Coverity - CID [%s] in TS [%s] with Ext Ref [%s]' % (cid, triageStore, extRefId))

        # triage store identifier
        triageStoreIdDO = self.client.factory.create('triageStoreIdDataObj')
        triageStoreIdDO.name = triageStore

        # CID to update
        mergedDefectIdDO = self.client.factory.create('mergedDefectIdDataObj')
        mergedDefectIdDO.cid = cid


        # if an ext ref id value supplied
        if bool(extRefId):
            attrValue = extRefId
            commentValue = "%s recorded reference to new JIRA ticket." % scriptName
        else:
            # set to a space - which works as a blank without the WS complaining :-)
            attrValue = " "
            commentValue = "%s cleared former JIRA ticket reference." % scriptName

        # if a Coverity comment to tag on the end
        if bool(options.ccomment):
            commentValue += " " + options.ccomment
        RepDebug(2, 'Comment = [%s]' % commentValue)

        defectStateSpecDO = self.client.factory.create('defectStateSpecDataObj')

        # name value pairs to add to this update
        self.AddAttributeNameAndValue(defectStateSpecDO, nameOfExtReferenceAttribute, attrValue)
        self.AddAttributeNameAndValue(defectStateSpecDO, nameOfCommentAttribute, commentValue)

        # apply the update
        return self.client.service.updateTriageForCIDsInTriageStore(triageStoreIdDO, mergedDefectIdDO, defectStateSpecDO)


    # get the current impact of the 'nth' incident of this issue (High/Medium/Low)
    def getInstanceImpact(self, streamDefectDO, instanceNumber=1):
        counter = instanceNumber
        for thisInstance in streamDefectDO.defectInstances:
            counter -= 1
            if counter == 0:
                return thisInstance.impact.name
        return ""

    # lookup the value of a named attribute
    def getValueForNamedAttribute(self, streamDefectDO, attributeName):
        RepDebug(4, 'Get value for cov attribute [%s]' % attributeName)
        for attrValue in streamDefectDO.defectStateAttributeValues:
            if StringsMatch(attrValue.attributeDefinitionId.name, attributeName):
                RepDebug(4, 'Resolves to [%s]' % attrValue.attributeValueId.name)
                return str(attrValue.attributeValueId.name)
        RepDebug(4, 'Not found')
        return ""


    # get specified attribute was set to given matching value
    def getEventAttributeValue(self, thisDefectStateDO, attributeName, attributeValue=None):
        if bool(attributeValue):
            RepDebug(4, 'Searching for attribute [%s] with value [%s]' % (attributeName, attributeValue))
        else:
            RepDebug(4, 'Searching for attribute [%s]' % attributeName)

        for thisAttrValue in thisDefectStateDO.defectStateAttributeValues:
            # check if we have the named attribute
            if StringsMatch(thisAttrValue.attributeDefinitionId.name, attributeName):
                # if any value supplied or it matches requirement
                if bool(thisAttrValue.attributeValueId.name) and (not attributeValue or StringsMatch(thisAttrValue.attributeValueId.name, attributeValue)):
                    RepDebug(4, 'Found [%s] = [%s]' % (thisAttrValue.attributeDefinitionId.name, thisAttrValue.attributeValueId.name))
                    return True, thisAttrValue.attributeValueId.name
                else:
                    # break attribute name search - either no value or it doesn't match
                    break
        RepDebug(4, 'Not found')
        return False, None

    # get the nth matching attribute or attribute name/value pair and return the
    # attribute value or associated value of another named attribute
    def SeekNthMatch(self, thisEventHistory, nthEvent, attributeName, attributeValue, associatedAttrName=None):
        resFound = False
        resDefectStateDO = None
        resAttrValue = None
        numMatch = 0
        join = ""
        for thisDefectStateDO in thisEventHistory:
            # look for the named attribute or the name-value pair (if a value supplied) in this triage event
            reqEventFound, reqAttrValue = self.getEventAttributeValue(thisDefectStateDO, attributeName, attributeValue)
            # if there was a suitable named attribute/pair
            if reqEventFound:
                numMatch += 1

                if bool(associatedAttrName):
                    reqAssocAttrFound, reqAssocAttrValue = self.getEventAttributeValue(thisDefectStateDO, associatedAttrName)
                    if reqAssocAttrFound:
                        reqAttrValue = reqAssocAttrValue
                    else:
                        # failed to get associated attribute - skip this result
                        break
                # all values to be chained together
                if 0 == nthEvent:
                    # first one
                    if not resFound:
                        resAttrValue = reqAttrValue
                        resFound = True
                        join = "|"
                    else:
                        resAttrValue += join + reqAttrValue
                    resDefectStateDO = thisDefectStateDO
                # correct one?
                elif numMatch == nthEvent:
                    # we're done
                    return True, thisDefectStateDO, reqAttrValue
        return resFound, resDefectStateDO, resAttrValue


    # get event when specified attribute was set to given matching value
    def getEventForAttributeChange(self, thisStreamDefectDO, nthTerm, attributeName, attributeValue=None, associatedAttrName=None):
        RepDebug(4, 'Searching for triage event n=[%d] where attribute [%s] is set to [%s]' % (nthTerm, attributeName, attributeValue))

        # if all or nth attributes of this name to be fetched
        if nthTerm >= 0:
            found, thisDefectStateDO, value = self.SeekNthMatch(thisStreamDefectDO.history, nthTerm, attributeName, attributeValue, associatedAttrName)
        else:
            found, thisDefectStateDO, value = self.SeekNthMatch(reversed(thisStreamDefectDO.history), abs(int(nthTerm)), attributeName, attributeValue, associatedAttrName)

        return found,thisDefectStateDO, value


    # get the external ref id attribute value
    def getExtReferenceId(self, streamDefectDO):
        return self.getValueForNamedAttribute(streamDefectDO, nameOfExtReferenceAttribute)

    # get the defect status attribute value
    def getDefectStatus(self, streamDefectDO):
        return self.getValueForNamedAttribute(streamDefectDO, nameOfDefectStatusAttribute)

    # get the classification attribute value
    def getClassification(self, streamDefectDO):
        return self.getValueForNamedAttribute(streamDefectDO, nameOfClassificationAttribute)

    # get the action attribute value
    def getAction(self, streamDefectDO):
        return self.getValueForNamedAttribute(streamDefectDO, nameOfActionAttribute)

    # get (build) the defect URL to the Coverity CID
    # http://machine1.eng.company.com:8080/query/defects.htm?stream=StreamA&cid=1234
    def getCoverityDefectURL(self, streamName, cid):
        return self.getServiceURL('/query/defects.htm?stream=%s&cid=%s' % (streamName, str(cid)))




# - - - - - - - - - - - - - - - - - - - - - - - -
# Main Entry Point

def main():

    # check the Coverity credentials (port is not always required)
    if (not bool(options.ctransport) or
        not bool(options.chostname)):
        RepError('Incomplete Coverity host definition [%s://%s]' % (options.ctransport, options.chostname), exitCodes.MISSING_ARG)

    if (not bool(options.cusername) or
        not bool(options.cpassword)):
        RepError('Missing Coverity account credentials [%s/%s]' % (options.cusername, options.cpassword), exitCodes.MISSING_ARG)

    validMax=False
    validSkip=False
    validSensible=False
    maxValue=None
    skipValue=None
    sensibleValue=None

    # if we are to skip the first few results
    if bool(options.skip):
        validSkip,skipValue = InterpretNumeric(options.skip)
        if not validSkip or skipValue <= 0 or skipValue > 9999:
            RepError("Invalid 'skip' limit [%s]" % options.skip, exitCodes.INVALID_ARG)

    # if a maximum results limit to process
    if bool(options.max):
        validMax,maxValue = InterpretNumeric(options.max)
        if not validMax or maxValue <= 0 or maxValue > 9999:
            RepError("Invalid 'max' limit [%s]" % options.max, exitCodes.INVALID_ARG)

    # if a sensible results limit to work to
    if bool(options.sensible):
        validSensible,sensibleValue = InterpretNumeric(options.sensible)

        # if the sensible limit is breached we can set a max to only process a portion of this result set
        if validSensible and validMax and maxValue < sensibleValue:
            RepWarning("Max limit [%d] will constrain processing over sensible limit [%d]" % (maxValue, sensibleValue))
        elif not validSensible or sensibleValue <= 0 or sensibleValue > 9999:
            RepError("Invalid 'sensible' limit [%s]" % options.sensible, exitCodes.INVALID_ARG)


    # now think about logging
    global hLog, hOutput

    # Open a log file
    if bool(options.log):
        hLogFile = open(options.log, 'w')
        if hLogFile:
            RepNote('Logging to: ' + options.log)
            # switch to using the log file from now on
            hLog = hLogFile
            RepMsg("Started", str(datetime.datetime.now()))
        else:
            RepError("Failed to create log file [%s] - access permissions?" % options.log, exitCodes.INVALID_ARG)

    if options.mode & modeTypes.DUMP:
        # Open an output file
        if bool(options.output):
            hOutput = open(options.output, 'w')
            if hOutput:
                RepNote('Outputting to: ' + options.output)
            else:
                RepError("Failed to create output file [%s] - access permissions?" % options.output, exitCodes.INVALID_ARG)
    else:
        if bool(options.output):
            RepWarning("Ignoring output file - not running in DUMP mode")

    # Mandatory: a Coverity stream name must be supplied
    if not bool(options.cstream):
        RepError('No Coverity stream name has been supplied', exitCodes.MISSING_ARG)

    # get the Coverity configuration service
    covCS = CoverityConfigurationService(options.ctransport, options.chostname, options.cport)
    covCS.setSecurity(options.cusername, options.cpassword)

    # check the named stream exists plus we also need a Project name for it
    ourStreamDO = covCS.getStreamDO(options.cstream)

    if ourStreamDO is None:
        RepError('No such Coverity stream [%s] found on [%s]' % (options.cstream, covCS.getServiceURL()), exitCodes.INVALID_ARG)

    # Note which project it belongs to
    projectNameForStream = covCS.getProjectName(ourStreamDO)
    RepDebug(2, 'Coverity stream [%s] is located in project [%s]' % (options.cstream, projectNameForStream))

    # check we have snapshots in this stream
    snapshotIdDO = covCS.getSnapshotsForStream(options.cstream)

    snapshotCount = len(snapshotIdDO)

    # if there are no snapshots
    if snapshotCount < 1:
        RepError('Stream [%s] is empty - nothing to do or incorrect stream name?' % options.cstream, exitCodes.PROC_ERROR)

    # if fewer than 2 snapshots
    if snapshotCount < 2:
        # if looking for newly detected
        if options.cscope == dataScopeType.NEWLY_DETECTED:
            # unless mode is changed, this is not a recommended scenario
            if options.mode & modeTypes.IGNORE_SNAPSHOT_COUNT:
                RepWarning('Stream [%s] contains only ONE SNAPSHOT - ALL ISSUES are potentially newly detected! Overriding check with --mode' % options.cstream)
            else:
                RepError('Stream [%s] contains only one snapshot - cannot perform a delta comparison to find new defects.  See --mode' % options.cstream, exitCodes.PROC_ERROR)

    RepDebug(2, 'Stream [%s] contains [%d] snapshots' % (options.cstream, snapshotCount))

    # note the triage store for this Coverity stream too
    triageStoreForStream = covCS.getTriageStore(ourStreamDO)
    RepDebug(2, 'Stream [%s] belongs to triage store [%s]' % (options.cstream, triageStoreForStream))

    # get the Coverity defect service
    covDS = CoverityDefectService(options.ctransport, options.chostname, options.cport)
    covDS.setSecurity(options.cusername, options.cpassword)
    covDS.setConfigurationService(covCS)

    # --- PRE-PROCESSING VALIDATION ---
    snapshotDetailsDismissed = None
    covDS.checkSnapshotIds()

    # if we are looking for defects dismissed since the previous commit
    if options.cscope == dataScopeType.NEWLY_DISMISSED:

        # if we know when the earlier snapshot was created we're only interested in any triage event
        # to dismiss this defect since this time
        snapshotIdValid,snapshotIdCutoff = InterpretNumeric(covDS.snapshotEarlier, 1)

        # if we have not supplied a numeric snapshot id (i.e. using the grammar terminology)
        if not snapshotIdValid:
            # Ideally this would directly use the snapshot grammar e.g. (lastBefore(last())  @TODO
#            snapshotGrammar = covDS.snapshotEarlier
            if covDS.snapshotEarlier == "lastBefore(last())":
                snapshotGrammar = "-2"
            elif covDS.snapshotEarlier == "last()":
                snapshotGrammar = "-1"
            elif covDS.snapshotEarlier == "first()":
                snapshotGrammar = "1"
            else:
                RepError("Sorry, we can't handle this snapshot grammar term [%s] for checking dismissed defects, use IDs?" % covDS.snapshotEarlier, exitCodes.INTERNAL_ERROR)

            # get the id this defn relates to
            snapshotIdCutoff = covCS.getSnapshotId(snapshotIdDO, int(snapshotGrammar))

            # if we have a snapshot id
            if snapshotIdCutoff:
                RepDebug(3,"Snapshot [%s] -> ID [%d]" % (snapshotGrammar, snapshotIdCutoff))
            else:
                RepError("Unable to determine ID for snapshot [%s]" % snapshotGrammar, exitCodes.INTERNAL_ERROR)

        # we can get the fuller details including its creation date
        snapshotDetailsDismissed = covCS.getSnapshotDetail(snapshotIdCutoff)

        if bool(snapshotDetailsDismissed):
            RepDebug(2, "Dismissal cutoff - snapshot ID [%d] was created at [%s]" % (snapshotIdCutoff, str(snapshotDetailsDismissed[0].dateCreated)))
        else:
            RepError("Failed to get details for dismissal snapshot ID [%d]" % snapshotIdCutoff, exitCodes.INVALID_ARG)


    # if we are only summarising Coverity findings
    if options.mode & modeTypes.SUMMARISE:
        # we are just going to summarise what we find - the less we validate the better to see true errors returned
        RepNote("Summarising Coverity results:-")


    RepMsg('', 'Querying Coverity...')

    # get filtered and merged defects (CIDs) in the named stream for the given Coverity data scope
    allMergedDefectsPageDO = covDS.getMergedDefectsForProjectAndStream(projectNameForStream, options.cstream, options.cscope)

    if covDS.filters:
        filtersApplied = "Filters: %s" % covDS.filters
    else:
        filtersApplied = ""

    # how many [potential] issues to process
    if allMergedDefectsPageDO.totalNumberOfRecords == 0:
        # nothing to process, we are done!
        RepNote("**NO** '%s' issues qualify in stream [%s].   %s" % (dataScopeTypeLabel[1+options.cscope], options.cstream, filtersApplied), 0, 1)

    RepMsg("", "'%s' issues to process %s= [%d]:   %s" % (dataScopeTypeLabel[1+options.cscope], dataScopeTypeCaveat[1+options.cscope], allMergedDefectsPageDO.totalNumberOfRecords, filtersApplied))

    # if we breached the sensible limit and there is no max and we're not summarising
    if validSensible and allMergedDefectsPageDO.totalNumberOfRecords > sensibleValue and not (options.mode & modeTypes.SUMMARISE):
        if not validMax or maxValue > sensibleValue:
            RepError("Exceeded 'sensible' limit [%d] of results to process [%d] - aborting to protect data/integrity" % (sensibleValue, allMergedDefectsPageDO.totalNumberOfRecords), exitCodes.PROC_ERROR)

    recordsToProcess = allMergedDefectsPageDO.totalNumberOfRecords

    if validSkip and skipValue >= recordsToProcess:
        RepError("Skipping [%d] over all results to process [%d] - nothing to do" % (skipValue, allMergedDefectsPageDO.totalNumberOfRecords), exitCodes.SUCCESS_NO_RESULTS)

    if validMax and recordsToProcess > maxValue:
        if validSkip:
            RepNote('Skip first n records = [%d]' % skipValue)
            # first drop the skip records
            recordsToProcess -= skipValue
        RepNote('Max records limit = [%d]' % maxValue)
        if recordsToProcess > maxValue:
            recordsToProcess = maxValue

    # Note: recordsToProcess is only an estimate (max) if post processing is required
    if options.mode & modeTypes.SUMMARISE:
        progressTitle = "Processing"
        ShowProgressBar(progressTitle, 0, recordsToProcess)


    global cntResults, cntValidResults, cntDefects, cntWorkDone, exitCode

    countersCWE = {}
    countersComponent = {}
    countersDefectStatus = {}
    countersClassification = {}
    countersAction = {}
    countersImpact = {}
    countersChecker = {}
    countersKind = {}

    # iterate through these issue results
    for thisMergedDefectDO in allMergedDefectsPageDO.mergedDefects:

        # count each Coverity result for processing
        cntResults += 1

        # may need to post-process the actual Coverity results before we can consider it valid
        if (not validSkip) or (options.cscope == dataScopeType.NEWLY_DISMISSED) or (cntValidResults >= skipValue):
            # get 'list' of detailed information for this individual CID (in the required stream)
            # there is only one defect in the list
            streamDefectDOList = covDS.getStreamDefectsForCID(thisMergedDefectDO.cid, options.cstream)

            if not streamDefectDOList:
                RepWarning("Failed to get defect data for CID [%s] in stream [%s]" % (str(thisMergedDefectDO.cid), options.cstream))
                continue

            streamDefectDO = streamDefectDOList[0]

        covReportComment = ""

        # for newly dismissed results we have to post-process the results dataset
        if options.cscope == dataScopeType.NEWLY_DISMISSED:

            # check this defect for when the required attribute **first** changed state
            # i.e. when was this defect dismissed as Intentional or a False Positive
            foundChange,defectStateDO,valueClassification = covDS.getEventForAttributeChange(streamDefectDO, 1, nameOfClassificationAttribute, "(Intentional|False Positive)")

            # if we didn't find the event - odd, how did it become dismissed? - perhaps a really long time ago (data has been deleted)
            if not foundChange:
                RepWarning("Not sure when CID [%s] was actually dismissed?" % str(thisMergedDefectDO.cid))
                continue

            # found the required attribute event change and it did not occur before our earlier snapshot
            if defectStateDO.dateCreated < snapshotDetailsDismissed[0].dateCreated:
                # this defect is NOT in scope - event was a long time ago and thus since the penultimate snapshot
                RepDebug(2, "CID [%s] was dismissed some time ago [%s] - ignoring" % (str(thisMergedDefectDO.cid), str(defectStateDO.dateCreated)))
                continue

            RepDebug(2, "CID [%s] was dismissed as [%s] on [%s]" % (str(thisMergedDefectDO.cid), valueClassification, str(defectStateDO.dateCreated)))



        # valid results after any post processing
        cntValidResults += 1

        # ignore the first 'n' skip results
        if validSkip:
            if cntValidResults <= skipValue:
                RepDebug(2, "%d CID [%s] - skipping" % (cntResults, str(thisMergedDefectDO.cid)))
                continue
            elif cntValidResults == (1+skipValue):
                RepNote("Skipped first [%d] results" % skipValue)

        # count each one for reporting
        cntDefects += 1

        # show progress if summarising and not logging
        if options.mode & modeTypes.SUMMARISE:
            # simple
            ShowProgressBar(progressTitle, cntResults, recordsToProcess)
        else:
            # show each qualifying CID found
            RepMsg("", "\n%d (%d) CID [%s]" % (cntDefects, cntResults, str(thisMergedDefectDO.cid)))


        # get some data to analyze or dump ...

        # grab the all/first/last report-tagged Comment that was added
        nth = options.cattrmode

        foundReportEvent = False

        # if we have an attribute requirement
        if bool(options.creqattrname):
            # look for (0)=all or the (1)=first/(-1)=last triage event(s) with this
            # named attribute characteristic (and possibly a regex value requirement too)
            # and fetch the one or more associated "Comment" named attribute value(s)
            foundReportEvent, eventDefectStateDO, covReportComment = covDS.getEventForAttributeChange(streamDefectDO, nth,
                                                                                                      options.creqattrname,
                                                                                                      options.creqattrvalue,
                                                                                                      options.cattrname)

        if foundReportEvent:
            RepDebug(1, "[%s]=[%s] triage item occurred on [%s]" % (options.creqattrname, options.creqattrvalue, str(eventDefectStateDO.dateCreated)))
            RepDebug(1, "[%s]-[%s]: [%s]" % (options.creqattrname, options.cattrname, covReportComment))

        # if no custom named attribute events or no associated Comment named attribute - (unlikely)
        else:
            # grab either the last "comment" or all comments as required
            foundComment, eventDefectStateDO, covReportComment = covDS.getEventForAttributeChange(streamDefectDO, nth,
                                                                                                  options.cattrname)
            if foundComment:
                RepDebug(1, "%s-[%s]: [%s]" % (positionLabel[nth+1], options.cattrname, covReportComment))
            else:
                RepDebug(2, "No filled [%s] attributes found??" % options.cattrname)


        # note Bug Tracking System Reference Id value (if one defined)
        btsRefId = covDS.getExtReferenceId(streamDefectDO)

        # not all defects have a cwe
        if hasattr(thisMergedDefectDO, 'cwe'):
            cweValue = "%s" % str(thisMergedDefectDO.cwe)
            cweLabel = "CWE-%s" % cweValue
            cweTag = " (%s)" % cweLabel
        else:
            cweValue = ""
            cweLabel = ""
            cweTag = ""

        # not all defects have a component
        if hasattr(thisMergedDefectDO, 'componentName') and (
                    thisMergedDefectDO.componentName != 'Default.Other'):
            componentValue = thisMergedDefectDO.componentName
            componentTag = " (Comp=%s)" % componentValue
            componentDesc = "\nComponent: '%s'" % componentValue
        else:
            componentValue = ""
            componentTag = ""
            componentDesc = ""

        covClassification = covDS.getClassification(streamDefectDO)

        covAction = covDS.getAction(streamDefectDO)

        covDefectStatus = covDS.getDefectStatus(streamDefectDO)


        # if we are dumping data
        if options.mode & modeTypes.DUMP:
            cntWorkDone += 1

            # build the output record
            outputRecord = "%s,%s,%s,%s" % (
                str(thisMergedDefectDO.cid),
                covDefectStatus,
                thisMergedDefectDO.checkerName,
                covReportComment)

            # output to a file or the screen
            if hOutput:
                hOutput.write(outputRecord + '\n')
            else:
                print outputRecord


        if options.mode & modeTypes.SUMMARISE:
            cntWorkDone += 1
            IncrementCounterForKey(countersCWE, cweValue)
            IncrementCounterForKey(countersComponent, componentValue)
            IncrementCounterForKey(countersDefectStatus, covDefectStatus)
            IncrementCounterForKey(countersClassification, covClassification)
            IncrementCounterForKey(countersAction, covAction)
            IncrementCounterForKey(countersImpact, thisMergedDefectDO.displayImpact)
            IncrementCounterForKey(countersChecker, "%s (%s)" % (thisMergedDefectDO.checkerName, thisMergedDefectDO.displayImpact))
            # translate issue kind into a label
            IncrementCounterForKey(countersKind, covIssueKindLabel[thisMergedDefectDO.issueKind])



        # if we have just hit our max processing limit
        if validMax and cntDefects == maxValue:
            RepWarning("Maximum processing limit of [%d] reached - ABORTING with [%d] remaining to process" % (
            maxValue, (allMergedDefectsPageDO.totalNumberOfRecords - maxValue)))
            break

        # this is the end of our main loop



    # if we are to summarise findings
    if options.mode & modeTypes.SUMMARISE:
        RepMsg("", "\nSUMMARY:-")
        DumpKeys("Kind", countersKind)
        DumpKeys("Defect Status", countersDefectStatus)
        DumpKeys("Classification", countersClassification)
        DumpKeys("Action", countersAction)
        DumpKeys("Impact", countersImpact)
        DumpKeys("Checkers (impact)", countersChecker)
        DumpKeys("Components", countersComponent)
        DumpKeys("CWE", countersCWE)

    # if we wish to see an exit code for when work was done
    if cntWorkDone and options.exitcode is not None:
        exitCode = options.exitcode

    # line feed
    RepMsg()

    # show summary
    if RepDebug(1, "Job Summary %s" % ("- **DRYRUN** " if options.dryrun != 0 else "")):
        RepDebug(1, "  Results   : [%d] %s" % (cntResults,  filtersApplied))
        RepDebug(1, "  Defects   : [%d] - %s" % (cntDefects, dataScopeTypeLabel[1+options.cscope]))
        RepDebug(1, "  Processed : [%d]" % cntWorkDone)
        RepDebug(1, "  Warnings  : [%d]" % cntWarnings)
        RepDebug(1, "  Errors    : [%d]" % cntErrors)

    if options.mode & modeTypes.DUMP:
        if hOutput:
            RepNote('Output was written to: ' + options.output)
            hOutput.close()

    if hLog:
        hLog.close()

    if options.exitcode is not None:
        RepNote("ExitCode = [%d]" % exitCode)

    exit(exitCode)



# - - - - - - - - - - - - - - - - - - - - - - - -
# Global before the main entry is called

# Do argv default this way, as doing it in the functional
# declaration sets it at compile time.
argv = sys.argv

# Parse any config definition - don't accept -h to print help at this stage
confOnlyParser = argparse.ArgumentParser(
    description=__doc__,  # printed with -h/--help
    # Don't mess with format of description
    formatter_class=argparse.RawDescriptionHelpFormatter,
    # Turn off help, so we print all options in response to -h
    add_help=False
)

# these are the only args we're interested in at this stage
# if you want to see debug output as we interpret the config file - set --debug on the command line
confOnlyParser.add_argument("--silent", type=int,
                        help="Suppress screen output",
                        default = None)

confOnlyParser.add_argument("--debug", type=int,
                        help="Debug verbosity",
                        default = None)

confOnlyParser.add_argument("--config",
                        metavar = "FILE",
                        help = "Specify a config file",
                        default = defConfigFile)

# process the args looking only for these two params
(options, remaining_argv) = confOnlyParser.parse_known_args()

# remember the command line arg values as the 2nd parse of args parsing won't see them
argSilent = options.silent
argDebug = options.debug

# global config file
configFile = ConfigParser.ConfigParser()

# if a config file was defined (or we have a default)
if options.config:
    # if this file also exists
    if os.path.exists(options.config):
        # open it and read content
        RepMsg("", 'Reading configuration file [%s]' % options.config)
        configFile.read([options.config])
    else:
        # if not the default value, report error to the user
        if options.config != defConfigFile:
            RepError('Config file [%s] does not exist?' % options.config, exitCodes.INVALID_ARG)

# Need to parse the remainder of anticipated arguments - inherit options from the confOnlyParser
argParser = argparse.ArgumentParser(
    parents=[confOnlyParser]
)

# ---- General  options ----
generalSection = 'general'

# register args and take defaults from config file or hard coded in the system
RegisterStringArg('--log',         generalSection, 'log filename')
RegisterStringArg('--output',      generalSection, 'output filename (when dumping)')
RegisterStringArg('--mode',        generalSection, 'Special mode option (1)-normal (2)-force ticket creation + OTHERS (see Doc)', str(modeTypes.NORMAL))
RegisterIntegerArg('--dryrun',     generalSection, 'dry run option (test Jira actions)',                '0')
RegisterIntegerArg('--exitcode',   generalSection, 'exit code, if work is done')
RegisterIntegerArg('--skip',       generalSection, 'skip the first n results',                         None)
RegisterIntegerArg('--max',        generalSection, 'max limit of results to process',                   None)
RegisterIntegerArg('--sensible',   generalSection, 'sensible max limit of results to potentially process - else error', 200)

# config might also define these (overriding system defaults)
cfgSilent = ConfigSectionString(generalSection, '--silent')
cfgDebug = ConfigSectionString(generalSection, '--debug')


# ---- Coverity options ----
coveritySection = 'coverity'

# register args taking defaults from config file or system
RegisterStringArg('--ctransport',    coveritySection, 'Cov transport to use (http/s)',                    defCoverityTransport)
RegisterStringArg('--chostname',     coveritySection, 'Cov hostname or IP address of Coverity Connect',   defCoverityHostname)
RegisterStringArg('--cport',         coveritySection, 'Cov port number for Coverity Connect',             defCoverityPort)
RegisterStringArg('--cusername',     coveritySection, 'Cov username to perform WS query',                 defCoverityUsername)
RegisterStringArg('--cpassword',     coveritySection, 'Cov password for the specified username',          defCoverityPassword)
RegisterStringArg('--cstream',       coveritySection, 'Cov data stream for accessing')
RegisterStringArg('--csnapshots',    coveritySection, 'Cov snapshot defn ([a],[b]) to compare (optional)')
RegisterIntegerArg('--cscope',       coveritySection, 'Scope of Cov stream data (0-all, 1-newly detected, 2-fixed', '0')
RegisterStringArg('--ccomment',      coveritySection, 'Comment to add into Coverity triage history (when updating Ext Ref Id)', None)

RegisterIntegerArg('--cattrmode',    coveritySection, 'Attr selection type -1=last, 0=all, +1=first)', -1)
RegisterStringArg('--cattrname',     coveritySection, 'Name of triage attribute for which a value is required', "Comment")
RegisterStringArg('--creqattrname',  coveritySection, 'Triage attr requirement - must have a value for this named attribute (regex supported)', None)
RegisterStringArg('--creqattrvalue', coveritySection, 'Triage req value for the named attribute (regex supported)', None)

# triage field filters
RegisterStringArg('--checker',       coveritySection, 'CSV list of required Coverity checker(s) (regex supported)')
RegisterStringArg('--impact',        coveritySection, 'CSV list of required Coverity impact(s) (regex supported)')
RegisterStringArg('--classification',coveritySection, 'CSV list of required Coverity classification(s) (regex supported)')
RegisterStringArg('--kind',          coveritySection, 'CSV list of required Coverity issue kind(s) (regex supported)')
RegisterStringArg('--action',        coveritySection, 'CSV list of required Coverity action value(s) (regex supported)')
RegisterStringArg('--component',     coveritySection, 'CSV list of required Component(s) (Map.Component)')
RegisterStringArg('--cwe',           coveritySection, 'CSV list of required CWE value(s)')
RegisterStringArg('--cid',           coveritySection, 'CSV list of required CID value(s)')
RegisterStringArg('--custom',        coveritySection, 'CSV list of required custom attribute value(s) (name:value)')





# parse the command line arguments - override any noted in a config file or defaults
options = argParser.parse_args(remaining_argv)

# User arg or confg or system value as appropriate
options.silent = AssignNumeric('silent', argSilent, cfgSilent)
options.debug = AssignNumeric('debug', argDebug, cfgDebug)

# mode can be defined as a hex value (for easier addition of bit settings) - command line parser doesn't support this
# so treat as a string and interpret it's integer value here
options.mode = AssignNumeric('mode', options.mode, None)



# - - - - - - - - - - - - - - - - - - - - - - - -
# Now we can call main()
if __name__ == '__main__':
    main()
    if hLog:
        RepMsg("Finished", str(datetime.datetime.now()))

##end