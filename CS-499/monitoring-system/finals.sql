-- MySQL dump 10.13  Distrib 8.0.21, for Linux (x86_64)
--
-- Host: localhost    Database: zoo
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `animals`
--

DROP TABLE IF EXISTS `animals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `animals` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `name` char(30) NOT NULL,
  `species` char(30) NOT NULL,
  `age` mediumint unsigned NOT NULL,
  `health` char(255) NOT NULL,
  `feeding` char(255) NOT NULL,
  `alarm` tinyint unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animals`
--

LOCK TABLES `animals` WRITE;
/*!40000 ALTER TABLE `animals` DISABLE KEYS */;
INSERT INTO `animals` VALUES (1,'Leo','lion',5,'Cut on left front paw','Twice daily',1),(2,'Maj','tiger',15,'None','3x daily',0),(3,'Baloo','bear',6,'None','None',2),(4,'Spots','giraffe',12,'None','Grazing',0),(12,'Betsy','cow',2,'None','Grazing',0);
/*!40000 ALTER TABLE `animals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `habitats`
--

DROP TABLE IF EXISTS `habitats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `habitats` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `habitat` char(30) NOT NULL,
  `species` char(30) NOT NULL,
  `temperature` char(255) NOT NULL,
  `feeding` char(255) NOT NULL,
  `cleaning` char(255) NOT NULL,
  `alarm` tinyint unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habitats`
--

LOCK TABLES `habitats` WRITE;
/*!40000 ALTER TABLE `habitats` DISABLE KEYS */;
INSERT INTO `habitats` VALUES (1,'Penguin Habitat','penguin','Freezing','Fish in water running low','Passed',2),(2,'Bird House','bird','Moderate','Natural from environment','Passed',0),(3,'Aquarium','aquarium','Varies with output temperature','Added daily','Needs cleaning from algae',3),(6,'Cowtopia','cow','Moderate','Grazing','Passed',0);
/*!40000 ALTER TABLE `habitats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-20  3:04:40
