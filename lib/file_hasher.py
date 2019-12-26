#!/usr/bin/env python3

# portable system imports
from sys import argv
from os.path import realpath, abspath, dirname, basename, getsize, getmtime, join as join_path
from site import addsitedir
import hashlib
from socket import gethostname as hostname

# local imports
addsitedir(dirname(realpath(argv[0])))


# exports
def hash(fqpn):
    try:
        h = hashlib.sha256()
        cycles = 0
        with open(fqpn, 'rb') as f:
            while True:
                buf = f.read(8192)
                if cycles > 8192 or not buf:
                    break
                h.update(buf)
                cycles += 1
        return h.hexdigest()
    except OSError as e:
        if e.errno == 22:
            return e.strerror
        raise e


def mklist_dinfo(finfo, hash, size=None, mtime=None):
    if size is None: size = finfo["size"]
    if mtime is None: mtime = finfo["mtime"]
    return [
        size,
        mtime,
        hash,
        finfo["host"],
        finfo["dirname"],
        finfo["basename"]
    ]


def mklist_finfo(finfo):
    return [finfo["host"],
            finfo["dirname"],
            finfo["basename"],
            finfo["size"],
            finfo["mtime"]]


def mkdict_finfo(fqpn, host=None):
    if host is None: host = hostname()
    return {
        "host": host,
        "dirname": dirname(fqpn),
        "basename": basename(fqpn),
        "size": getsize(fqpn),
        "mtime": int(getmtime(fqpn))
    }


def mkdict_dinfo(dinfo):
    return {
        "host": dinfo[0],
        "dirname": dinfo[1],
        "basename": dinfo[2],
        "size": dinfo[3],
        "mtime": dinfo[4],
        "hash": dinfo[5],
        "last_seen": dinfo[6]
    }


def mkstr_fqpn(finfo):
    return "{}".format(join_path(finfo["dirname"], finfo["basename"]))

def mkstr_host_fqpn(finfo):
    return "{}:{}".format(finfo["host"], mkstr_fqpn(finfo))

# main
if __name__ == "__main__":
    fqpn = realpath(abspath(argv[0]))
    print("hash({}) = [{}]".format(fqpn, hash(fqpn)))
    finfo_dict = mkdict_finfo(fqpn)
    print("dict({}) = [{}]".format(fqpn, finfo_dict))
    finfo_list = mklist_finfo(finfo_dict)
    print("list({}) = [{}]".format(fqpn, finfo_list))
    fqpn2 = mkstr_fqpn(finfo_dict)
    print("fqpn({}) = [{}]".format(fqpn, fqpn2))
    fqpn3 = mkstr_host_fqpn(finfo_dict)
    print("host:fqpn({}) = [{}]".format(fqpn, fqpn3))
    dinfo_dict = mkdict_dinfo(["thehostname", "thedirname", "thebasename", "thesize", "themtime", "thehash", "thelast_seen"])
    print("dinfo(thefile) = [{}]".format(dinfo_dict))
    raise RuntimeError("this is meant to be imported")
