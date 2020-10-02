-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 10, 2020 at 08:04 AM
-- Server version: 5.7.26
-- PHP Version: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: 'carrenter'
--

-- --------------------------------------------------------

--
-- Table structure for table 'CarRenter'
--
CREATE DATABASE IF NOT EXISTS carrenter DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE carrenter;
DROP TABLE IF EXISTS `carrenter`;

CREATE TABLE IF NOT EXISTS `carrenter` (
  `crID` int(15) NOT NULL AUTO_INCREMENT,
  `crUsername` varchar(64) NOT NULL,
  `crPassword` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `telegramID` varchar(64) NOT NULL,
  PRIMARY KEY (`crID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `carrenter` (`crID`, `crUsername`, `crPassword`, `name`, `email`, `telegramID`) 
VALUES 
(NULL, 'amy111', 'amy111',  'Amy Tan', 'edwinlee14@gmail.com', 'is0ap'),
(NULL, 'bebe111', 'bebe111', 'Bebe Tan', 'edwinlee14@gmail.com', 'is0ap'),
(NULL, 'cutie111', 'cutie111', 'Cutie Tan', 'choozhengyang@hotmail.com', 'choo_zy'),
(NULL, 'doggy111', 'doggy111', 'Doggy Tan', 'fionaaoye@gmail.com', 'porcupie'),
(NULL, 'ugly111', 'ugly111', 'Ugly Tan', 'ugly.tan@gmail.com', 'uglytan111');

COMMIT;

--
-- Truncate table before insert 'CarRenter'
--

-- TRUNCATE TABLE 'CarRenter';