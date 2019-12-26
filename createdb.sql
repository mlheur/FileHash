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
    `hostnames`.`hostname`,
    `dirnames`.`dirname`,
    `filenames`.`filename`,
    `file_instance`.`fileid` AS `fileid`
  FROM
    `hostnames`,
    `dirnames`,
    `filenames`,
    `file_instance`
  WHERE
    `hostnames`.`hostid` = `file_instance`.`hostid` AND
    `dirnames`.`dirid`   = `file_instance`.`dirid` AND
    `filenames`.`fileid` = `file_instance`.`fileid`;

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

INSERT INTO `hostnames` SET `hostname` = 'localhost';
INSERT INTO `dirnames` SET `dirname` = '/foo';

INSERT INTO `fqpn` SET `fqpn`.`file`='bar'
 WHERE `fqpn`.`dirname`='/foo' AND `fqpn`.`hostname`='localhost';

     
INSERT INTO `fstat`
 SET
     `fstat`.`size`='0',
     `fstat`.`mtime`='12345', 
     `fstat.`hash`='ABC789'
     `fstat`.`fileid` = (
  SELECT
       `fqpn`.`fileid`
  FROM
       `fqpn`
  WHERE
       `fqpn`.`filename`='bar' AND
       `fqpn`.`dirname`='/foo' AND
       `fqpn`.`hostname`='localhost')
;
     

SELECT * FROM `fqpn`;
SELECT * FROM `fstat`;
