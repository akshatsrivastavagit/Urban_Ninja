
CREATE TABLE IF NOT EXISTS `major_category_table` (
  `mc_id` int(11) NOT NULL AUTO_INCREMENT,
  `mc_name` varchar(100) NOT NULL,
  PRIMARY KEY (`mc_id`),
  UNIQUE KEY `mc_id_UNIQUE` (`mc_id`),
  UNIQUE KEY `mc_name_UNIQUE` (`mc_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



INSERT INTO `major_category_table` VALUES (2,'AC & Appliance Repair'),(3,'Cleaning'),(4,'Electrician, Plumber & Carpenter'),(1,'Men & Women Salon');
