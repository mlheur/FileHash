CREATE OR REPLACE DATABASE `FileHash`;
USE `FileHash`;

--------------------------------------------------------------------------------
-- hosts
--------------------------------------------------------------------------------
CREATE TABLE `hosts`
(`hn` VARCHAR(255) UNIQUE NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
) ENGINE=MyISAM;

SELECT * from `hosts`;

--------------------------------------------------------------------------------
-- dirs
--------------------------------------------------------------------------------
CREATE TABLE `dirs`
(`dn` TEXT UNIQUE NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
) ENGINE=MyISAM;


--------------------------------------------------------------------------------
-- dir_on_host
--------------------------------------------------------------------------------
CREATE TABLE `dir_on_host`
(`hid` BIGINT NOT NULL
,`did` BIGINT NOT NULL
,PRIMARY KEY(`hid`,`did`)
,CONSTRAINT `pk_hid`
 FOREIGN KEY (`hid`)
 REFERENCES `hosts` (`id`)
 ON DELETE CASCADE
,CONSTRAINT `pk_did`
 FOREIGN KEY (`did`)
 REFERENCES `dirs` (`id`)
) ENGINE=MyISAM;

CREATE VIEW `vw_fqdn` (`hn`,`dn`,`fqdn`,`hid`,`did`) AS
SELECT `h`.`hn`
,`d`.`dn`
,CONCAT(`h`.`hn`,':',`d`.`dn`)
,`dh`.`hid`
,`dh`.`did`
FROM `dir_on_host` `dh`
INNER JOIN `hosts` `h`
ON `dh`.`hid`=`h`.`id`
INNER JOIN `dirs` `d`
ON `dh`.`did`=`d`.`id`
;

--------------------------------------------------------------------------------
-- file_in_dir
--------------------------------------------------------------------------------
CREATE TABLE `file_in_dir`
(`hid` BIGINT UNSIGNED NOT NULL
,`did` BIGINT UNSIGNED NOT NULL
,`hash` VARCHAR(64) NOT NULL
,`fn` TEXT NOT NULL
,`size` BIGINT UNSIGNED NOT NULL
,`mtime` INT UNSIGNED NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
,CONSTRAINT `pk_hid`
 FOREIGN KEY (`hid`)
 REFERENCES `dir_on_host` (`did`)
 ON DELETE CASCADE
,CONSTRAINT `pk_did`
 FOREIGN KEY (`did`)
 REFERENCES `dir_on_host` (`did`)
 ON DELETE CASCADE
) ENGINE=MyISAM;

CREATE VIEW `vw_fqpn` (`id`,`hn`,`dn`,`fn`,`size`,`mtime`,`hash`,`fqdn`,`fqpn`) AS
SELECT `fd`.`id`
,`vw_fqdn`.`hn`
,`vw_fqdn`.`dn`
,`fd`.`fn`
,`fd`.`size`
,`fd`.`mtime`
,`fd`.`hash`
,`vw_fqdn`.`fqdn`
,(CONCAT(`vw_fqdn`.`fqdn`,'/',`fd`.`fn`))
FROM file_in_dir `fd`
INNER JOIN `vw_fqdn`
ON (`fd`.`hid`=`vw_fqdn`.`hid` AND `fd`.`did` = `vw_fqdn`.`did`)
;

--DBG--  --------------------------------------------------------------------------------
--DBG--  -- TESTS
--DBG--  -- 1a
--DBG--  INSERT INTO `hosts` (`hn`)
--DBG--  VALUES ('budweiser'),('labatts'),('canadian'),('losmuertos');
--DBG--  -- 1b
--DBG--  INSERT INTO `dirs` (`dn`)
--DBG--  VALUES ('/'),('/etc'),('/bin'),('/foo/bar');
--DBG--  -- 1c
--DBG--  insert into dir_on_host (hid,did)
--DBG--  VALUES ((SELECT hosts.id FROM hosts WHERE hosts.hn = 'budweiser'),(SELECT dirs.id FROM dirs WHERE dirs.dn = '/etc'));
--DBG--  -- 1.
--DBG--  SELECT * FROM vw_fqdn;
--DBG--  -- 2a
--DBG--  INSERT INTO `file_in_dir` (`dhid`,`hash`,`fn`,`size`,`mtime`)
--DBG--  VALUES ((SELECT id FROM vw_fqdn WHERE fqdn = 'budweiser:/etc')
--DBG--  ,'01234556789ABCDEF','fstab',32,1598764320)
--DBG--  ;
--DBG--  -- 2.
--DBG--  SELECT * FROM vw_fqpn;
--DBG--  --------------------------------------------------------------------------------
