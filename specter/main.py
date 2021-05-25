import os
from specter.monitor import DirLoop
from pathlib import Path
from specter.git import push as git_push, pull as git_pull, commit, get_repo
from specter.utils import get_all_files, relative_to_absolute, get_notes_path, load_saves
from specter.monitor import dump_saves
import sys
import datetime
import click
import json

@click.group()
def cli():
    pass

@click.command()
def init():
    host = input("Type in server IP: ")
    repo = input("Type in the repository name (main.git): ")
    location = input("Type in notes folder location relative to home (Documents/Notes): ")
    SAVES = load_saves()
    SAVES["host"] = host
    SAVES["repo"] = repo
    SAVES["location"] = location
    SAVES["last_checked"] = datetime.datetime.now().timestamp()
    SAVES["files"] = []
    with open("data.json", "w") as f:
        json.dump(SAVES, f)

@click.command()
def push():
    notes_path = get_notes_path()
    files = get_all_files(notes_path, ignore=[".DS_Store", "/data", "/.git", "sonic.cfg", "\\.git", "\\data"])
    repo = get_repo(notes_path)
    commit(repo, files)
    git_push(repo)
    click.echo('Pushing specter changes')

@click.command()
def pull():
    notes_path = get_notes_path()
    repo = get_repo(notes_path)
    git_pull(repo)
    click.echo('Pulling specter changes')

@click.command()
def listen():
    notes_path = get_notes_path()

    def notify(x):
        print(x)

    l = DirLoop(path=notes_path)
    repo = get_repo(notes_path)
    l.set_save_func(git_push, repo)
    l.set_open_func(notify, "OPEN")
    l.start()

cli.add_command(init)
cli.add_command(push)
cli.add_command(pull)
cli.add_command(listen)