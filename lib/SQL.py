#!/usr/bin/env python3

class SQL:
    """ static strings used for structured queries. """
    DROP = {}
    CREATE = {}
    INSERT = {}
    SELECT = {}
    UPDATE = {}
    DELETE = {}

    ATTACH = "ATTACH DATABASE '{}' As 'hashtable';"
    TABLES = ["finfo"]

    INSERT["finfo"] = \
        '''INSERT OR REPLACE
        INTO finfo (size, mtime, hash, last_seen, host, dirname, basename)
        VALUES(?,?,?,strftime('%s','now'),?,?,?)'''

    UPDATE["finfo"] = \
        '''UPDATE OR REPLACE
        finfo SET (size, mtime, hash, last_seen) = (?,?,?,strftime('%s','now'))
        WHERE host = ? AND dirname = ? AND basename = ?'''

    DELETE["finfo"] = \
        '''DELETE FROM finfo
        WHERE host = ? AND dirname = ? AND basename = ?'''

    SELECT["allhashes"] = \
        '''SELECT DISTINCT hash FROM finfo ORDER BY last_seen DESC'''

    SELECT["allall"] = \
        '''SELECT * FROM finfo'''

    SELECT["dinfo_from_finfo_as_host_fqpn_size_mtime"] = \
        '''SELECT host, dirname, basename, size, mtime, hash, last_seen FROM finfo
        WHERE host = ? AND dirname = ? AND basename = ? AND size = ? AND mtime = ?
        ORDER BY last_seen DESC'''

    SELECT["dinfo_from_host_fqpn"] = \
        '''SELECT host, dirname, basename, size, mtime, hash, last_seen FROM finfo
        WHERE host=? AND dirname=? AND basename=?
        ORDER BY last_seen DESC'''

    SELECT["dinfo_from_hash"] = \
        '''SELECT host, dirname, basename, size, mtime, hash, last_seen FROM finfo
        WHERE hash=?
        ORDER BY last_seen DESC'''

    DROP["finfo"] = \
        '''DROP TABLE IF EXISTS finfo;'''

    CREATE["finfo"] = \
        '''CREATE TABLE finfo (
        host TEXT NOT NULL,
        dirname TEXT NOT NULL,
        basename TEXT NOT NULL,
        size INTEGER NOT NULL,
        mtime INTEGER NOT NULL,
        hash TEXT NOT NULL,
        last_seen INTEGER NOT NULL,
        PRIMARY KEY (host, dirname, basename));'''


if __name__ == "__main__":
    print("this is meant to be imported")
