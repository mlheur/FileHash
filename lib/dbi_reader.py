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

    def select_all_from_fqpn(self):
        return self.select("all_from_fqpn")

    def select_distinct_hashes(self):
        return self.select("distinct_hashes")

    def select_all_from_fqpn_where_hash_is(self, hash):
        return self.select("from_fqpn_where_hash_is", [hash])

    def select_all_from_fqpn_where_fqpn_is(self, hn, dn, fn):
        return self.select("from_fqpn_where_fqpn_is", [hn,dn,fn])

if __name__ == "__main__":
    from socket import gethostname as hostname
    from file_hasher import mkdict_finfo
    from os.path import join as join_path
    fqpn = join_path(dirname(realpath(abspath(argv[0]))), "dbi.py")
    finfo = mkdict_finfo(fqpn)
    d = dbi_reader({"dbn":"FileHash","user":"FileHash","pass":"dbms","host":"losmuertos"},{})

    print("All from FQPN: {}".format(d.select_all_from_fqpn()));
    print("Distinct Hash: {}".format(d.select_distinct_hashes()));
    print("All from fqpn where hash is 'F00BADCEA052234': {}".format(d.select_all_from_hash('F00BADCEA052234')))
    print("All from fqpn where fqpn is '': {}".format(d.select_all_from_hash('F00BADCEA052234')))

    raise RuntimeError("this is meant to be imported")
