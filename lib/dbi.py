#!/usr/bin/env python3

from sys import argv
from os import unlink
from os.path import abspath, realpath, dirname, basename
from site import addsitedir
from fcntl import flock, LOCK_EX, LOCK_UN

addsitedir(dirname(realpath(argv[0])))
import sqlite3
from SQL import SQL
from time import sleep, time as now


class TransactionError(Exception):
    def __init__(self, arg):
        Exception(self, arg)


class dbi(object):
    """ Interface to store and retrieve file hash info.  """

    def __init__(self, dbn, verbose=False, quiet=False):
        """ Instantiate an interface with a particular data base. """
        self.verbose = verbose
        self.quiet = quiet
        self.attached = False
        self.dbn = dbn
        self.conn = None
        self.attach(dbn);

    def attach(self, dbn, keepalive=False):
        if not keepalive: self.close()
        try:
            self.conn = sqlite3.connect(dbn)
        except error as e:
            print(e)
            self.close()
            return
        self.c = self.conn.cursor()
        if self.c.execute(SQL.ATTACH.format(dbn)):
            self.attached = True
        return self

    def show(self):
        print("{}".format(self))

    def __str__(self):
        return "dbn=[{}] conn=[{}] c=[{}]".format(self.dbn, self.conn, self.c)

    def close(self):
        if self.conn is None: return
        self.conn.close()
        self.conn = None
        return self

    def q(self, stmt, vals=None, call="Q"):
        if self.attached and (stmt is not None and stmt != ""):
            if self.verbose:
                print("{}:[{}]\nV:[{}]".format(call, stmt, vals))
            try:
                if vals is not None:
                    self.c.execute(stmt, vals)
                else:
                    self.c.execute(stmt)
            except Exception as e:
                if self.verbose:
                    print("sql error {}".format(e))
                return None
            return self.c.fetchall()

    def lock(self):
        self._lck = open("dbi.lock", "w")
        flock(self._lck, LOCK_EX)

    def unlock(self):
        flock(self._lck, LOCK_UN)

    def dowrite(self, act, key, vals):
        call = act[0]
        stmt = getattr(SQL, act)[key]
        if self.q(stmt, vals, call) is None:
            return None
        self.conn.commit()
        return self

    def insert(self, key, vals):
        return self.dowrite("INSERT", key, vals)

    def update(self, key, vals):
        return self.dowrite("UPDATE", key, vals)

    def delete(self, key, vals):
        return self.dowrite("DELETE", key, vals)

    def select(self, key, vals=None):
        R = self.q(SQL.SELECT[key], vals, "S")
        if self.verbose:
            print("R:[{}]".format(R))
        if R is None:
            return []
        return R

    def drop(self, table):
        self.q(SQL.DROP[table])
        return self

    def create(self, table):
        self.q(SQL.CREATE[table])
        return self

    def createdb(self, dbn=None):
        if dbn is None: dbn = self.dbn
        self.close().attach(dbn)
        for table in SQL.TABLES:
            self.drop(table).create(table)
        return self


if __name__ == "__main__":
    d = dbi("test_dbi.db", True).createdb()
    f = realpath(abspath(argv[0]))
    from socket import gethostname as hostname
    from file_hasher import hash, mkdict_finfo, mklist_dinfo

    h = hash(f)
    finfo = mkdict_finfo(f)
    d = d.insert("finfo", mklist_dinfo(finfo, "0" * 64, 0, 0))
    print("allhashes: {}".format(d.select("allhashes")))
    d = d.update("finfo", mklist_dinfo(finfo, h))
    print("dinfo: {}".format(d.select("dinfo_from_host_fqpn", [hostname(), dirname(f), basename(f)])))

    raise RuntimeError("this is meant to be imported")
