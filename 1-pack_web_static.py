#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder of
AirBnB Clone repo, using the function do_pack
"""
from fabric.api import local
from time import strftime


def do_pack():
    """generaate a .tgz archive"""
    timenow = strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        archname = "versions/web_static_{}.tgz".format(timenow)
        local("tar -cvzf {} web_static/".format(archname))
        return archname
    except:
        return None
