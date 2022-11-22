#!/usr/bin/env python

import requests
import json 

# Change this:
base_url = 'https://cov-connect.example.com:443'
base_auth = requests.auth.HTTPBasicAuth('<username>', '<password-or-authkey')
proj_name = "<project-name>"


# No need to change anything below here:
def get_intentional_filter(project_name):
    return {
        "filters": [
            {
                "columnKey": "project",
                "matchMode": "oneOrMoreMatch",
                "matchers": [
                    {
                        "class": "Project",
                        "name": project_name,
                        "type": "nameMatcher"
                    }
                ]
            },
            {
                "columnKey": "classification",
                "matchMode": "oneOrMoreMatch",
                "matchers": [
                    {
                    "key": "Intentional",
                    "type": "keyMatcher"
                    }
                ]
            }
        ],
        "columns": [
            "cid",
            "lastTriageComment",
            "column_custom_Deviation Status"
        ]
    }
    

def find_deviation_attribute(obj):
    for a in obj["attributes"]:
        if a["name"] == "Deviation Status" and a["attributeType"] == "LIST_OF_VALUES":
            for value in a["attributeValues"]:
                if value["name"] == "Comment Missing":
                    return True
    return False

# Check if custom triage attribute "Deviation Status" exists:
def has_deviation_attribute():
    url = base_url + '/api/v2/triageAttributes'
    header = { "Accept": "application/json" }
    response = requests.get(url, auth = base_auth, headers = header)
    #print(json.dumps(response.json(), indent=4))
    attributes = response.json()
    if not find_deviation_attribute(response.json()):
        return False
    else:
        return True

def get_intentional_issues(project_name):
    page_size = 100

    url = base_url + '/api/v2/issues/search'
    header = { "Content-Type": "application/json", "Accept": "application/json" }
    params = { "includeColumnLabels" : "true", "locale": "en_us", "offset": 0, "queryType": "bySnapshot", "rowCount": page_size, "sortOrder": "asc" }
    filter = get_intentional_filter(project_name)
   
    # Initialize loop vars
    items = 0
    issues = []

    # Get first page
    response = requests.post(url, auth = base_auth, headers = header, params = params, data = json.dumps(filter))
    page = response.json()
    #print(page)
    total_items = page['totalRows']

    while items < total_items:
        # Copy issues from current page into issues[]
        for row in page["rows"]:
            issue = {}
            for col in row:
                issue[col['key']] = col['value']
            issues.append(issue)
            items = items + 1
        # Get next page
        params['offset'] = int(items / page_size) * page_size
        response = requests.post(url, auth = base_auth, headers = header, params = params, data = json.dumps(filter))
        page = response.json()

    return issues

def set_deviation_status(issue, status):
    url = base_url + '/api/v2/issues/triage'
    header = { "Content-Type": "application/json", "Accept": "application/json" }
    # TODO: check triage store of stream
    params = { "triageStoreName": "Default Triage Store" }
    filter = { "cids": [ issue['cid'] ], "attributeValuesList": [ { "attributeName": "Deviation Status", "attributeValue": status } ] }
    response = requests.put(url, auth = base_auth, headers = header, params = params, data = json.dumps(filter))
    #print(response.json())

def get_triage_history(cid):
    url = base_url + '/api/v2/issues/triageHistory'
    header = { "Accept": "application/json" }
    # TODO: check triage store of stream
    params = { "cid" : cid, "triageStoreNames": "Default Triage Store" }
    response = requests.get(url, auth = base_auth, headers = header, params = params)
    triage_history = response.json()
    return triage_history["triageHistories"]

# Note: lastTriageComment field is not reliable, as it changes to '' when other
# triage fields are changed in the UI. So we're parsing the history instead.
def get_last_triage_comment(cid):
    hist = get_triage_history(cid)
    for hist_entry in hist:
        for attr_entry in hist_entry["attributeValuesList"]:
            if attr_entry["attributeName"] == "comment" and attr_entry["attributeValue"]:
                last_comment = attr_entry["attributeValue"]
                return last_comment
    return ''
    

# Custom attributed do not seems be to be contained in the issue columns, so we
# search the triage history instead.
"""
def get_deviation_status(cid):
    hist = get_triage_history(cid)
    for hist_entry in hist:
        for attr_entry in hist_entry["attributeValuesList"]:
            if attr_entry["attributeName"] == "Deviation Status":
                last_deviation_status = attr_entry["attributeValue"]
                return last_deviation_status
    return ''
"""

# Main program starts here

# Check if "Deviation Status" attribute exists in Connect
print("Checking for 'Deviation Status' attribute...")

if not has_deviation_attribute():
    print("Error: required attribute \"Deviation Status\" not found.")
    exit(-1)
else:
    print("... ok.")

# Get all intentional issues (aka deviated issues)
print("Reading issues with classification 'Intentional'...")
issues = get_intentional_issues(proj_name)
print("... found " + str(len(issues)) + " issues.")

# Checking last triage comment
for issue in issues:
    cid = issue['cid']
    comment = get_last_triage_comment(cid)
    #print(str(cid) + ": " + comment)
    # TODO: set_deviation_status can be done for mutiple cids at once
    if comment == '' or comment == 'default triage, overridden by manual triage':
        set_deviation_status(issue, "Comment Missing")
        print(str(cid) + " -> " "Comment Missing")
    else:
        set_deviation_status(issue, "Ready for Review")
        print(str(cid) + " -> " "Ready for Review")
    



