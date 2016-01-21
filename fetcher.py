import os
import md5
import sys
import json
import base64
import codecs
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
            break;

# remove all empty files
def remove_empties(dir):
    target_size = 0
    for dirpath, dirs, files in os.walk(dir):
        for file in files: 
            path = os.path.join(dirpath, file)
            if os.stat(path).st_size == target_size:
                os.remove(path)
                print "Empty File: " + path + " removed."

# remove duplicate files
def remove_duplicates(dir):
    unique = []
    for filename in os.listdir(dir):
        if os.path.isdir(filename):
            continue
        if os.path.isfile(filename):
            filehash = md5.md5(file(filename).read()).hexdigest()
        if filehash not in unique: 
            unique.append(filehash)
        else: 
            os.remove(filename)
            print "Duplicated File: " + filename + " removed."

if __name__ == '__main__':
    bugid = 600000
    if len(sys.argv) >= 2:
        bugid = int(sys.argv[len(sys.argv)-1])

    fetcher(bugid)
    remove_empties(os.getcwd())
    remove_duplicates(os.getcwd())
