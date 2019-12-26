CREATE OR REPLACE DATABASE `FileHash`;
USE `FileHash`;

--------------------------------------------------------------------------------
-- hosts
--------------------------------------------------------------------------------
CREATE TABLE `hosts`
(`hn` VARCHAR(255) UNIQUE NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
) ENGINE=MyISAM;


INSERT INTO `hosts` (`hn`)
VALUES ('budweiser')
,('labatts')
,('canadian')
,('losmuertos')
;

-- SELECT * from `hosts`;

--------------------------------------------------------------------------------
-- dirs
--------------------------------------------------------------------------------
CREATE TABLE `dirs`
(`dn` TEXT UNIQUE NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
) ENGINE=MyISAM;


INSERT INTO `dirs` (`dn`)
VALUES ('/')
,('/bin')
,('/etc')
,('/usr')
;

-- SELECT * from `dirs`;

--------------------------------------------------------------------------------
-- dir_on_host
--------------------------------------------------------------------------------
CREATE TABLE `dir_on_host`
(`hostid` BIGINT NOT NULL
,`dirid` BIGINT NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
,CONSTRAINT `pk_hostid`
 FOREIGN KEY (`hostid`)
 REFERENCES `hosts` (`id`)
 ON DELETE CASCADE
,CONSTRAINT `pk_dirid`
 FOREIGN KEY (`dirid`)
 REFERENCES `dirs` (`id`)
) ENGINE=MyISAM;

INSERT INTO `dir_on_host` (`hostid`,`dirid`)
VALUES (1,1)
,(1,2)
,(1,3)
,(2,1)
,(2,4)
,(3,1)
,(3,3)
,(3,4)
;

CREATE VIEW `fqdn` AS
SELECT CONCAT(`hn`,':',`dn`) AS `fqdn`
FROM `dir_on_host` `dh`
INNER JOIN `hosts` `h`
ON `dh`.`hostid`=`h`.`id`
INNER JOIN `dirs` `d`
ON `dh`.`dirid`=`d`.`id`;

-- SELECT * FROM `dir_on_host`;

--------------------------------------------------------------------------------
-- fstats
--------------------------------------------------------------------------------
CREATE TABLE `fstats`
(`size` BIGINT NOT NULL
,`mtime` BIGINT NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
) ENGINE=MyISAM;


--------------------------------------------------------------------------------
-- hashes
--------------------------------------------------------------------------------
CREATE TABLE `hashes`
(`hash` VARCHAR(64) UNIQUE NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
) ENGINE=MyISAM;


--------------------------------------------------------------------------------
-- file_in_dir
--------------------------------------------------------------------------------
CREATE TABLE `file_in_dir`
(`dirhostid` BIGINT UNSIGNED NOT NULL
,`hashid` BIGINT UNSIGNED NOT NULL
,`filename` TEXT NOT NULL
,`size` BIGINT UNSIGNED NOT NULL
,`mtime` INT UNSIGNED NOT NULL
,`id` BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT
,CONSTRAINT `pk_dirhostid`
 FOREIGN KEY (`dirhostid`)
 REFERENCES `dir_on_host` (`id`)
 ON DELETE CASCADE
) ENGINE=MyISAM;

-- CREATE VIEW `fqpn` AS
-- (SELECT (CONCAT(`fqdn`,'/',`filename`)) AS `fqpn`
-- FROM file_in_dir `fd`
-- INNER JOIN `fqdn` `fqdn`
-- ON `fd`.`dirhostid`=`fqdn`.`id`
-- );
