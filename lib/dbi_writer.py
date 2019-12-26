#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, basename
from site import addsitedir

addsitedir(dirname(realpath(abspath(argv[0]))))
from dbi_reader import dbi_reader as dbi
from file_hasher import mklist_dinfo


class dbi_writer(dbi):
    """ wrapped insert functions for dbi """

    def insert_finfo(self, finfo, hash):
        self.insert("finfo", mklist_dinfo(finfo, hash))

if __name__ == "__main__":
    from socket import gethostname as hostname
    from file_hasher import hash, mkdict_finfo

    d = dbi_writer("test_dbi.db", False)
    fqpn = realpath(abspath(argv[0]))
    d.insert_finfo(mkdict_finfo(fqpn), hash(fqpn))
    print("allhashes: {}".format(d.select_allhashes()))
    print("allall: {}".format(d.select("allall")))
    print("dinfo self: {}".format(d.select_dinfo_from_host_fqpn(hostname(), fqpn)))

    raise RuntimeError("this is meant to be imported")
