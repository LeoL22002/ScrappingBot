CREATE DATABASE marketbot;
USE marketbot;

CREATE TABLE users (
id int primary key,
username varchar(200),
status int
);

CREATE TABLE users_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user INT,
    start DATETIME DEFAULT CURRENT_TIMESTAMP,
    foreign key (user) references users(id)
);

CREATE TABLE vehicles(
id int primary key AUTO_INCREMENT,
description varchar(300),
price double,
url varchar(999)
);

CREATE TABLE users_vehicles(
id int primary key AUTO_INCREMENT,
user int,
vehicle int,
foreign key (user) references users(id),
foreign key (vehicle) references vehicles(id)
);
