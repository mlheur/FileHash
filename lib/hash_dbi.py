#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, join as join_path, getsize, getmtime, basename
from site import addsitedir
from socket import gethostname as hostname

addsitedir(dirname(realpath(abspath(argv[0]))))
from dbi_writer import dbi_writer as dbi
from file_hasher import hash


class hash_dbi(dbi):
    """ High level dbi for calls from the application """

    def mk_fqpn_dict(self,fqpn_struct):
        R = {}
        K = ["hn","dn","fn","size","mtime","hash"]
        for i in range(0,len(fqpn_struct)):
            R[K[i]] = fqpn_struct[i]
        return R

    def mk_fqpn_struct_prehash(self, fqpn):
        return [hostname(),
                dirname(fqpn),
                basename(fqpn),
                getsize(fqpn),
                getmtime(fqpn)]
    
    def mk_fqpn_struct(self,fqpn,hash):
        R = self.mk_fqpn_struct_prehash(fqpn)
        R.append(hash)
        return R

    def changed(self,existing,ondisk):
        K = ["size","mtime"]
        for i in range(0,len(K)):
            if existing[i] != ondisk[i]:
                return True
        return False

    def addfile(self, fqpn, rehash=False):
        fqpn_struct = self.mk_fqpn_struct_prehash(fqpn)
        existing = self.select_all_from_fqpn_where_fqpn_is(fqpn_struct[0],fqpn_struct[1],fqpn_struct[2])
        if len(existing) == 0\
        or self.changed(mk_fqpn_dict(existing[0]), mk_fqpn_dict(fqpn_struct)):
            rehash = True
        if rehash:
            fqpn_struct = self.mk_fqpn_struct(fqpn,hash(fqpn))
            if "debug" in self.printargs and self.printargs["debug"] == True:
                print("debug: fqpn_struct={}".format(fqpn_struct))
            self.insert_fqpn(fqpn_struct)

if __name__ == "__main__":
    d = hash_dbi(printargs={"debug":True})
    d.addfile(abspath(realpath(argv[0])))
    print(d.select_all_from_fqpn())
    raise RuntimeError("this is meant to be imported")
