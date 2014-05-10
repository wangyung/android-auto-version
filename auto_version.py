#!/usr/bin/env python

import os
import sys
import argparse
import subprocess
from xml.dom.minidom import parse

def parse_manifest(manifest_path):
    try:
        dom1 = parse(manifest_path)
    except IOError as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit()

    is_git = is_git_repo(manifest_path)
    version = auto_version(is_git)
    dom1.documentElement.setAttribute("android:versionName", version)
    f = open(manifest_path, "w+")
    f.write(dom1.toxml() )

def auto_version(is_git):
    if is_git:
        sha1 = subprocess.check_output(["git", "log", "-n", "1", "--pretty=one"])
        version = sha1[:6].upper()
    else:
        version = subprocess.check_output(["date", "+%Y%m%d%H%M"])

    return version.strip()

def is_git_repo(manifest_path):

    dirname = os.path.dirname(os.path.realpath(manifest_path))
    while os.path.isdir(dirname):
        files = os.listdir(dirname)
        if ".git" in files:
            return True
        dirname = os.path.dirname(dirname)

    return False

def main():
    parser = argparse.ArgumentParser(description='Auto-version for android apk.')
    parser.add_argument("-m", "--manifest", nargs="?", dest='manifest_path', default="./AndroidManifest.xml", help="The path of AndroidManifest.xml")
    args = parser.parse_args()
    parse_manifest(args.manifest_path)

if __name__ == "__main__":
    main()
