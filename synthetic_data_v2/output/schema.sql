CREATE DATABASE IF NOT EXISTS `loan_collection_synthetic`;
USE `loan_collection_synthetic`;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `ground_truth`;
DROP TABLE IF EXISTS `promises_to_pay`;
DROP TABLE IF EXISTS `contact_attempts`;
DROP TABLE IF EXISTS `risk_indicators`;
DROP TABLE IF EXISTS `collection_cases`;
DROP TABLE IF EXISTS `delinquency_snapshots`;
DROP TABLE IF EXISTS `payments`;
DROP TABLE IF EXISTS `contact_preferences`;
DROP TABLE IF EXISTS `installments`;
DROP TABLE IF EXISTS `loans`;
DROP TABLE IF EXISTS `accounts`;
DROP TABLE IF EXISTS `customers`;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `customers` (
    `customer_id` VARCHAR(40) NOT NULL,
    `name` VARCHAR(150) NULL,
    `email` VARCHAR(255) NULL,
    `city` VARCHAR(100) NULL,
    `phone` VARCHAR(30) NULL,
    PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `accounts` (
    `account_id` VARCHAR(40) NOT NULL,
    `customer_id` VARCHAR(40) NULL,
    `account_status` VARCHAR(40) NULL,
    `opened_date` DATE NULL,
    `closed_date` DATE NULL,
    PRIMARY KEY (`account_id`),
    CONSTRAINT `fk_accounts_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `loans` (
    `loan_id` VARCHAR(40) NOT NULL,
    `account_id` VARCHAR(40) NULL,
    `customer_id` VARCHAR(40) NULL,
    `loan_amount` DECIMAL(14,2) NULL,
    `annual_interest_rate` DECIMAL(7,4) NULL,
    `loan_date` DATE NULL,
    `maturity_date` DATE NULL,
    PRIMARY KEY (`loan_id`),
    CONSTRAINT `fk_loans_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`),
    CONSTRAINT `fk_loans_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `installments` (
    `installment_id` VARCHAR(80) NOT NULL,
    `loan_id` VARCHAR(40) NULL,
    `customer_id` VARCHAR(40) NULL,
    `installment_number` INT NULL,
    `due_date` DATE NULL,
    `installment_amount` DECIMAL(14,2) NULL,
    PRIMARY KEY (`installment_id`),
    CONSTRAINT `fk_installments_loan_id` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
    CONSTRAINT `fk_installments_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `contact_preferences` (
    `customer_id` VARCHAR(40) NOT NULL,
    `phone_allowed` BOOLEAN NULL,
    `sms_allowed` BOOLEAN NULL,
    `email_allowed` BOOLEAN NULL,
    `contact_opt_out` BOOLEAN NULL,
    `allowed_start_time` TIME NULL,
    `allowed_end_time` TIME NULL,
    PRIMARY KEY (`customer_id`),
    CONSTRAINT `fk_contact_preferences_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `payments` (
    `payment_id` VARCHAR(40) NOT NULL,
    `loan_id` VARCHAR(40) NULL,
    `customer_id` VARCHAR(40) NULL,
    `installment_id` VARCHAR(80) NULL,
    `installment_number` INT NULL,
    `payment_date` DATE NULL,
    `amount_due` DECIMAL(14,2) NULL,
    `amount_paid` DECIMAL(14,2) NULL,
    `payment_status` VARCHAR(40) NULL,
    PRIMARY KEY (`payment_id`),
    CONSTRAINT `fk_payments_loan_id` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
    CONSTRAINT `fk_payments_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
    CONSTRAINT `fk_payments_installment_id` FOREIGN KEY (`installment_id`) REFERENCES `installments` (`installment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `delinquency_snapshots` (
    `snapshot_id` VARCHAR(40) NOT NULL,
    `loan_id` VARCHAR(40) NULL,
    `installment_id` VARCHAR(80) NULL,
    `as_of_date` DATE NULL,
    `due_date` DATE NULL,
    `amount_due` DECIMAL(14,2) NULL,
    `amount_paid` DECIMAL(14,2) NULL,
    `outstanding_amount` DECIMAL(14,2) NULL,
    `days_past_due` INT NULL,
    `installment_status` VARCHAR(40) NULL,
    PRIMARY KEY (`snapshot_id`),
    CONSTRAINT `fk_delinquency_snapshots_loan_id` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
    CONSTRAINT `fk_delinquency_snapshots_installment_id` FOREIGN KEY (`installment_id`) REFERENCES `installments` (`installment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `collection_cases` (
    `case_id` VARCHAR(40) NOT NULL,
    `loan_id` VARCHAR(40) NULL,
    `account_id` VARCHAR(40) NULL,
    `customer_id` VARCHAR(40) NULL,
    `outstanding` DECIMAL(14,2) NULL,
    `days_past_due` INT NULL,
    `risk_score` INT NULL,
    `priority_score` INT NULL,
    `priority_rank` INT NULL,
    `case_status` VARCHAR(50) NULL,
    `action_status` VARCHAR(60) NULL,
    `dispute_status` VARCHAR(50) NULL,
    `hardship_status` VARCHAR(50) NULL,
    `contact_status` VARCHAR(50) NULL,
    PRIMARY KEY (`case_id`),
    CONSTRAINT `fk_collection_cases_loan_id` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
    CONSTRAINT `fk_collection_cases_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`),
    CONSTRAINT `fk_collection_cases_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `risk_indicators` (
    `loan_id` VARCHAR(40) NOT NULL,
    `missed_installments` INT NULL,
    `days_past_due` INT NULL,
    `hardship_flag` BOOLEAN NULL,
    `dispute_flag` BOOLEAN NULL,
    `contact_restricted` BOOLEAN NULL,
    `risk_score` INT NULL,
    PRIMARY KEY (`loan_id`),
    CONSTRAINT `fk_risk_indicators_loan_id` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `contact_attempts` (
    `attempt_id` VARCHAR(80) NOT NULL,
    `case_id` VARCHAR(40) NULL,
    `loan_id` VARCHAR(40) NULL,
    `customer_id` VARCHAR(40) NULL,
    `attempt_datetime` DATETIME NULL,
    `channel` VARCHAR(40) NULL,
    `outcome` VARCHAR(60) NULL,
    `within_allowed_window` BOOLEAN NULL,
    PRIMARY KEY (`attempt_id`),
    CONSTRAINT `fk_contact_attempts_case_id` FOREIGN KEY (`case_id`) REFERENCES `collection_cases` (`case_id`),
    CONSTRAINT `fk_contact_attempts_loan_id` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
    CONSTRAINT `fk_contact_attempts_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `promises_to_pay` (
    `promise_id` VARCHAR(40) NOT NULL,
    `case_id` VARCHAR(40) NULL,
    `loan_id` VARCHAR(40) NULL,
    `customer_id` VARCHAR(40) NULL,
    `promise_amount` DECIMAL(14,2) NULL,
    `created_date` DATE NULL,
    `promise_date` DATE NULL,
    `amount_paid` DECIMAL(14,2) NULL,
    `remaining_amount` DECIMAL(14,2) NULL,
    `promise_status` VARCHAR(40) NULL,
    PRIMARY KEY (`promise_id`),
    CONSTRAINT `fk_promises_to_pay_case_id` FOREIGN KEY (`case_id`) REFERENCES `collection_cases` (`case_id`),
    CONSTRAINT `fk_promises_to_pay_loan_id` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`loan_id`),
    CONSTRAINT `fk_promises_to_pay_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ground_truth` (
    `record_id` VARCHAR(100) NOT NULL,
    `entity` VARCHAR(60) NULL,
    `anomaly_type` VARCHAR(100) NULL,
    `expected_decision` VARCHAR(100) NULL,
    PRIMARY KEY (`record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
