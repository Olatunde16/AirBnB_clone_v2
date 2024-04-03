#!/usr/bin/python3
"""
Fabric script methods:
do_pack: packs web_static/ files into .tgz archive
do_deploy: deploys archive to webservers
deploy: do_packs && do_deploys
"""
from fabric.api import *
from time import strftime
import os.path

env.hosts = ['<100.25.17.119>', '54.88.101.99']
env.users = '<ubuntu>'
env.key_filename = '<~/.ssh/school>'


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
