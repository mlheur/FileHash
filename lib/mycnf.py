#!/usr/bin/env python3

from sys import argv
from os.path import abspath, realpath, dirname, basename, join as join_path, exists
from os import environ as env
from mysql import connector as dbms
from time import sleep, time as now
from site import addsitedir

class mycnf(object):
    """ Parse $HOME/.my.cnf for FileHash dbargs. """

    def __init__(self,mycnf=None,user=None,password=None,database=None,host=None):
        self.mycnf = mycnf
        if self.mycnf is None:
            self.mycnf = join_path(env["HOME"], ".my.cnf")
        if not exists(abspath(realpath(self.mycnf))):
            raise RuntimeError("could not find my.cnf at {}".format(self.mycnf))

        self.user = user
        if user is None:
            self.loadval("user")
            
        self.password = password
        if password is None:
            password = self.loadval("password")
            
        self.database = database
        if database is None:
            database = self.loadval("database")
            
        self.host = host
        if host is None:
            host = self.loadval("host")
            
    def __str__(self):
        return "{}".format(self.__dict__)

    def loadval(self,val):
        cnf = open(self.mycnf, "r")
#       print("got cnf {}".format(cnf))
        while True:
            text = cnf.readline().strip("\n")
#           print("got line {}".format(text))
            if len(text) == 0:
                 break
            try:
                [k,v] = text.split("=")
            except ValueError as ve:
#               print(ve)
                continue
#           print("got [k,v]{}".format([k,v]))
            if k.strip(' 	') == val:
                self.__dict__[val] = v.strip(' 	')
        cnf.close()

if __name__ == "__main__":
    my = mycnf()
    print(my)
    print(my.user)
    print(my.password)
    print(my.host)
    raise RuntimeError("this is meant to be imported")
