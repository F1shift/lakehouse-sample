CREATE DATABASE sample_db;

USE sample_db;

CREATE TABLE IF NOT EXISTS shop  (
    id VARCHAR(7) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

INSERT INTO shop (id, name)
VALUES ("0123456", "店舗1");