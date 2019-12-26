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

    def select_allhashes(self):
        R = []
        for V in self.select("allhashes"):
            R.append(V[0])
        return R

    def select_dinfo_from_hash(self, hash):
        R = []
        for V in self.select("dinfo_from_hash", [hash]):
            R.append(mkdict_dinfo(V))
        return R

    def select_dinfo_from_finfo_as_host_fqpn_size_mtime(self, finfo, q="dinfo_from_finfo_as_host_fqpn_size_mtime", nV=5, sV=0):
        R = self.select(q, mklist_finfo(finfo)[sV:nV])
        if R is None:
            return None
        nR = len(R)
        if nR < 1: return None
        if nR > 1: raise TE("dinfo returned [{}] rows, expected 0 or 1".format(nR))
        return mkdict_dinfo(R[0])

    def select_dinfo_from_host_fqpn(self, host, fqpn):
        finfo = mkdict_finfo(fqpn, host)
        return self.select_dinfo_from_finfo_as_host_fqpn_size_mtime(finfo, "dinfo_from_host_fqpn", 3)


if __name__ == "__main__":
    from socket import gethostname as hostname
    from file_hasher import mkdict_finfo
    from os.path import join as join_path

    fqpn = join_path(dirname(realpath(abspath(argv[0]))), "dbi.py")
    finfo = mkdict_finfo(fqpn)

    hdbi = dbi_reader("test_dbi.db", False)
    allhashes = hdbi.select_allhashes()
    print("select_allhashes: {}".format(allhashes))
    print("select(allall): {}".format(hdbi.select("allall")))
    print("select_dinfo_from_hash: {}".format(hdbi.select_dinfo_from_hash(allhashes[0])))
    print("select_dinfo_from_finfo_as_host_fqpn_size_mtime = [{}]".format(hdbi.select_dinfo_from_finfo_as_host_fqpn_size_mtime, finfo))
    print("select_dinfo_from_host_fqpn: {}".format(hdbi.select_dinfo_from_host_fqpn(hostname(), fqpn)))

    raise RuntimeError("this is meant to be imported")
