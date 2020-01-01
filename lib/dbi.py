#!/usr/bin/env python3

from sys import argv
from os import unlink
from os.path import abspath, realpath, dirname, basename
from mysql import connector as dbms
from time import sleep, time as now
from site import addsitedir

addsitedir(dirname(realpath(argv[0])))
from SQL import SQL
from mycnf import mycnf

class TransactionError(Exception):
    def __init__(self, arg):
        Exception(self, arg)


class dbi(object):
    """ Interface to store and retrieve file hash info.  """

    def __init__(self, dbargs=None, printargs={"verbose":False,"debug":False,"quiet":True}):
        """ Instantiate an interface with a particular data base. """
        self.printargs = printargs
        self.dbargs = dbargs
        if dbargs is None:
           self.dbargs = mycnf().__dict__
        self.conn = None
        self.attached = False
        self.conn = None
        self.attach(self.dbargs)

    def attach(self, dbargs=None):
        self.attached = False
        if dbargs is None:
            dbargs = self.dbargs

        if "verbose" in self.printargs.keys() and self.printargs["verbose"]:
            print("Calling attach with dbargs {}".format(dbargs))

        if "keepalive" in dbargs and not dbargs["keepalive"]:
            self.close()
        try:
            d = dbargs["database"]
            u = dbargs["user"]
            p = dbargs["password"]
            h = dbargs["host"]
            if "debug" in self.printargs and self.printargs["debug"]: print("d:{} u:{} p:{} h:{}".format(d,u,p,h))
            self.conn = dbms.connect(database=d
                                    ,user=u
                                    ,password=p
                                    ,host=h
                                    )
        except dbms.errors.ProgrammingError as pe:
            raise pe
        except Exception as e:
            print(e)
            self.close()
            raise RuntimeError("Unable to connect to the database")
        self.c = self.conn.cursor()
        stmt_use = "USE `{}`;".format(dbargs["database"])
        if "debug" in self.printargs and self.printargs["debug"]:
            print("got cursor {}, executing {}".format(self.c,stmt_use))
        self.c.execute(stmt_use)
        self.attached = True
        return self

    def show(self):
        print("{}".format(self))

    def __str__(self):
        return "database=[{}] conn=[{}] c=[{}]".format(self.dbargs["database"], self.conn, self.c)

    def close(self):
        if self.conn is None: return self
        self.conn.close()
        self.conn = None
        return self

    def q(self, stmt, vals=None, call="Q"):
        if self.attached and (stmt is not None and stmt != ""):
            if "verbose" in self.printargs and self.printargs["verbose"]:
                print("{}:[{}]\nV:[{}]".format(call, stmt, vals))
            try:
                if vals is not None:
                    self.c.execute(stmt, vals)
                else:
                    self.c.execute(stmt)
            except Exception as e:
                if "verbose" in self.printargs and self.printargs["verbose"]:
                    print("sql error {}".format(e))
                return None
            try:
                return self.c.fetchall()
            except dbms.errors.InterfaceError as ie:
                return []
            except Exception as e:
                raise e

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
        if "verbose" in self.printargs and self.printargs["verbose"]:
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

if __name__ == "__main__":
    d = dbi(printargs={"quiet": False, "verbose": True, "debug": True})
    f = realpath(abspath(argv[0]))
    from socket import gethostname as hostname
    from file_hasher import hash

    h = hash(f)
    d.insert("hn",[hostname()])
    hid = d.select("hid_from_hn",[hostname()])[0][0]
    d.insert("dn",[dirname(f)])
    did = d.select("did_from_dn",[dirname(f)])[0][0]
    d.insert("dh",[hostname(),dirname(f)])
    fqdn = d.select("fqdn_from_fqdn_where_hn_dn",[hostname(),dirname(f)])[0][0]
    d.insert("fqpn",[fqdn,fqdn,basename(f),321,18726423,"ABCD18742391"])
    d.select("all_from_fqpn")

    raise RuntimeError("this is meant to be imported")
