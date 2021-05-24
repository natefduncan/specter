import os
from specter.monitor import DirLoop
from pathlib import Path
from specter.git import push as git_push, pull as git_push, commit, get_repo
from specter.utils import get_all_files
from specter.monitor import dump_saves
import sys
import click

@click.group()
def cli():
    pass

@click.group()
def init():
    HOST = input("Type in server IP: ")
    REPO = input("Type in the repository name (main.git): ")
    LOCATION = input("Type in notes folder location relative to home (/Documents/Notes): ")

@click.command()
@click.argument("notes_path", help="file path to notes repository")
def push(notes_path):
    files = get_all_files(notes_path, ignore=[".DS_Store", "/data", "/.git", "sonic.cfg", "\\.git", "\\data"])
    repo = get_repo(notes_path)
    commit(repo, files)
    git_push(repo)
    click.echo('Pushing specter changes')

@click.command()
@click.argmuent("notes_path", help="file path to notes repository")
def pull(notes_path):
    repo = get_repo(notes_path)
    pull(repo)
    click.echo('Pulling specter changes')

@click.command()
@click.argmuent("notes_path", help="file path to notes repository")
def listen(notes_path):
    home_dir = Path(os.path.expanduser('~'))
    notes_path = str(Path(f"{str(home_dir)}/{notes_path}"))

    def notify(x):
        print(x)

    home_dir = Path(os.path.expanduser('~'))
    dir_path = f"{str(home_dir)}/Documents/Notes"

    l = DirLoop(path=notes_path)
    l.set_save_func(git_push, notes_path)
    l.set_open_func(notify, "OPEN")
    l.start()

cli.add_command(push)
cli.add_command(pull)
cli.add_command(listen)