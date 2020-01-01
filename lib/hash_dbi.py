#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, join as join_path, getsize, getmtime
from site import addsitedir
from socket import gethostname as hostname

addsitedir(dirname(realpath(abspath(argv[0]))))
from dbi_writer import dbi_writer as dbi
from file_hasher import hash


class hash_dbi(dbi):
    """ High level dbi for calls from the application """

    def mk_fqpn_struct(self, fqpn):
        return [
            hostname(),
            dirname(fqpn),
            basename(fqpn),
            getsize(fqpn),
            getmtime(fqpn),
            ]

    def addfile(self, fqpn, rehash=False):
        existing = self.select_from_fqpn_where_fqpn_is(fqpn)
        fqpn_struct = self.mk_fqpn_struct(fqpn)
        if rehash or len(fqpn_struc:
            fqpn_struct[5] = hash(fqpn)
        
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

    raise RuntimeError("this is meant to be imported")
