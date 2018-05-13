/*


*/

-- MySQL dump 10.13  Distrib 5.6.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: electronics
-- ------------------------------------------------------
-- Server version	5.6.28-0ubuntu0.15.04.1


--
-- Table structure for table `goods_table`
--

DROP TABLE IF EXISTS `goods_table`;

CREATE TABLE `goods_table` (
  `id` int(4) AUTO_INCREMENT NOT NULL ,
  `name` varchar(45) NOT NULL,
  `kind` varchar(20) NOT NULL,
  `price` int(11) NOT NULL,
  `discount` int(11) DEFAULT NULL,
  `store` int(11) NOT NULL,
  `detail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `goods_table`
--

LOCK TABLES `goods_table` WRITE;
INSERT INTO `goods_table` VALUES (1,'computer','A',50,9,100,'cheap'),(2,'mouse','B',50,9,200,NULL); -- 3
UNLOCK TABLES;

--
-- Table structure for table `order_table`
--

DROP TABLE IF EXISTS `order_table`; -- 2

CREATE TABLE `order_table` ( -- 1
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) NOT NULL,
  `good_id` int(4) DEFAULT NULL,
  `goods_name` varchar(20) DEFAULT NULL,
  `goods_num` int(4) DEFAULT NULL,
  `sum` int(6) DEFAULT NULL,
  `deal_time` varchar(20) DEFAULT NULL,
  `pay` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order_table`
--

LOCK TABLES `order_table` WRITE;
INSERT INTO `order_table` VALUES (1,'002',2,'mouse',3,60,'2017-05-31-18:39',0);
UNLOCK TABLES;

--
-- Table structure for table `user_table`
--

DROP TABLE IF EXISTS `user_table`; --2

CREATE TABLE `user_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `addr` text,
  `tel` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

LOCK TABLES `user_table` WRITE;
INSERT INTO `user_table` VALUES (1,'123','abc123',NULL,NULL),(2,'124','def456',NULL,NULL),(3,'125','abc123','HIT','18963166073'),(4,'127','abc123','HIT','18963166073'),(5,'129','abc123','HIT','18963166073'),(6,'130','abc123','HIT','18963166073'),(7,'132','abc123','HIT','18963166073'),(8,'135','abc123','HIT','18963166073'),(9,'185','abc123','HIT','18963166073'),(10,'165','abc123','HIT','18963166073'),(11,'795','abc123','HIT','18963166073'),(12,'9999','c81e728d9d4c2f636f067f89cc14862c','fff','sdf');

