#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, basename
from site import addsitedir

addsitedir(dirname(realpath(abspath(argv[0]))))
from dbi_reader import dbi_reader as dbi
from file_hasher import mklist_dinfo


class dbi_writer(dbi):
    """ wrapped insert functions for dbi """

    def insert_hn(self,hn):
        self.insert("hn",[hn])

    def insert_dn(self,dn):
        self.insert("dn",[dn])

    def insert_dh(self,hn,dn,from_scratch=False):
        if from_scratch:
            self.insert_hn(hn)
            self.insert_dn(dn)
        self.insert("dh",[hn,dn])

    def insert_fqpn(self,hn,dn,fn,size,mtime,hash):
        fqdn = hn+":"+dn
        self.insert_dh(hn,dn,True)
        self.insert("fqpn",[fqdn,fqdn,fn,size,mtime,hash])

if __name__ == "__main__":
    from socket import gethostname as hostname
    from file_hasher import hash, mkdict_finfo

    d = dbi_writer({"dbn":"FileHash","user":"FileHash","pass":"dbms","host":"losmuertos"},{})
    fqpn = realpath(abspath(argv[0]))
    d.insert_hn(hostname())
    d.insert_dn(dirname(fqpn))
    d.insert_dh(hostname(),dirname(fqpn))

    d.insert_dh("thefakehost","/foo/bin",True)
    print(d.select("all_from_fqdn"))

    d.printargs["debug"] = True
    d.printargs["verbose"] = True
    d.printargs["quiet"] = False

    d.insert_fqpn(
       hostname()
       ,dirname(fqpn)
       ,basename(fqpn)
       ,123
       ,1543287692
       ,"F00BADCEA052234"
    )
    print(d.select("all_from_fqpn"))

    raise RuntimeError("this is meant to be imported")
