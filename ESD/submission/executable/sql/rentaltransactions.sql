SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


CREATE DATABASE IF NOT EXISTS `rentaltransaction` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `rentaltransaction`;
drop table if exists rentaltransaction;

create table rentaltransaction(
transactionID int(15) not null AUTO_INCREMENT,
crID int(15) not null,
coID int(15) not null,
carID int(15) not null,
rentalDate date not null,
price decimal(10,2) not null,
rentalStatus varchar(64) not null,

Constraint rentaltransaction_pk Primary Key (transactionID)
);

INSERT INTO rentaltransaction (crID,coID,carID,rentalDate,price,rentalStatus)
VALUES 
('03', '06', '11', '2020-01-09','35','completed'),
('03', '06', '11', '2020-01-10','35','completed'),
('03', '06', '11', '2020-01-11','35','completed'),
('03', '04', '03', '2020-02-02','35','completed'),
('03', '04', '03', '2020-02-03','35','completed'),
('03', '05', '10', '2020-03-14','85','completed'),
('03', '05', '10', '2020-03-15','85','completed'),
('03', '05', '10', '2020-03-16','85','completed');

commit;