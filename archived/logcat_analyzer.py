import sys
import time
import subprocess
import webbrowser

from shutil import copyfile
from simple_analyzer import * 
from simple_feedback import * 

if __name__ == '__main__':
    copyfile("template.html", "feedback.html")
    p = subprocess.Popen(["python", "simple_server.py"])
    time.sleep(1)
    webbrowser.open("http://localhost:8080/")

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

                sf = SimpleFeedback(lp.return_list(), lp.return_error(), "template.html", "fbtmp.html")
                sf.generate_feedback_form(False)
                k = k + 1
                copyfile("fbtmp.html", "feedback.html")
    except KeyboardInterrupt:
       sys.stdout.flush()
       pass 
