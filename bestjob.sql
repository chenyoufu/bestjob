
CREATE DATABASE IF NOT EXISTS `bestjob` DEFAULT CHARACTER SET utf8;

USE `bestjob`;

DROP TABLE IF EXISTS `jobs`;

CREATE TABLE `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `salary_min` int(11) DEFAULT NULL,
  `salary_max` int(11) DEFAULT NULL,
  `salary_avg` float(11,1) DEFAULT NULL,
  `salary` varchar(255) DEFAULT NULL,
  `create_time` date DEFAULT NULL,
  `company_id` varchar(20) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `position_id` bigint(20) DEFAULT NULL,
  `position_name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `source` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id_idx` (`company_id`) USING BTREE,
  KEY `position_id_idx` (`position_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=29271 DEFAULT CHARSET=utf8;

