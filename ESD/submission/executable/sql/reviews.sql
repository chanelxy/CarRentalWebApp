SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


DROP DATABASE IF EXISTS reviews;
CREATE DATABASE reviews;
USE reviews;

DROP TABLE IF EXISTS `reviews`;
CREATE TABLE IF NOT EXISTS `reviews` (
  `RID` int(11) NOT NULL AUTO_INCREMENT,
  `crUsername` varchar(128) NOT NULL,
  `cID` int(11) NOT NULL,
  `reviewContents` varchar(1000) NOT NULL,
  PRIMARY KEY (`RID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;


INSERT INTO `reviews` (`RID`, `crUsername`, `cID`, `reviewContents`) 
VALUES
(1, 'amy111', '1', 'Nice car, great owner!'),
(2, 'bebe111', '2', 'Clean but old'),
(3, 'cutie111', '3', 'Pretty owner : - )'),
(4, 'doggy111', '4', 'Wow even prettier owner.'),
(5, 'ugly111', '6', 'Try harder next time, car quite bad....'),
(6, 'amy111', '7', 'Nice car, great owner!'),
(7, 'bebe111', '8', 'Clean but old'),
(8, 'cutie111', '9', 'Pretty owner : - )'),
(9, 'doggy111', '10', 'Wow even prettier owner.'),
(10, 'ugly111', '11', 'Try harder next time, car quite bad....');

COMMIT;
