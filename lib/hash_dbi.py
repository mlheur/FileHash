#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, join as join_path
from site import addsitedir

addsitedir(dirname(realpath(abspath(argv[0]))))
from dbi_writer import dbi_writer as dbi
from file_hasher import hash, mkdict_finfo, mkstr_host_fqpn


class hash_dbi(dbi):
    """ High level dbi for calls from the application """

    def mkdict_hash_flist(self):
        table = {}
        for hash in self.select_distinct_hashes():
            table[hash] = self.select_all_from_hash(hash)
        return table

    def report(self, opts=None):
        if opts is None or len(opts) < 1:
            opts = ["0", "1", "+"]
        for hash, flist in self.mkdict_hash_flist().items():
            if len(flist) < 1:
                if "0" in opts:
                    print("ERROR: Orphaned Hash: {}".format(hash))
            elif len(flist) > 1:
                if "+" in opts:
                    print("Duplicated Hash: {}".format(hash))
                    for f in flist:
                        print(" ... {}".format(mkstr_host_fqpn(f)))
            else:
                if "1" in opts:
                    print("Unique hash: {} {}".format(hash, mkstr_host_fqpn(flist[0])))
        return self

    def addfile(self, fqpn, rehash=False):
        finfo = mkdict_finfo(fqpn)
        existing = None
        if not rehash:
            existing = self.select_dinfo_from_finfo_as_host_fqpn_size_mtime(mkdict_finfo(fqpn))
        if existing is None:
            self.lock()
            existing = self.select_dinfo_from_finfo_as_host_fqpn_size_mtime(mkdict_finfo(fqpn))
            if existing is None:
                hashed = 0
                if finfo["size"] > 0:
                    hashed = hash(fqpn)
                self.insert_finfo(finfo, hashed)
                if not self.quiet:
                    print("+> {}".format(mkstr_host_fqpn(finfo)))
                self.unlock()
        if (existing is not None) and (not self.quiet):
            print("=> {}".format(mkstr_host_fqpn(existing)))
        return self


if __name__ == "__main__":
    from time import sleep

    fqpn = join_path(dirname(realpath(abspath(argv[0]))), "dbi.py")
    hdbi = hash_dbi("test_hash_dbi.db", True)
    print("\n\n##### createdb\n")
    hdbi.createdb()
    print("\n\n##### addfile new\n")
    hdbi.addfile(fqpn)
    print("\n\n##### report\n")
    hdbi.report()
    print("\n\n##### addfile existing, sleep\n")
    sleep(5)
    hdbi.addfile(fqpn)
    print("\n\n##### report\n")
    hdbi.report()
    print("\n\n##### done\n")
    raise RuntimeError("this is meant to be imported")
