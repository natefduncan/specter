import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

HOST=os.getenv("HOST")
REPO=os.getenv("REPO")
SUPERUSER=os.getenv("SUPERUSER")
SUPERUSER_PASSWORD=os.getenv("SUPERUSER_PASSWORD")
USERNAME=os.getenv("USERNAME")
PASSWORD=os.getenv("PASSWORD")

from fabric import Connection

def get_id_rsa():
    home_dir = Path(os.path.expanduser('~'))
    id_rsa_path = home_dir / ".ssh" / "id_rsa.pub"
    with open(id_rsa_path) as f:
        content = f.read()
    return content

def run_user_setup():
    ssh_pub_file = get_id_rsa()
    command = f"""
    #Create user
    useradd -m -G sudo,www-data {USERNAME} &&\\ \n\
    echo -e \"{PASSWORD}\\n{PASSWORD}\\n\" | passwd {USERNAME} \n\
    chsh -s /bin/bash {USERNAME} \n\
    #Create SSH directory \n\
    mkdir /home/{USERNAME}/.ssh \n\
    cd /home/{USERNAME}/.ssh \n\
    #Copy over public key \n\
    touch authorized_keys \n\
    echo \"{ssh_pub_file}\" > authorized_keys \n\
    #Set SSH key permissions \n\
    chmod 700 /home/{USERNAME}/.ssh \n\
    #Change file/folder ownership to new user \n\
    chown -R {USERNAME}:{USERNAME} /home/{USERNAME} \n\
    exit
    """

    result = Connection(f'{SUPERUSER}:{SUPERUSER_PASSWORD}@{HOST}').run(command, hide=True)
    msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    return msg.format(result)

if __name__=="__main__":
    get_id_rsa()