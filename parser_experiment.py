import sys

error_keys   = ["error", "fail", "crash", "exception", "kill", "fault", r"^E/", "die"]
warning_keys = ["warn", "bad", "refuse", "miss", " not ", 
                " no ", "invalid", "ignore", "undefined", "unsuccess",
                "unauthor", "unable", "skip", "cannot", "unknown"]

for line in sys.stdin:
    lowercase_line = line.lower()
    for k in error_keys:
        if k in lowercase_line:
            print "  ERROR:\t" + line.strip()
            break
    for k in warning_keys:
        if k in lowercase_line:
            print "WARNING:\t" + line.strip()
            break
