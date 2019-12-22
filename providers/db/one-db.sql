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

