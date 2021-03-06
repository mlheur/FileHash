#!/usr/bin/env python3

from sys import argv, stderr
from os import chdir, environ
from os.path import realpath, dirname, join as join_path
from site import addsitedir

basedir = dirname(realpath(argv[0]))
addsitedir(basedir)
addsitedir(join_path(basedir, "lib"))
from hash_dbi import hash_dbi as dbi
from file_scanner import file_scanner as scanner
from file_sifter import file_sifter as sifter

class FileHash(object):
    def __init__(self, mode, opts):
        self.mode = mode
        self.opts = opts
        self.sifter = sifter()
        self.dbi = dbi(self.sifter)
        self.scanner = scanner(self.dbi,self.sifter)
        if "debug" in environ and int(environ["debug"]) > 0:
            self.dbi.printargs["debug"] = True

    def run(self): getattr(self, self.mode, lambda: 'Invalid')()
    def scan(self): self.scanner.scan(self.opts)
    def report(self): self.dbi.report(self.opts)

    # ToDo: def prune(self): # remove hashtable entries against


if __name__ == "__main__":
    arg0 = argv[0]
    argv = argv[1:]
    chdir(dirname(arg0))
    if len(argv) == 0:
        stderr.write("Usage: {} <command> [-opts]\n".format(arg0))
        # ToDo: document commands and opts
        exit(2)
    mode = argv[0]
    opts = argv[1:]
    FileHash(mode, opts).run()
