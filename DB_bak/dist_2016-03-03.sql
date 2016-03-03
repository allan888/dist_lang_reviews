# ************************************************************
# Sequel Pro SQL dump
# Version 4529
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: s2.zhujieao.com (MySQL 5.5.47-0ubuntu0.14.04.1)
# Database: dist
# Generation Time: 2016-03-03 15:15:20 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table projects
# ------------------------------------------------------------

DROP TABLE IF EXISTS `projects`;

CREATE TABLE `projects` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL DEFAULT '',
  `home_page` varchar(500) DEFAULT NULL,
  `developer` varchar(500) DEFAULT NULL,
  `developer_email` varchar(500) DEFAULT NULL,
  `developer_home_page` varchar(500) DEFAULT NULL,
  `problem` varchar(500) DEFAULT NULL,
  `algorithm` varchar(500) DEFAULT NULL,
  `language` varchar(500) DEFAULT NULL,
  `language_version` varchar(500) DEFAULT NULL,
  `release_date` date DEFAULT NULL,
  `release_version` varchar(500) DEFAULT NULL,
  `platforms` varchar(500) DEFAULT NULL,
  `lines_total` int(11) DEFAULT NULL,
  `lines_pure` int(11) DEFAULT NULL,
  `applications` varchar(500) DEFAULT NULL,
  `additional_information` varchar(1000) DEFAULT NULL,
  `additional_attributes` varchar(1000) DEFAULT NULL,
  `list_on_dist_algo_web_site` tinyint(1) DEFAULT '1',
  `submitter` varchar(500) DEFAULT NULL,
  `submitter_email` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
