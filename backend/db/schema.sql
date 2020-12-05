-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema appli_maintenance
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema appli_maintenance
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `appli_maintenance` DEFAULT CHARACTER SET utf8 ;
USE `appli_maintenance` ;

-- -----------------------------------------------------
-- Table `appli_maintenance`.`poste`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`poste` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `start` TIME NOT NULL,
  `end` TIME NOT NULL,
  `porder` SMALLINT NOT NULL,
  `season_start` DATE NOT NULL,
  `season_end` DATE NOT NULL,
  `break_minutes` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`role` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`stade`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`stade` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `img_url` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`section`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`section` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`equipment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`equipment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `section_id` INT NOT NULL,
  `stade_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `equipment_section_idx` (`section_id` ASC),
  INDEX `equipment_stade_idx` (`stade_id` ASC),
  CONSTRAINT `equipment_section`
    FOREIGN KEY (`section_id`)
    REFERENCES `appli_maintenance`.`section` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `equipment_stade`
    FOREIGN KEY (`stade_id`)
    REFERENCES `appli_maintenance`.`stade` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NULL,
  `role_id` INT NULL,
  `stade_id` INT NULL,
  `section_id` INT NULL,
  `photo_file_name` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  INDEX `user_role_idx` (`role_id` ASC),
  INDEX `user_stade_idx` (`stade_id` ASC),
  INDEX `user_section_idx` (`section_id` ASC),
  CONSTRAINT `user_role`
    FOREIGN KEY (`role_id`)
    REFERENCES `appli_maintenance`.`role` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_stade`
    FOREIGN KEY (`stade_id`)
    REFERENCES `appli_maintenance`.`stade` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_section`
    FOREIGN KEY (`section_id`)
    REFERENCES `appli_maintenance`.`section` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`action`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`action` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `equipment_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `action_equipment_idx` (`equipment_id` ASC),
  CONSTRAINT `action_equipment`
    FOREIGN KEY (`equipment_id`)
    REFERENCES `appli_maintenance`.`equipment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`document`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`document` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `link` VARCHAR(255) NULL,
  `title` VARCHAR(45) NULL,
  `description` TEXT NULL,
  `mime_type` VARCHAR(255) NULL,
  `equipment_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `document_equipment_idx` (`equipment_id` ASC),
  CONSTRAINT `document_equipment`
    FOREIGN KEY (`equipment_id`)
    REFERENCES `appli_maintenance`.`equipment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`ot`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`ot` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `team_lead_id` INT NULL,
  `stade_id` INT NULL,
  `section_id` INT NULL,
  `equipment_id` INT NULL,
  `work_status` INT NULL,
  `priority` INT NULL,
  `maintenance_type` INT NULL,
  `action_id` INT NULL,
  `type_arret` INT NULL,
  `scheduled_date` DATE NULL,
  `uo_estimated` INT NULL,
  `uo_actual` INT NULL,
  `status` INT NULL,
  `start` DATETIME NULL,
  `end` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `ot_team_lead_idx` (`team_lead_id` ASC),
  INDEX `ot_stade_idx` (`stade_id` ASC),
  INDEX `ot_section_idx` (`section_id` ASC),
  INDEX `ot_equipment_idx` (`equipment_id` ASC),
  INDEX `ot_action_idx` (`action_id` ASC),
  CONSTRAINT `ot_team_lead`
    FOREIGN KEY (`team_lead_id`)
    REFERENCES `appli_maintenance`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ot_stade`
    FOREIGN KEY (`stade_id`)
    REFERENCES `appli_maintenance`.`stade` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ot_section`
    FOREIGN KEY (`section_id`)
    REFERENCES `appli_maintenance`.`section` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ot_equipment`
    FOREIGN KEY (`equipment_id`)
    REFERENCES `appli_maintenance`.`equipment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ot_action`
    FOREIGN KEY (`action_id`)
    REFERENCES `appli_maintenance`.`action` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`ot_event`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`ot_event` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ot_id` INT NULL,
  `timestamp` DATETIME NULL,
  `key` VARCHAR(45) NULL,
  `value` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  INDEX `ot_event_ot_idx` (`ot_id` ASC),
  CONSTRAINT `ot_event_ot`
    FOREIGN KEY (`ot_id`)
    REFERENCES `appli_maintenance`.`ot` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`pause`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`pause` (
  `ot_id` INT NOT NULL,
  `start` DATETIME NOT NULL,
  `stop` DATETIME NULL,
  PRIMARY KEY (`ot_id`, `start`),
  CONSTRAINT `pause_ot`
    FOREIGN KEY (`ot_id`)
    REFERENCES `appli_maintenance`.`ot` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`ot_operator`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`ot_operator` (
  `ot_id` INT NOT NULL,
  `operator_id` INT NOT NULL,
  `team_lead_id` INT NOT NULL,
  PRIMARY KEY (`ot_id`, `team_lead_id`, `operator_id`),
  INDEX `operator_ot_operator_idx` (`operator_id` ASC),
  INDEX `operator_ot_team_lead_idx` (`team_lead_id` ASC),
  CONSTRAINT `ot_operator_ot`
    FOREIGN KEY (`ot_id`)
    REFERENCES `appli_maintenance`.`ot` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ot_operator_operator`
    FOREIGN KEY (`operator_id`)
    REFERENCES `appli_maintenance`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ot_operator_team_lead`
    FOREIGN KEY (`team_lead_id`)
    REFERENCES `appli_maintenance`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`ot_team_lead`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`ot_team_lead` (
  `ot_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  PRIMARY KEY (`ot_id`, `user_id`, `timestamp`),
  INDEX `ot_team_lead_user_idx` (`user_id` ASC),
  CONSTRAINT `ot_team_lead_ot`
    FOREIGN KEY (`ot_id`)
    REFERENCES `appli_maintenance`.`ot` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ot_team_lead_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `appli_maintenance`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`action_document`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`action_document` (
  `action_id` INT NOT NULL,
  `document_id` INT NOT NULL,
  PRIMARY KEY (`action_id`, `document_id`),
  INDEX `action_document_document_idx` (`document_id` ASC),
  CONSTRAINT `action_document_action`
    FOREIGN KEY (`action_id`)
    REFERENCES `appli_maintenance`.`action` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `action_document_document`
    FOREIGN KEY (`document_id`)
    REFERENCES `appli_maintenance`.`document` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`comment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `ot_id` INT NOT NULL,
  `text` TEXT NULL,
  `date` DATETIME NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `comment_ot_idx` (`ot_id` ASC),
  INDEX `comment_user_idx` (`user_id` ASC),
  CONSTRAINT `comment_ot`
    FOREIGN KEY (`ot_id`)
    REFERENCES `appli_maintenance`.`ot` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `comment_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `appli_maintenance`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `appli_maintenance`.`stade_section`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appli_maintenance`.`stade_section` (
  `stade_id` INT NOT NULL,
  `section_id` INT NOT NULL,
  PRIMARY KEY (`stade_id`, `section_id`),
  INDEX `stade_section_section_idx` (`section_id` ASC),
  CONSTRAINT `stade_section_stade`
    FOREIGN KEY (`stade_id`)
    REFERENCES `appli_maintenance`.`stade` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `stade_section_section`
    FOREIGN KEY (`section_id`)
    REFERENCES `appli_maintenance`.`section` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
