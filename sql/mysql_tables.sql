SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `measurers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL COMMENT 'Measurer unique code',
  `name` varchar(100) NOT NULL COMMENT 'Weather measurer name',
  `description` text COMMENT 'Weather measurer description',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

CREATE TABLE IF NOT EXISTS `weather` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `measurer_id` int(10) unsigned NOT NULL,
  `temperature` decimal(4,2) NOT NULL COMMENT 'Temperature in celcius',
  `humidity` decimal(5,2) NOT NULL COMMENT 'Humidity in percents',
  `measure_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Measure date and time',
  PRIMARY KEY (`id`),
  KEY `measure_date` (`measure_date`),
  KEY `measurer_id` (`measurer_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;


ALTER TABLE `weather`
ADD CONSTRAINT `weather_ibfk_1` FOREIGN KEY (`measurer_id`) REFERENCES `measurers` (`id`) ON UPDATE CASCADE;
