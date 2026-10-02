-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Vidly
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Vidly
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Vidly` DEFAULT CHARACTER SET utf8 ;
USE `Vidly` ;

-- -----------------------------------------------------
-- Table `Vidly`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`users` (
  `user_id` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `phone` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `status` TINYINT NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`rental_rate`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`rental_rate` (
  `rental_rate_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `rate` DECIMAL(6,2) NOT NULL,
  PRIMARY KEY (`rental_rate_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`lost_rate`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`lost_rate` (
  `lost_rate_id` INT NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `rate` DECIMAL(5,2) ZEROFILL NOT NULL,
  PRIMARY KEY (`lost_rate_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`movies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`movies` (
  `movie_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `status` TINYINT NOT NULL,
  `total_quantity` SMALLINT NOT NULL DEFAULT 0,
  `available_quantity` SMALLINT NOT NULL DEFAULT 0,
  `product_year` YEAR NOT NULL,
  `barcode` CHAR(10) NOT NULL,
  `creat_time` DATETIME NOT NULL,
  `rental_rate_id` INT NOT NULL,
  `lost_rate_id` INT NOT NULL,
  PRIMARY KEY (`movie_id`),
  INDEX `fk_movies_rental_rate1_idx` (`rental_rate_id` ASC) VISIBLE,
  INDEX `fk_movies_lost_rate1_idx` (`lost_rate_id` ASC) VISIBLE,
  CONSTRAINT `fk_movies_rental_rate1`
    FOREIGN KEY (`rental_rate_id`)
    REFERENCES `Vidly`.`rental_rate` (`rental_rate_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_lost_rate1`
    FOREIGN KEY (`lost_rate_id`)
    REFERENCES `Vidly`.`lost_rate` (`lost_rate_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`customers` (
  `customer_id` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `status` TINYINT NOT NULL,
  `phone` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `points` INT NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL DEFAULT 0,
  `deposit` VARCHAR(45) NOT NULL,
  `creat_time` DATETIME NOT NULL,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`rent_record`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`rent_record` (
  `record_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `rent_time` DATETIME NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`record_id`),
  INDEX `fk_rent_record_customers1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_rent_record_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_rent_record_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `Vidly`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rent_record_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Vidly`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`return_record`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`return_record` (
  `record_id` INT NOT NULL,
  `date_time` DATETIME NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `user_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `return_time` DATETIME NOT NULL,
  `amount` DECIMAL(6,2) NOT NULL,
  PRIMARY KEY (`record_id`),
  INDEX `fk_return_record_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_return_record_customers1_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_return_record_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Vidly`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_return_record_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `Vidly`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`rent_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`rent_items` (
  `item_id` INT NOT NULL,
  `rent_record_id` INT NOT NULL,
  `movie_id` INT NOT NULL,
  `quantity` SMALLINT NOT NULL,
  `daily_rate` DECIMAL(6,2) NOT NULL,
  INDEX `fk_rent_record_items_rent_record_idx` (`rent_record_id` ASC) VISIBLE,
  PRIMARY KEY (`item_id`),
  INDEX `fk_record_items_movies1_idx` (`movie_id` ASC) VISIBLE,
  CONSTRAINT `fk_rent_record_items_rent_record`
    FOREIGN KEY (`rent_record_id`)
    REFERENCES `Vidly`.`rent_record` (`record_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_record_items_movies1`
    FOREIGN KEY (`movie_id`)
    REFERENCES `Vidly`.`movies` (`movie_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`return_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`return_items` (
  `item_id` INT NOT NULL,
  `return_record_id` INT NOT NULL,
  `quantity` SMALLINT NOT NULL,
  `rent_items_item_id` INT NOT NULL,
  `charged_amount` DECIMAL(6,2) NOT NULL,
  INDEX `fk_return_record_items_return_record1_idx` (`return_record_id` ASC) VISIBLE,
  PRIMARY KEY (`item_id`),
  INDEX `fk_return_items_rent_items1_idx` (`rent_items_item_id` ASC) VISIBLE,
  CONSTRAINT `fk_return_record_items_return_record1`
    FOREIGN KEY (`return_record_id`)
    REFERENCES `Vidly`.`return_record` (`record_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_return_items_rent_items1`
    FOREIGN KEY (`rent_items_item_id`)
    REFERENCES `Vidly`.`rent_items` (`item_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`coupons`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`coupons` (
  `coupon_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `status` TINYINT NOT NULL,
  `crea_time` DATETIME NOT NULL,
  `operator` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`coupon_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`customer_coupons`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`customer_coupons` (
  `customer_coupon_id` INT NOT NULL,
  `status` TINYINT NOT NULL,
  `quantity` SMALLINT NOT NULL,
  `customer_id` INT NOT NULL,
  `coupon_id` INT NOT NULL,
  `claim_time` DATETIME NOT NULL,
  `return_record_id` INT NULL DEFAULT NULL,
  INDEX `fk_customer_coupons_customers1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_customer_coupons_conpons1_idx` (`coupon_id` ASC) VISIBLE,
  INDEX `fk_customer_coupons_return_record1_idx` (`return_record_id` ASC) VISIBLE,
  PRIMARY KEY (`customer_coupon_id`),
  CONSTRAINT `fk_customer_coupons_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `Vidly`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_customer_coupons_conpons1`
    FOREIGN KEY (`coupon_id`)
    REFERENCES `Vidly`.`coupons` (`coupon_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_customer_coupons_return_record1`
    FOREIGN KEY (`return_record_id`)
    REFERENCES `Vidly`.`return_record` (`record_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`roles` (
  `role_id` INT NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(45) NULL DEFAULT 'null',
  PRIMARY KEY (`role_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`user_roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`user_roles` (
  `user_id` INT NOT NULL,
  `role_id` INT NOT NULL,
  `creat_time` DATETIME NOT NULL,
  `operator` VARCHAR(50) NOT NULL,
  INDEX `fk_table1_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_table1_roles1_idx` (`role_id` ASC) VISIBLE,
  CONSTRAINT `fk_table1_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Vidly`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table1_roles1`
    FOREIGN KEY (`role_id`)
    REFERENCES `Vidly`.`roles` (`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`operation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`operation` (
  `operation_id` INT NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`operation_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`roles_operations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`roles_operations` (
  `role_id` INT NOT NULL,
  `operation_id` INT NOT NULL,
  `creat_time` DATETIME NOT NULL,
  `operator` VARCHAR(50) NOT NULL,
  INDEX `fk_roles_operations_roles1_idx` (`role_id` ASC) VISIBLE,
  INDEX `fk_roles_operations_operation1_idx` (`operation_id` ASC) VISIBLE,
  CONSTRAINT `fk_roles_operations_roles1`
    FOREIGN KEY (`role_id`)
    REFERENCES `Vidly`.`roles` (`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_roles_operations_operation1`
    FOREIGN KEY (`operation_id`)
    REFERENCES `Vidly`.`operation` (`operation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`recharge_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`recharge_items` (
  `recharge_id` INT NOT NULL,
  `amount` DECIMAL(5,2) NOT NULL,
  `recharge_type` TINYINT NOT NULL,
  `customer_id` INT NOT NULL,
  `date_time` DATETIME NOT NULL,
  PRIMARY KEY (`recharge_id`),
  INDEX `fk_recharge_items_customers1_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_recharge_items_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `Vidly`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Vidly`.`refund_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vidly`.`refund_items` (
  `refund_id` INT NOT NULL,
  `amount` DECIMAL(5,2) NOT NULL,
  `refund_type` TINYINT NOT NULL,
  `customer_id` INT NOT NULL,
  `date_time` DATETIME NOT NULL,
  PRIMARY KEY (`refund_id`),
  INDEX `fk_refund_items_customers1_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_refund_items_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `Vidly`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
