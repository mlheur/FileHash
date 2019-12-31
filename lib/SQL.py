#!/usr/bin/env python3

class SQL:
    """ static strings used for structured queries. """
    INSERT = {}
    SELECT = {}
    DELETE = {}



    SELECT['all_from_fqdn'] = '''SELECT * FROM `vw_fqdn`'''
    SELECT['all_from_fqpn'] = '''SELECT * FROM `vw_fqpn`'''

    SELECT['hid_from_hn'] = '''SELECT `id` FROM `hosts` WHERE `hn` = %s'''
    SELECT['did_from_dn'] = '''SELECT `id` FROM `dirs`  WHERE `dn` = %s'''

    SELECT['hid_from_fqdn'] = '''SELECT `hid` FROM `vw_fqdn` WHERE `fqdn` = %s'''
    SELECT['did_from_fqdn'] = '''SELECT `did` FROM `vw_fqdn` WHERE `fqdn` = %s'''

    SELECT['distinct_hashes'] = '''SELECT DISTINCT `hash` FROM `vw_fqpn`'''
    SELECT['all_from_hash'] = '''SELECT * FROM `vw_fqpn` WHERE `hash` = %s'''

    INSERT['hn'] =\
    '''INSERT IGNORE INTO `hosts`(`hn`) VALUES(%s)'''

    INSERT['dn'] =\
    '''INSERT IGNORE INTO `dirs` (`dn`) VALUES(%s)'''

    INSERT['dh'] =\
    '''INSERT INTO `dir_on_host` (`hid`,`did`)
       VALUES(({}),({}))'''\
    .format(SELECT['hid_from_hn'],SELECT['did_from_dn'])

    INSERT['fqpn'] =\
    '''INSERT IGNORE INTO `file_in_dir` (`hid`,`did`,`fn`,`size`,`mtime`,`hash`)
       VALUES ((SELECT `hid` FROM `vw_fqdn` WHERE `fqdn` = %s)
       ,(SELECT `did` FROM `vw_fqdn` WHERE `fqdn` = %s)
       ,%s,%s,%s,%s)'''

if __name__ == "__main__":
    raise RuntimeError("this is meant to be imported")
