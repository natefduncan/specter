import os
from pathlib import Path
import datetime
import json
import time

from utils import get_all_files

def load_saves():
    with open("saves.json") as f:
        SAVES = json.load(f)
    return SAVES

def get_last_modified(path):
    ts = os.path.getmtime(path)
    dt = datetime.datetime.fromtimestamp(ts)
    return dt

def saved_files(files, SAVES):
    output = []
    for file in files:
        if file not in SAVES["files"]:
            output.append(file)
        else:
            if get_last_modified(file).timestamp() > SAVES["last_saved"]:
                output.append(file)
    return output

def dump_saves(files):
    with open("saves.json", "w") as f:
        json.dump({"last_saved" : datetime.datetime.now().timestamp(), "files" : files}, f)

def save_loop(path, wait=5, trigger_func=None, *args, **kwargs):
    SAVES = load_saves()
    while True: 
        try:
            files = get_all_files(path, ignore=[".DS_Store", "/data", "/.git", "sonic.cfg", ".gitignore", "\\data", "\\.git"])
            saved = saved_files(files, SAVES)
            if len(saved) > 0:
                dump_saves(files)
                if trigger_func:
                    trigger_func(*args, **kwargs)
                SAVES = load_saves()
            time.sleep(wait)
        except KeyboardInterrupt:
            break

if __name__=="__main__":
    def notify(x):
        print(x)
    home_dir = Path(os.path.expanduser('~'))
    save_loop(f"{str(home_dir)}/Documents/Notes", wait=5, trigger_func=notify, x="SAVED")
