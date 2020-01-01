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


# main
if __name__ == "__main__":
    raise RuntimeError("this is meant to be imported")
