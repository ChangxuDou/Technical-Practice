-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema schools
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema schools
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `schools` DEFAULT CHARACTER SET utf8 ;
USE `schools` ;

-- -----------------------------------------------------
-- Table `schools`.`students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schools`.`students` (
  `student_id` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `date_registered` DATETIME NOT NULL,
  PRIMARY KEY (`student_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `schools`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schools`.`courses` (
  `course_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `price` DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (`course_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `schools`.`enrollment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schools`.`enrollment` (
  `student_id` INT NOT NULL,
  `course_id` INT NOT NULL,
  `date` DATETIME NOT NULL,
  `price` DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (`student_id`, `course_id`),
  INDEX `fk_enrollment_courses_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_enrollment_students`
    FOREIGN KEY (`student_id`)
    REFERENCES `schools`.`students` (`student_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_enrollment_courses`
    FOREIGN KEY (`course_id`)
    REFERENCES `schools`.`courses` (`course_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `schools`.`instructors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schools`.`instructors` (
  `instructor_id` SMALLINT NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`instructor_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `schools`.`course_Instructor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schools`.`course_Instructor` (
  `course_id` INT NOT NULL,
  `instructor_id` SMALLINT NOT NULL,
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NOT NULL,
  `role` VARCHAR(50) NOT NULL,
  INDEX `fk_Course_Instructor_instructors1_idx` (`instructor_id` ASC) VISIBLE,
  PRIMARY KEY (`course_id`, `instructor_id`),
  CONSTRAINT `fk_course_Instructor_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `schools`.`courses` (`course_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_course_Instructor_instructors1`
    FOREIGN KEY (`instructor_id`)
    REFERENCES `schools`.`instructors` (`instructor_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `schools`.`tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schools`.`tags` (
  `tag_id` TINYINT NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`tag_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `schools`.`course_tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schools`.`course_tags` (
  `course_id` INT NOT NULL,
  `tag_id` TINYINT NOT NULL,
  PRIMARY KEY (`course_id`, `tag_id`),
  INDEX `fk_course_tags_courses1_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_course_tags_tags1`
    FOREIGN KEY (`tag_id`)
    REFERENCES `schools`.`tags` (`tag_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_course_tags_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `schools`.`courses` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
