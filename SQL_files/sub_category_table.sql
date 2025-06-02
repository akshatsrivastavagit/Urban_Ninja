
CREATE TABLE IF NOT EXISTS  `sub_category_table` (
  `sc_id` int(11) NOT NULL AUTO_INCREMENT,
  `sc_name` varchar(100) NOT NULL,
  `mc_id` int(11) NOT NULL,
  PRIMARY KEY (`sc_id`),
  UNIQUE KEY `sc_id_UNIQUE` (`sc_id`),
  UNIQUE KEY `sc_name_UNIQUE` (`sc_name`),
  KEY `mc_id_idx` (`mc_id`),
  CONSTRAINT `fk_mc_id` FOREIGN KEY (`mc_id`) REFERENCES `major_category_table` (`mc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT=' ';

INSERT INTO `sub_category_table` VALUES (11,'Electrician',4),(12,'Plumber',4),(13,'Carpenter',4),(15,'AC Repair & Service',2),(16,'Chimney Repair',2),(17,'Microwave Repair',2),(18,'Refrigerator Repair',2),(19,'Water Purifier',2),(20,'Washing Machine Repair',2),(21,'Bathroom & Kitchen Cleaning',3),(22,'Full Home Cleaning',3),(23,'Sofa & Carpet Cleaning',3),(24,'Hair',1),(25,'Massage',1),(26,'Facial',1),(27,'Grooming',1);
