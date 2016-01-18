import sys
import json
import base64
import codecs
import urllib3
import requests
import requests.packages.urllib3


requests.packages.urllib3.disable_warnings()

bugid = 540000
while True:
    # Check bugzilla for logcat using restful requests
    url = "https://bugzilla.mozilla.org/rest/bug/" + str(bugid) + "/attachment"
    response = requests.get(url)
    result = json.loads(response.text)

    files = []
    # If it does has attachments, try to check if it matches the criteria
    if 'code' in result:
        print bugid
        bugid += 1
        continue
    if len(result['bugs'][str(bugid)]) > 0:
        for item in result['bugs'][str(bugid)]:
           if (   "logcat" in item['description'] or "log cat" in item['description']
               or "logcat" in item['file_name'] or "log cat" in item['file_name']     ):
               files.append(item['data'])

    # Setting the system encoding to utf8 so that we can decode the data correctly
    reload(sys)
    sys.setdefaultencoding('utf8')

    # decode the data and output to files
    count = 0
    for item in files:
       f = codecs.open(str(bugid) + "_" + str(count) + ".txt", "w+", "utf-8")
       f.write(base64.b64decode(item.strip()))
       f.close()
       count += 1

    if count > 0:
        print str(bugid) + " has logcat" + str(count) + "attachment(s).\n"
    else:
        print bugid

    bugid += 1 
