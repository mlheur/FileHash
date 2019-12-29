#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, basename
from site import addsitedir

addsitedir(dirname(realpath(abspath(argv[0]))))
from dbi import dbi as dbi
from dbi import TransactionError as TE
from file_hasher import mklist_finfo, mkdict_finfo, mkdict_dinfo


class dbi_reader(dbi):
    """ wrapped select fuctions for dbi """

    def select_hid_from_hn(self, hn):
        R = None
        for V in self.select("hid_from_hn", [hn]):
            R = V[0]
        return R

if __name__ == "__main__":
    from socket import gethostname as hostname
    from file_hasher import mkdict_finfo
    from os.path import join as join_path
    fqpn = join_path(dirname(realpath(abspath(argv[0]))), "dbi.py")
    finfo = mkdict_finfo(fqpn)
    hdbi = dbi_reader("test_dbi.db", False)

    print("{}".format(hdbi.select_hid_from_hn(hostname())));

    raise RuntimeError("this is meant to be imported")
