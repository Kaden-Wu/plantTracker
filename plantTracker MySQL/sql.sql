CREATE DATABASE plant_tracker;
USE plant_tracker;

CREATE TABLE plants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    water_hours INT NOT NULL,
    sunlight_hours INT NOT NULL,
    last_watered DATETIME NOT NULL,
    last_rotated DATETIME NOT NULL
);

CREATE TABLE reminders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    time DATETIME NOT NULL,
    message VARCHAR(255) NOT NULL,
    enabled BOOLEAN NOT NULL,
    triggered BOOLEAN NOT NULL
);

SHOW TABLES;