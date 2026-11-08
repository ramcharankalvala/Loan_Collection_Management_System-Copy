CREATE DATABASE  IF NOT EXISTS `loan_collection_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `loan_collection_db`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: loan_collection_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `collection_cases`
--

DROP TABLE IF EXISTS `collection_cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collection_cases` (
  `case_id` varchar(30) NOT NULL,
  `loan_id` varchar(30) DEFAULT NULL,
  `customer_id` varchar(20) DEFAULT NULL,
  `priority_rank` int DEFAULT NULL,
  `priority_score` int DEFAULT NULL,
  `outstanding` decimal(12,2) DEFAULT NULL,
  `dpd` int DEFAULT NULL,
  `case_status` varchar(30) DEFAULT NULL,
  `action_status` varchar(50) DEFAULT NULL,
  `dispute_status` varchar(50) DEFAULT NULL,
  `hardship_status` varchar(50) DEFAULT NULL,
  `contact_status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`case_id`),
  KEY `loan_id` (`loan_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `collection_cases_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
  CONSTRAINT `collection_cases_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `collection_priority`
--

DROP TABLE IF EXISTS `collection_priority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collection_priority` (
  `priority_rank` int DEFAULT NULL,
  `loan_id` varchar(30) NOT NULL,
  `priority_score` int DEFAULT NULL,
  `outstanding` decimal(12,2) DEFAULT NULL,
  `dpd` int DEFAULT NULL,
  `risk_score` int DEFAULT NULL,
  `balance_score` int DEFAULT NULL,
  `dpd_score` int DEFAULT NULL,
  `hardship_flag` tinyint(1) DEFAULT NULL,
  `dispute_flag` tinyint(1) DEFAULT NULL,
  `contact_restricted` tinyint(1) DEFAULT NULL,
  `dispute_status` varchar(50) DEFAULT NULL,
  `hardship_status` varchar(50) DEFAULT NULL,
  `contact_status` varchar(50) DEFAULT NULL,
  `action_status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`loan_id`),
  CONSTRAINT `collection_priority_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact_attempts`
--

DROP TABLE IF EXISTS `contact_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_attempts` (
  `attempt_id` varchar(50) NOT NULL,
  `case_id` varchar(30) DEFAULT NULL,
  `loan_id` varchar(30) DEFAULT NULL,
  `customer_id` varchar(20) DEFAULT NULL,
  `attempt_datetime` datetime DEFAULT NULL,
  `channel` varchar(20) DEFAULT NULL,
  `outcome` varchar(30) DEFAULT NULL,
  `data_source` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`attempt_id`),
  KEY `case_id` (`case_id`),
  KEY `loan_id` (`loan_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `contact_attempts_ibfk_1` FOREIGN KEY (`case_id`) REFERENCES `collection_cases` (`case_id`),
  CONSTRAINT `contact_attempts_ibfk_2` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
  CONSTRAINT `contact_attempts_ibfk_3` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact_preferences`
--

DROP TABLE IF EXISTS `contact_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_preferences` (
  `customer_id` varchar(20) NOT NULL,
  `phone_allowed` tinyint(1) DEFAULT NULL,
  `sms_allowed` tinyint(1) DEFAULT NULL,
  `email_allowed` tinyint(1) DEFAULT NULL,
  `contact_opt_out` tinyint(1) DEFAULT NULL,
  `allowed_start_time` time DEFAULT NULL,
  `allowed_end_time` time DEFAULT NULL,
  `data_source` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  CONSTRAINT `contact_preferences_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `customer_promise_summary`
--

DROP TABLE IF EXISTS `customer_promise_summary`;
/*!50001 DROP VIEW IF EXISTS `customer_promise_summary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `customer_promise_summary` AS SELECT
 1 AS `customer_id`,
 1 AS `customer_name`,
 1 AS `total_promises`,
 1 AS `total_promised`,
 1 AS `total_paid`,
 1 AS `total_remaining`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` varchar(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `delinquency`
--

DROP TABLE IF EXISTS `delinquency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delinquency` (
  `loan_id` varchar(30) NOT NULL,
  `customer_id` varchar(20) DEFAULT NULL,
  `installment_number` int NOT NULL,
  `due_date` date DEFAULT NULL,
  `emi_amount` decimal(12,2) DEFAULT NULL,
  `amount_paid` decimal(12,2) DEFAULT NULL,
  `outstanding_amount` decimal(12,2) DEFAULT NULL,
  `dpd` int DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`loan_id`,`installment_number`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `delinquency_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
  CONSTRAINT `delinquency_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emi_schedules`
--

DROP TABLE IF EXISTS `emi_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emi_schedules` (
  `loan_id` varchar(30) NOT NULL,
  `customer_id` varchar(20) DEFAULT NULL,
  `month` int NOT NULL,
  `emi` decimal(12,2) DEFAULT NULL,
  `interest` decimal(12,2) DEFAULT NULL,
  `principal_paid` decimal(12,2) DEFAULT NULL,
  `remaining_balance` decimal(12,2) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  PRIMARY KEY (`loan_id`,`month`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `emi_schedules_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
  CONSTRAINT `emi_schedules_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `loan_delinquency_summary`
--

DROP TABLE IF EXISTS `loan_delinquency_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loan_delinquency_summary` (
  `loan_id` varchar(30) NOT NULL,
  `paid_count` int DEFAULT NULL,
  `partial_count` int DEFAULT NULL,
  `missed_count` int DEFAULT NULL,
  `total_emi` decimal(12,2) DEFAULT NULL,
  `total_paid` decimal(12,2) DEFAULT NULL,
  `outstanding` decimal(12,2) DEFAULT NULL,
  `dpd` int DEFAULT NULL,
  PRIMARY KEY (`loan_id`),
  CONSTRAINT `loan_delinquency_summary_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `loan_id` varchar(30) NOT NULL,
  `customer_id` varchar(20) DEFAULT NULL,
  `loan_amount` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`loan_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `payment_id` varchar(30) NOT NULL,
  `loan_id` varchar(30) DEFAULT NULL,
  `customer_id` varchar(20) DEFAULT NULL,
  `installment_number` int DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `emi_amount` decimal(12,2) DEFAULT NULL,
  `amount_paid` decimal(12,2) DEFAULT NULL,
  `unpaid_amount` decimal(12,2) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `loan_id` (`loan_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
  CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `promise_payment_allocations`
--

DROP TABLE IF EXISTS `promise_payment_allocations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promise_payment_allocations` (
  `allocation_id` varchar(30) NOT NULL,
  `promise_id` varchar(30) DEFAULT NULL,
  `payment_id` varchar(30) DEFAULT NULL,
  `allocated_amount` decimal(12,2) DEFAULT NULL,
  `allocation_date` date DEFAULT NULL,
  PRIMARY KEY (`allocation_id`),
  KEY `promise_id` (`promise_id`),
  KEY `payment_id` (`payment_id`),
  CONSTRAINT `promise_payment_allocations_ibfk_1` FOREIGN KEY (`promise_id`) REFERENCES `promises_to_pay` (`promise_id`),
  CONSTRAINT `promise_payment_allocations_ibfk_2` FOREIGN KEY (`payment_id`) REFERENCES `payments` (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `promises_to_pay`
--

DROP TABLE IF EXISTS `promises_to_pay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promises_to_pay` (
  `promise_id` varchar(30) NOT NULL,
  `loan_id` varchar(30) DEFAULT NULL,
  `customer_id` varchar(20) DEFAULT NULL,
  `promise_amount` decimal(12,2) DEFAULT NULL,
  `promise_date` date DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `amount_paid` decimal(12,2) DEFAULT NULL,
  `remaining_amount` decimal(12,2) DEFAULT NULL,
  `promise_status` varchar(30) DEFAULT NULL,
  `review_notes` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`promise_id`),
  KEY `loan_id` (`loan_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `promises_to_pay_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
  CONSTRAINT `promises_to_pay_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `risk_indicators`
--

DROP TABLE IF EXISTS `risk_indicators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `risk_indicators` (
  `loan_id` varchar(30) NOT NULL,
  `missed_installments` int DEFAULT NULL,
  `repeated_payment_failure` tinyint(1) DEFAULT NULL,
  `hardship_flag` tinyint(1) DEFAULT NULL,
  `dispute_flag` tinyint(1) DEFAULT NULL,
  `contact_restricted` tinyint(1) DEFAULT NULL,
  `risk_score` int DEFAULT NULL,
  `data_source` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`loan_id`),
  CONSTRAINT `risk_indicators_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `customer_promise_summary`
--

/*!50001 DROP VIEW IF EXISTS `customer_promise_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 SQL SECURITY INVOKER */
/*!50001 VIEW `customer_promise_summary` AS select `c`.`customer_id` AS `customer_id`,`c`.`name` AS `customer_name`,count(`p`.`promise_id`) AS `total_promises`,sum(`p`.`promise_amount`) AS `total_promised`,sum(`p`.`amount_paid`) AS `total_paid`,sum(`p`.`remaining_amount`) AS `total_remaining` from (`customers` `c` join `promises_to_pay` `p` on((`c`.`customer_id` = `p`.`customer_id`))) group by `c`.`customer_id`,`c`.`name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-08 23:12:29
