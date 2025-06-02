CREATE TABLE IF NOT EXISTS `technician_booking_table` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `tech_id` int(11) DEFAULT NULL,
  `sc_id` int(11) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `slot_date` date DEFAULT NULL,
  `slot_time` varchar(255) DEFAULT NULL,
  `booking_id` bigint(20) DEFAULT NULL,
  `service_duration` int(11) DEFAULT NULL,
  PRIMARY KEY (`row_id`),
  KEY `tech_id_idx` (`tech_id`),
  KEY `sc_id_idx` (`sc_id`),
  KEY `booking_id_tech_b` (`booking_id`),
  CONSTRAINT `fk_sc_id_tb` FOREIGN KEY (`sc_id`) REFERENCES `sub_category_table` (`sc_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_tech_id_tb` FOREIGN KEY (`tech_id`) REFERENCES `technician_table` (`tech_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `technician_booking_table` VALUES (1,1111190,21,'Jalna','2024-06-25','09:00 - 11:00',1111111111111159,120);
