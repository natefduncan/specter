import os
from pathlib import Path
import datetime
import json

with open("files.json") as f:
    SAVES = json.load(f)

def get_last_modified(path):
    ts = os.path.getmtime(path)
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def saved_files(files):
    for file in files:
        if file not in SAVES:
            pass

            

        

if __name__=="__main__":
    print(get_last_modified("/Users/User/Documents/Notes/Work/Victor DB.txt"))