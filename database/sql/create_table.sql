DROP DATABASE IF EXISTS zipzup;
CREATE DATABASE zipzup;
USE zipzup;

CREATE TABLE `buildings` (
    `id` BIGINT NOT NULL AUTO_INCREMENT, 
    `building` VARCHAR(32) NOT NULL,
    `dist_origin` VARCHAR(64) NOT NULL,
    `dist_road` VARCHAR(64) NOT NULL, 
    `bunji` VARCHAR(32), 
    `year_build` INT,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`dist_origin`, `dist_road`)
);

CREATE TABLE `districts` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `dist_origin` VARCHAR(64) NOT NULL,
    `dist_join` VARCHAR(64) NOT NULL,
    `sub_dist1` VARCHAR(16) NOT NULL, 
    `sub_dist2` VARCHAR(16) NOT NULL,
    `sub_dist3` VARCHAR(16) NOT NULL,
    `sub_dist4` VARCHAR(16),
    PRIMARY KEY (`id`),
    UNIQUE KEY (`dist_origin`)
);

CREATE TABLE `areas` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `dist_origin` VARCHAR(64) NOT NULL,
    `dist_road` VARCHAR(64) NOT NULL, 
    `area` DOUBLE NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`dist_origin`, `dist_road`, `area`)
);

CREATE TABLE `trades` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `dist_origin` VARCHAR(64) NOT NULL,
    `dist_road` VARCHAR(64) NOT NULL, 
    `bunji` VARCHAR(64), 
    `building` VARCHAR(32) NOT NULL,
    `date_contract` INT NOT NULL, 
    `day_contract` INT NOT NULL, 
    `price` INT NOT NULL, 
    `floor` INT NOT NULL, 
    `area` DOUBLE,

    PRIMARY KEY (`id`),
    UNIQUE KEY (`dist_origin`, `dist_road`, `area`)
);

ALTER TABLE `districts` 
ADD FOREIGN KEY (`dist_origin`) 
REFERENCES `buildings`(`dist_origin`), `trades`(`dist_origin`);

ALTER TABLE `buildings` 
ADD CONSTRAINT `fk_buildings`
FOREIGN KEY (`dist_origin`, `dist_road`) 
REFERENCES `areas`(`dist_origin`, `dist_road`);

