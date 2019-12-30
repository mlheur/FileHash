#!/usr/bin/env python3

from sys import argv
from os import unlink
from os.path import abspath, realpath, dirname, basename
from mysql import connector as dbms
from site import addsitedir
from fcntl import flock, LOCK_EX, LOCK_UN

addsitedir(dirname(realpath(argv[0])))
from SQL import SQL
from time import sleep, time as now

class TransactionError(Exception):
    def __init__(self, arg):
        Exception(self, arg)


class dbi(object):
    """ Interface to store and retrieve file hash info.  """

    def __init__(self, dbargs, printargs):
        """ Instantiate an interface with a particular data base. """
        self.printargs = printargs
        self.dbargs = dbargs
        self.conn = None
        self.attached = False
        self.conn = None
        self.attach(self.dbargs)

    def attach(self, dbargs={}):
        if len(dbargs) == 0:
            dbargs = self.dbargs

        if self.printargs["verbose"]:
            print("Calling attach with dbargs {}".format(dbargs))

        if not dbargs["keepalive"]:
            self.close()
        try:
            d = dbargs["dbn"]
            u = dbargs["user"]
            p = dbargs["pass"]
            h = dbargs["host"]
            if self.printargs["debug"]: print("d:{} u:{} p:{} h:{}".format(d,u,p,h))
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
        if self.c.execute("USE `{}`".format(dbargs["dbn"])):
            self.atteched = True
        return self

    def show(self):
        print("{}".format(self))

    def __str__(self):
        return "dbn=[{}] conn=[{}] c=[{}]".format(self.dbargs["dbn"], self.conn, self.c)

    def close(self):
        if self.conn is None: return self
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
        if self.printargs["verbose"]:
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
    _dbargs = {"dbn"       : "FileHash"
              ,"user"      : "FileHash"
              ,"pass"      : "dbms"
              ,"host"      : "rdbms.telus.local"
              ,"keepalive" : False
    }

    _printargs = {"quiet": False
                 ,"verbose": True
                 ,"debug": True
    }

    d = dbi(_dbargs,_printargs)
    f = realpath(abspath(argv[0]))
    from socket import gethostname as hostname
    from file_hasher import hash

    h = hash(f)
    d.insert("hn",[hostname()])
    d.insert("dn",[dirname(f)])
    d.insert("dh",[hostname(),dirname(f)])
    d.select("all_from_fqdn")

    raise RuntimeError("this is meant to be imported")
