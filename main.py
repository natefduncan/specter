import os
from specter.monitor import DirLoop
from pathlib import Path
from specter.git import push, pull, commit, get_repo
from specter.utils import get_all_files
import sys

def specter_push(notes_path):
    files = get_all_files(notes_path, ignore=[".DS_Store", "/data", "/.git", "sonic.cfg", "\\.git", "\\data"])
    repo = get_repo(notes_path)
    print(files)
    commit(repo, files)
    push(repo)
    print("Pushing specter changes")

def specter_pull(notes_path): 
    repo = get_repo(notes_path)
    pull(repo)
    print("Pulling specter changes")

if __name__=="__main__":
    relative_notes_path = sys.argv[1]
    home_dir = Path(os.path.expanduser('~'))
    notes_path = str(Path(f"{str(home_dir)}/{relative_notes_path}"))

    l = DirLoop(path=notes_path)
    l.set_save_func(specter_push, notes_path)
    l.set_open_func(specter_pull, notes_path)
    l.start()
