CREATE OR REPLACE DATABASE `FileHash`;
USE `FileHash`;

CREATE TABLE `hostnames` (
  `hostid`	BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `hostname`	TEXT UNIQUE NOT NULL
) ENGINE=MyISAM;

CREATE TABLE `dirnames` (
  `dirid`	BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `dirname`	TEXT NOT NULL
) ENGINE=MyISAM;

CREATE TABLE `file_instance` (
  `fileid`	BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  `hostid`	BIGINT NOT NULL,
  `dirid`	BIGINT NOT NULL,
  CONSTRAINT `pk_hostid`
    FOREIGN KEY (`hostid`)
    REFERENCES `hostnames` (`hostid`)
    ON UPDATE NO ACTION
    ON DELETE SET NULL,
  CONSTRAINT `pk_dirid`
    FOREIGN KEY (`dirid`)
    REFERENCES `dirnames` (`dirid`)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
) ENGINE=MyISAM;

CREATE TABLE `stats` (
  `size`	INT NOT NULL,
  `mtime`	INT NOT NULL,
  `hash`	VARCHAR(64) NOT NULL,
  `fileid`	BIGINT NOT NULL,
  PRIMARY KEY (`size`,`mtime`,`hash`,`fileid`),
  CONSTRAINT `pk_fileid`
    FOREIGN KEY (`fileid`)
    REFERENCES `file_instance` (`fileid`)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
) ENGINE=MyISAM;

CREATE TABLE `filenames` (
  `fileid`	BIGINT UNSIGNED PRIMARY KEY,
  `filename`	TEXT NOT NULL,
  CONSTRAINT `pk_fileid`
    FOREIGN KEY (`fileid`)
    REFERENCES `file_instance` (`fileid`)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
) ENGINE=MyISAM;

CREATE VIEW `fqpn` AS
  SELECT
    `h`.`hostname` AS `hostname`,
    `d`.`dirname`  AS `dirname`,
    `f`.`filename` AS `filename`,
    `fi`.`fileid` AS `fileid`
  FROM
    `file_instance` AS `fi`
    INNER JOIN `dirnames` AS `d`
     ON `d`.`dirid` = `fi`.`dirid`
    INNER JOIN `hostnames` AS `h`
     ON `h`.`hostid` = `fi`.`hostid`
    INNER JOIN `filenames` AS `f`
     ON `f`.`fileid` = `fi`.`fileid`;

INSERT INTO `fqpn`
  SET
    `fqpn`.`hostname`='localhost';

INSERT INTO `fqpn`
  SET
    `fqpn`.`dirname`='/foo';

UPDATE `fqpn`
  SET
    `fqpn`.`filename`='bar'
  WHERE
    `fqpn`.`hostname`='localhost' AND
    `fqpn`.`dirname`='/foo';

select * from hostnames;
select * from dirnames;
select * from filenames;
select * from file_instance;
     
CREATE VIEW
    `fstat` AS
  SELECT
    `fqpn`.`hostname`,
    `fqpn`.`dirname`,
    `fqpn`.`filename`,
    `stats`.`size`,
    `stats`.`mtime`,
    `stats`.`hash`
  FROM
    `fqpn`,
    `stats`
  WHERE
    `fqpn`.`fileid` = `stats`.`fileid`;


SELECT * FROM `fqpn`;
SELECT * FROM `fstat`;
