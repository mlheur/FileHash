#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, basename
from site import addsitedir

addsitedir(dirname(realpath(abspath(argv[0]))))
from dbi import dbi as dbi
from dbi import TransactionError as TE

class dbi_reader(dbi):
    """ wrapped select fuctions for dbi """

    def select_all_from_fqpn(self):
        return self.select("all_from_fqpn")

    def select_distinct_hashes(self):
        return self.select("distinct_hashes")

    def select_all_from_fqpn_where_hash_is(self, hash):
        return self.select("all_from_fqpn_where_hash_is", [hash])

    def select_all_from_fqpn_where_fqpn_is(self, hn, dn, fn):
        return self.select("all_from_fqpn_where_fqpn_is", [hn,dn,fn])

if __name__ == "__main__":
    from socket import gethostname as hostname
    from os.path import join as join_path
    from file_sifter import file_sifter as sifter
    fqpn = join_path(dirname(realpath(abspath(argv[0]))), "dbi.py")
    d = dbi_reader(sifter(),printargs={"quiet": False, "verbose": True, "debug": True})

    print("All from FQPN: {}".format(d.select_all_from_fqpn()));
    print("Distinct Hash: {}".format(d.select_distinct_hashes()));
    print("All from fqpn where hash is 'F00BADCEA052234': {}".format(d.select_all_from_fqpn_where_hash_is('F00BADCEA052234')))
    print("All from fqpn where fqpn is [{}, {}, {}]: {}".format(hostname(),dirname(fqpn),basename(fqpn),d.select_all_from_fqpn_where_fqpn_is(hostname(),dirname(fqpn),basename(fqpn))))

    raise RuntimeError("this is meant to be imported")
