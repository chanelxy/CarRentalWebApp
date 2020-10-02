SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: car
--
CREATE DATABASE IF NOT EXISTS car DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE car;

-- --------------------------------------------------------

--
-- Table structure for table car
--

DROP TABLE IF EXISTS car;
CREATE TABLE IF NOT EXISTS car (
  cID int(11) NOT NULL AUTO_INCREMENT,
carPlateNo varchar(100) not null,
coUsername varchar(100) not null,
brand varchar(100) not null,
model varchar(100) not null,
colour char(100) not null,
capacity int(15) not null,
transmissionType char(100) not null,
dailyRate int(15) not null,
postalCode int(6) not null,

  PRIMARY KEY (cid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table car
--

INSERT INTO car (carplateno,cousername,brand,model,colour,capacity,transmissiontype,dailyrate,postalCode) VALUES 
 ('sku911c', 'fiona', 'Porsche', '911', 'Red','2', 'auto', 85,600111),
 ('sku8882c', 'fiona', 'Audi', 'R8', 'Black','2', 'manual', 85,600111),
 ('sku8888d', 'chanel', 'Range Rover', 'V6', 'White','7', 'manual', 65,600112),
 ('sku8883c', 'betaced', 'Honda', '338', 'Purple','5', 'auto', 35,600113),
 ('sku2382c', 'fiona', 'Toyota', 'Prius', 'White','5', 'auto', 35, 310156),
 ('sku5288d', 'chanel', 'Ford', 'Mustang', 'Red','2', 'manual', 75, 199447),
 ('sku8423c', 'betaced', 'BMW', 'X1', 'Black','5', 'auto', 55, 530425),
 ('sku5232c', 'winthony', 'Mercedes', 'GLC', 'White','5', 'auto', 65, 058282),
 ('sku2324e', 'charmz', 'Volvo', 'S11', 'Blue','5', 'manual', 35,150164),
 ('sku8351g', 'fiona', 'Peugeot', '207', 'White','2', 'manual', 65, 408571),
 ('sku2382c', 'fiona', 'Mercedes', 'Eclass', 'White','5', 'auto', 85, 508988),
 ('sku2288d', 'chanel', 'Peugeot', '508 GT', 'Black','2', 'manual', 35, 238877),
 ('sku1563l', 'betaced', 'Honda', 'Civic', 'Black','5', 'auto', 45, 757700),
 ('sku5488a', 'winthony', 'Toyota', 'Prius', 'White','5', 'auto', 35, 237994),
 ('sku5555c', 'betaced', 'Toyota', 'Wish', 'Pink','7', 'auto', 85,600111),
 ('sku9999c', 'fiona', 'Mercedes', 'MB290', 'Green','9', 'manual', 85,530425),
 ('sku8388k', 'charmz', 'Volkswagen', '555', 'Blue','5', 'manual', 35,238866);

 COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
