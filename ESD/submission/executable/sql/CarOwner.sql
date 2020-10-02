-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 10, 2020 at 07:55 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS carowner DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE carowner;

DROP TABLE IF EXISTS `carowner`;
CREATE TABLE IF NOT EXISTS `carowner` (
  `coID` int(15) NOT NULL AUTO_INCREMENT,
  `coUsername` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `telegramID` varchar(64) NOT NULL,
  `coPassword` varchar(64) NOT NULL,
  PRIMARY KEY (`coID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `carowner` (`coID`, `coUsername`, `name`, `email`, `telegramID`, `coPassword`) 
VALUES
(1, 'choozy', 'Choo Zheng Yang', 'choozhengyang@hotmail.com','choo_zy', 'choozy'),
(2, 'winthony', 'Edwin Lee', 'edwinlee14@gmail.com', 'is0ap', 'winthony'),
(3, 'charmz', 'Charmaine', 'charmz@gmail.com','cappletrx', 'charmz'),
(4, 'betaced', 'Cedric', 'cedric@gmail.com', 'CedricLSM', 'betaced'),
(5, 'fiona', 'Fiona', 'fionaaoye@gmail.com', 'porcupie', 'fiona'),
(6, 'chanel', 'Chanel', 'chanel@gmail.com', 'chanelxy' , 'chanel');

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

