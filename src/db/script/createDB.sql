CREATE TABLE `task` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `interval` int(11) unsigned DEFAULT NULL,
  `last_run_time` timestamp NULL DEFAULT NULL,
  `created` timestamp NULL DEFAULT NULL,
  `url` varchar(1000) DEFAULT NULL,
  `last_run_id` int(10) unsigned NOT NULL DEFAULT '0',
  `roi` varchar(63) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;