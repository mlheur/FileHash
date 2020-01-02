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
        K = ["hn","dn","fn","size","mtime","hash","fqdn","fqpn"]
        for i in range(0,len(fqpn_struct)):
            if i>=len(fqpn_struct) or i>=len(K):
               break
            R[K[i]] = fqpn_struct[i]
        return R

    def mk_fqpn_struct_prehash(self, fqpn):
        return [hostname(),
                dirname(fqpn),
                basename(fqpn),
                getsize(fqpn),
                int(getmtime(fqpn))]
    
    def mk_fqpn_struct(self,fqpn,hash):
        R = self.mk_fqpn_struct_prehash(fqpn)
        R.append(hash)
        return R

    def changed(self,existing,ondisk):
        K = ["size","mtime"]
        for i in range(0,len(K)):
            if existing[K[i]] != ondisk[K[i]]:
                return True
        return False

    def addfile(self, fqpn, rehash=False):
        fqpn_struct = self.mk_fqpn_struct_prehash(fqpn)
        existing = self.select_all_from_fqpn_where_fqpn_is(fqpn_struct[0],fqpn_struct[1],fqpn_struct[2])
        if len(existing) == 0\
        or self.changed(self.mk_fqpn_dict(existing[0]), self.mk_fqpn_dict(fqpn_struct)):
            rehash = True
        if rehash:
            fqpn_struct = self.mk_fqpn_struct(fqpn,hash(fqpn))
            if "debug" in self.printargs and self.printargs["debug"] == True:
                print("debug: fqpn_struct={}".format(fqpn_struct))
            self.insert_fqpn(fqpn_struct)

    def mk_dict_hash_fqpn_list(self):
        table = {}

        for row in self.select_all_from_fqpn():
            fd = self.mk_fqpn_dict(row)
            if not fd["hash"] in table:
                table[fd["hash"]] = []
            table[fd["hash"]].append(fd)

        if "debug" in self.printargs and self.printargs["debug"] == True:
            print("debug: returning table {}".format(table))

        return table

    def report(self,opts=None):
        if opts is None or len(opts) == 0:
            opts = "0","1","+"
        for [hash, fqpn_dict_list] in self.mk_dict_hash_fqpn_list().items():
            if len(fqpn_dict_list) < 1:
                if "0" in opts:
                    print("ERROR: Orphaned Hash: {}".format(hash))
            elif len(fqpn_dict_list) > 1:
                if "+" in opts:
                    print("Duplicated Hash: {}".format(hash))
                    for f in fqpn_dict_list:
                        print(" ... {} {} {}".format(f["mtime"],f["size"],f["fqpn"]))
            else:
                if "1" in opts:
                    print("Unique hash: {} {}".format(fqpn_dict_list[0]["hash"], fqpn_dict_list[0]["fqpn"]))
        return self

if __name__ == "__main__":
    d = hash_dbi(printargs={"debug":True,"verbose":True,"quiet":False})
    d.addfile(abspath(realpath(argv[0])))
    print(d.select_all_from_fqpn())
    d.report()
    raise RuntimeError("this is meant to be imported")
