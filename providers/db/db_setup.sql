--
-- Database: `billdb`
--

CREATE DATABASE IF NOT EXISTS `billdb`;
USE `billdb`;

-- --------------------------------------------------------

--
-- Table structure
--

CREATE TABLE IF NOT EXISTS `Provider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  AUTO_INCREMENT=10001 ;

CREATE TABLE IF NOT EXISTS `Rates` (
  `product_id` varchar(50) NOT NULL,
  `rate` int(11) DEFAULT 0,
  `scope` varchar(50) DEFAULT NULL,
  FOREIGN KEY (scope) REFERENCES `Provider`(`id`)
) ENGINE=MyISAM ;

CREATE TABLE IF NOT EXISTS `Trucks` (
  `id` varchar(10) NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`provider_id`) REFERENCES `Provider`(`id`)
) ENGINE=MyISAM ;
--
-- Dumping data
--

/*
INSERT INTO Provider (`name`) VALUES ('ALL'), ('pro1'),
(3, 'pro2');

INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES ('1', 2, 'ALL'),
(2, 4, 'pro1');

INSERT INTO Trucks (`id`, `provider_id`) VALUES ('134-33-443', 2),
('222-33-111', 1);
*/
--
-- Database: `Weight`
--

CREATE DATABASE IF NOT EXISTS `weight`;

-- --------------------------------------------------------

--
-- Table structure for table `containers-registered`
--

USE weight;


CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  --   "neto": <int> or "na" // na if some of containers unknown
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

show tables;

describe containers_registered;
describe transactions;



--
-- Dumping data for table `test`
--

-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa'),
Skip to content
 
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@saarice 
5
0 3 argamanza/gan-shmuel
 Code  Issues 0  Pull requests 1  Projects 1  Wiki  Security  Insights
gan-shmuel/docker/db/db_create.sql
@argamanza argamanza change whole structure to act as CI Server
9774e22 on Apr 18
118 lines (89 sloc)  4.3 KB
  
CREATE DATABASE  IF NOT EXISTS `db` /* Blue's db! */;
USE `db`;
-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: db
-- ------------------------------------------------------
-- Server version	8.0.15


DROP TABLE IF EXISTS `containers`;
CREATE TABLE `containers` (
  `id` varchar(45) NOT NULL,
  `weight` float NOT NULL,
  `unit` enum('kg','lbs') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(45) NOT NULL,
  `rate` int(11) NOT NULL,
  `scope` varchar(45) NOT NULL DEFAULT 'ALL',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `providers`;
CREATE TABLE `providers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `providername` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `trucks`;
CREATE TABLE `trucks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `truckid` varchar(45) NOT NULL,
  `providerid` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `unit` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `direction` enum('in','out','none') DEFAULT NULL,
  `f` bool DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `bruto` float DEFAULT NULL,
  `neto` float DEFAULT NULL,
  `trucks_id` int(11) DEFAULT NULL,
  `products_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `containers_has_sessions`;
CREATE TABLE `containers_has_sessions` (
  `containers_id` varchar(45) NOT NULL,
  `sessions_id` int(11) NOT NULL,
  PRIMARY KEY (`containers_id`,`sessions_id`),
  KEY `fk_containers_has_sessions_sessions1_idx` (`sessions_id`),
  KEY `fk_containers_has_sessions_containers1_idx` (`containers_id`),
  CONSTRAINT `fk_containers_has_sessions_containers1` FOREIGN KEY (`containers_id`) REFERENCES `containers` (`id`),
  CONSTRAINT `fk_containers_has_sessions_sessions1` FOREIGN KEY (`sessions_id`) REFERENCES `sessions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `trucks` (`id`, `truckid`) VALUES (1, 'none');

INSERT INTO providers (providername) VALUES ('Tapuzina');
INSERT INTO providers (providername) VALUES ('Herut');
INSERT INTO providers (providername) VALUES ('Mishmeret');
INSERT INTO providers (providername) VALUES ('KfarHess');

INSERT INTO containers (id,weight,unit) VALUES ('K-8263',666,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-7854',854,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-6523',741,'kg');
INSERT INTO containers (id,weight,unit) VALUES ('K-2369',120,'kg');
INSERT INTO containers (id,weight,unit) VALUES ('K-7845',999,'lbs');

INSERT INTO products (product_name,rate,scope) VALUES ('Blood',122,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Mandarin',103,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Navel',97,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Blood',102,'1');
INSERT INTO products (product_name,rate,scope) VALUES ('Clementine',100,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Tangerine',80,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Clementine',90,'2');

INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('77777',2,666,'lbs');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('66666',2,120,'kg');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('99888',1,999,'lbs');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('66321',3,741,'kg');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('12365',4,854,'lbs');


INSERT INTO sessions (direction, f, date, bruto, neto, trucks_id, products_id) VALUES ('in', 1, '20181218181512', 999, 800, 77777, 2);
INSERT INTO sessions (direction, f, date, bruto, neto, trucks_id, products_id) VALUES ('in', 1, '20161218181512', 120, 100, 99888, 1);
INSERT INTO sessions (direction, f, date, bruto, neto, trucks_id, products_id) VALUES ('out', 1, '20170920102017', 741, 650, 12365, 3);









© 2019 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About

