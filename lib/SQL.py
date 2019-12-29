#!/usr/bin/env python3

class SQL:
    """ static strings used for structured queries. """
    INSERT = {}
    SELECT = {}
    DELETE = {}



    SELECT['all_from_fqdn'] = '''SELECT * FROM `vw_fqdn`;'''
 
    SELECT['hid_from_hn'] = '''SELECT `id` FROM `hosts` WHERE hn = '?';'''

    SELECT['did_from_dn'] = '''SELECT `id` FROM `dirs`  WHERE dn = '?';'''



    INSERT['hn'] =\
    '''INSERT IGNORE INTO `hosts`(`hn`) VALUES(?);'''

    INSERT['dn'] =\
    '''INSERT IGNORE INTO `dirs` (`dn`) VALUES(?);'''

    INSERT['dh'] =\
    '''INSERT INTO `dir_on_host` (`hid`,`did`)
       VALUES(({}),({}));'''\
    .format(SELECT['hid_from_hn'],SELECT['did_from_dn'])



if __name__ == "__main__":
    raise RuntimeError("this is meant to be imported")
