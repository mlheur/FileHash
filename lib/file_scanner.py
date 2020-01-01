#!/usr/bin/env python3

from sys import argv
from os import listdir as ls
from os.path import dirname, basename, realpath, abspath, isdir, isfile, islink, join as join_path, getsize, getmtime
from site import addsitedir

addsitedir(dirname(realpath(abspath(argv[0]))))


class file_scanner(object):
    """ Performs filesysem and hashing operations necessary to load file info into the database interface. """

    def __init__(self, dbi):
        self.dbi = dbi
        self.INCLUDE = [".profile"]
        self.EXCLUDE = [".DS_Store", "Thumbs.db", "Code Cache", "Cache", ".PyCharmCE2019.3", "__pycache__", ".git"]
        self.rehash = False

    def is_skippable(self, fqpn):
        if basename(fqpn) in self.INCLUDE: return False
        if basename(fqpn) in self.EXCLUDE: return True
        if basename(dirname(fqpn)) in self.EXCLUDE: return True
        if basename(dirname(fqpn)) in self.EXCLUDE: return True
        return False

    def mkfile(self, fqpn):
        if self.is_skippable(fqpn):
            return
        self.dbi.addfile(fqpn, self.rehash)

    def scandir(self, dir):
        try:
            if not isdir(dir):
                if isfile(dir) and not islink(dir):
                    self.mkfile(dir)
            else:
                for dirent in ls(dir):
                    fqpn = join_path(dir, dirent)
                    if islink(fqpn):
                        continue
                    if isdir(fqpn) and not self.is_skippable(fqpn):
                        self.scandir(fqpn)
                    if isfile(fqpn):
                        self.mkfile(fqpn)
        except PermissionError:
            pass

    def scan(self, opts):
        if len(opts) == 0:
            sys.stderr.write("Usage: ... scan [-opts] <dir|file> [ <dir2|file2> [ ... ] ]\n")
            sys.exit(2)
        # ToDo: peek at opts for flags, e.g. qualifiers (skip dot & hidden)
        while opts[0][0] == "-":
            opt = opts.pop(0)
            if opt == "--rehash": self.rehash = True
        for base in opts:
            self.scandir(realpath(abspath(base)))


if __name__ == "__main__":
    from hash_dbi import hash_dbi as dbi

    hdbi = dbi()
    file_scanner(hdbi).scan([realpath(abspath(".."))])
    print(hdbi.select_all_from_fqpn())
#    hdbi.report()
    raise RuntimeError("this is meant to be imported")
