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

    SELECT['fqdn_from_fqdn_where_hn_dn'] = '''SELECT `fqdn` FROM `vw_fqdn` WHERE `hn` = %s AND `dn` = %s'''

    SELECT['distinct_hashes'] = '''SELECT DISTINCT `hash` FROM `vw_fqpn`'''
    SELECT['from_fqpn_where_hash_is'] = '''SELECT * FROM `vw_fqpn` WHERE `hash` = %s'''
    SELECT['from_fqpn_where_fqpn_is'] = '''SELECT * FROM `vw_fqpn` WHERE `hn` = %s AND `dn` = %s AND `fn` = %s'''

    INSERT['hn'] =\
    '''INSERT IGNORE INTO `hosts`(`hn`) VALUES(%s)'''

    INSERT['dn'] =\
    '''INSERT IGNORE INTO `dirs` (`dn`) VALUES(%s)'''

    INSERT['dh'] =\
    '''INSERT IGNORE INTO `dir_on_host` (`hid`,`did`)
       VALUES(({}),({}))'''\
    .format(SELECT['hid_from_hn'],SELECT['did_from_dn'])

    INSERT['fqpn'] =\
    '''INSERT IGNORE INTO `file_in_dir` (`hid`,`did`,`fn`,`size`,`mtime`,`hash`)
       VALUES ((SELECT `hid` FROM `vw_fqdn` WHERE `fqdn` = %s)
       ,(SELECT `did` FROM `vw_fqdn` WHERE `fqdn` = %s)
       ,%s,%s,%s,%s)'''

if __name__ == "__main__":
    raise RuntimeError("this is meant to be imported")
