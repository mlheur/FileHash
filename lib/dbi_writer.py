#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, basename
from site import addsitedir

addsitedir(dirname(realpath(abspath(argv[0]))))
from dbi_reader import dbi_reader as dbi


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

    def insert_fqpn(self,hn,dn=None,fn=None,size=None,mtime=None,hash=None):
        if "debug" in self.printargs and self.printargs["debug"] == True:
            print("debug: hn={} dn={}".format(hn,dn))
        if type(hn) == type([]):
           hash = hn[5]
           mtime = hn[4]
           size = hn[3]
           fn = hn[2]
           dn = hn[1]
           hn = hn[0]
        if dn is None:
           raise RuntimeError("required positional argument(2) dn is missing")
        fqdn = hn+":"+dn
        self.insert_dh(hn,dn,True)
        self.insert("fqpn",[fqdn,fqdn,fn,size,mtime,hash])

if __name__ == "__main__":
    from socket import gethostname as hostname

    d = dbi_writer()
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
