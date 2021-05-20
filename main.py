import os
from specter.monitor import DirLoop
from pathlib import Path
from specter.git import push, pull, commit, get_repo
from specter.utils import get_all_files
from specter.monitor import dump_saves
import sys

def specter_push(notes_path):
    files = get_all_files(notes_path, ignore=[".DS_Store", "/data", "/.git", "sonic.cfg", "\\.git", "\\data"])
    repo = get_repo(notes_path)
    commit(repo, files)
    push(repo)
    print("Pushing specter changes")

def specter_pull(notes_path): 
    repo = get_repo(notes_path)
    pull(repo)
    print("Pulling specter changes")

from specter.ssh import add_key

if __name__=="__main__":
    relative_notes_path = sys.argv[1]
    home_dir = Path(os.path.expanduser('~'))
    notes_path = str(Path(f"{str(home_dir)}/{relative_notes_path}"))

    def notify(x):
        print(x)

    home_dir = Path(os.path.expanduser('~'))
    dir_path = f"{str(home_dir)}/Documents/Notes"

    l = DirLoop(path=notes_path)
    l.set_save_func(specter_push, notes_path)
    l.set_open_func(notify, "OPEN")
    l.start()