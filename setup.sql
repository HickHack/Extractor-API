CREATE DATABASE IF NOT EXISTS extractor_service;
CREATE USER 'django'@'localhost' IDENTIFIED BY '';
USE extractor_service;
GRANT ALL PRIVILEGES ON extractor_service.* TO 'django'@'localhost';
FLUSH PRIVILEGES;