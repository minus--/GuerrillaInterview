CREATE DATABASE  IF NOT EXISTS `coding_interview` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `coding_interview`;
-- MySQL dump 10.13  Distrib 5.6.17, for Win32 (x86)
--
-- Host: localhost    Database: coding_interview
-- ------------------------------------------------------
-- Server version	5.6.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `coding_assignment_default`
--

DROP TABLE IF EXISTS `coding_assignment_default`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coding_assignment_default` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coding_assignment_id` int(11) NOT NULL,
  `language` int(11) NOT NULL,
  `initial_code` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_idx` (`coding_assignment_id`),
  KEY `uk_idx` (`coding_assignment_id`,`language`),
  CONSTRAINT `fk_coding_assignment` FOREIGN KEY (`coding_assignment_id`) REFERENCES `coding_assignment` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coding_assignment_default`
--

LOCK TABLES `coding_assignment_default` WRITE;
/*!40000 ALTER TABLE `coding_assignment_default` DISABLE KEYS */;
INSERT INTO `coding_assignment_default` VALUES (1,1,1,'\nusing System;\nusing System.Collections.Generic;\nusing System.Linq;\nusing System.Text.RegularExpressions;\n\nnamespace Rextester\n{\n    public class Program\n    {\n        public static void Main(string[] args)\n        {\n            //Your code goes here\n            Console.WriteLine(\"Hello, world!\");\n        }\n    }\n}\n'),(2,1,5,'\n#Title of this code\n\nprint \"Hello, world!\"\n\n'),(3,1,17,'\n//Title of this code\n\nprint(\"Hello, world!\");\n\n');
/*!40000 ALTER TABLE `coding_assignment_default` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-12-07 23:29:14
