import os.path
import sys
import time
import subprocess
import webbrowser

from shutil import copyfile
from simple_analyzer import * 
from simple_feedback import * 

if __name__ == '__main__':
    copyfile("template.html", "feedback.html")
    pserver = subprocess.Popen(["python", "simple_server.py", "&"])
    time.sleep(1)
    webbrowser.open("http://localhost:8080/")
    dataset_number = 0

    lp = SimpleAnalyzer()
    k = 0
    cmd = ["adb", "logcat"]
    try: 
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=True)
        while True:
            line = proc.stdout.readline()
            if line.strip() != "":
                result = lp.parse_line(line)
                if result.strip() != "":
                    print result
                else:
                    pass

                # if any returned number, the server got shut down and we can stop this program
                if pserver.poll() is not None:
                    sys.exit()

                # produce simple feedback file
                sf = SimpleFeedback(lp.return_list(), lp.return_error(), "template.html", "fbtmp.html")
                previous_dataset_number = dataset_number
                if not os.path.isfile("fbtmp.html"):
                    dataset_number = sf.return_new_feedback(False, previous_dataset_number)
                k = k + 1

    except KeyboardInterrupt:
       sys.stdout.flush()
       pass 
