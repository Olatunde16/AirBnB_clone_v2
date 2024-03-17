#!/usr/bin/python3
"""
Fabric script methods:
do_pack: packs web_static/ files into .tgz archive
do_deploy: deploys archive to webservers
deploy: do_packs && do_deploys
"""
from fabric.api import local, env, put, run
from time import strftime
import os.path
env.hosts = ['35.237.202.79', '34.204.185.51']


def do_pack():
    """generate .tgz archive of web_static/ folder"""
    timenow = strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(timenow)
        local("tar -cvzf {} web_static/".format(filename))
        return filename
    except ValueError:
        return None


def do_deploy(archive_path):
    """
    Deploy archive to web server
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}/".format(no_ext)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_no_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_no_ext, path_no_ext))
        run("rm -rf {}web_static".format(path_no_ext))
        run("rm -rf {}".format(symlink))
        run("ln -s {} {}".format(path_no_ext, symlink))
        return True
    except ValueError:
        return False


def deploy():
    archive_path = do_pack()
    if archive_path is None:
        return False
    success = do_deploy(archive_path)
    return success


def do_clean(number=0):
    if number == 0:
        number = 1
    with cd.local('./versions'):
        local("ls -lt | tail -n +{} | rev | cut -f1 -d" " | rev | \
            xargs -d '\n' rm".format(1 + number))
    with cd('/data/web_static/releases/'):
        run("ls -lt | tail -n +{} | rev | cut -f1 -d" " | rev | \
            xargs -d '\n' rm".format(1 + number))
