# This is to fetch logcat from bugzilla (Mozilla)
# Simply run it and it will get logcat from bug 600000
# Otherwise, use "python (this file) (starting number)" to fetch files

import sys
import json
import base64
import codecs
import cleaner
import urllib3
import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

# major part of bugzilla logcat fetcher
def fetcher(bugid):
    at_most = 100000
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
        temp = []
        for item in files:
           data = base64.b64decode(item.strip())
           temp.append(data)
           if not (data in temp):
               f = codecs.open(str(bugid) + "_" + str(count) + ".txt", "w+", "utf-8")
               f.write(data)
               f.close()
               count += 1

        if count > 0:
            print str(bugid) + " has logcat" + str(count) + "attachment(s).\n"
        else:
            print bugid

        bugid += 1
        at_most -= 1
        if at_most <= 0:
            break

if __name__ == '__main__':
    bugid = 600000
    if len(sys.argv) >= 2:
        bugid = int(sys.argv[len(sys.argv)-1])

    fetcher(bugid)
    cleaner.remove_empties(os.getcwd())
    cleaner.remove_duplicates(os.getcwd())
