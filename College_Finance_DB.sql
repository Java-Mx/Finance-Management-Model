CREATE DATABASE IF NOT EXISTS college_finance_db DEFAULT CHARACTER SET utf8;

USE college_finance_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS monthly_budget (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    month VARCHAR(7) NOT NULL,
    budget FLOAT NOT NULL,
    priority1 VARCHAR(100),
    priority1_percent INT,
    priority2 VARCHAR(100),
    priority2_percent INT,
    priority3 VARCHAR(100),
    priority3_percent INT,
    miscellaneous_percent INT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS bill_splits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    bill_amount FLOAT NOT NULL,
    num_people INT NOT NULL,
    per_person_share FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tax_calculations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    income FLOAT NOT NULL,
    tax FLOAT NOT NULL,
    effective_rate FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS compound_interest_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    principal FLOAT NOT NULL,
    monthly_contrib FLOAT NOT NULL,
    years FLOAT NOT NULL,
    annual_rate FLOAT NOT NULL,
    variance FLOAT NOT NULL,
    frequency ENUM('annual','quarterly','monthly'),
    final_amount FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS currency_conversions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    from_currency VARCHAR(3) NOT NULL,
    to_currency VARCHAR(3) NOT NULL,
    amount FLOAT NOT NULL,
    converted_amount FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS savings_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    monthly_saving FLOAT NOT NULL,
    years FLOAT NOT NULL,
    annual_return FLOAT NOT NULL,
    final_balance FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('income','expense'),
    amount FLOAT NOT NULL,
    tag VARCHAR(100) NOT NULL,
    entry_time DATETIME NOT NULL
) ENGINE=InnoDB;
