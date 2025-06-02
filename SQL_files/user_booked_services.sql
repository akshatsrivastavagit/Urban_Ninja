

CREATE TABLE IF NOT EXISTS `user_booked_services` (
  `booking_id` bigint(20) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `warranty_duration` int(11) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  KEY `booking_id_booked_idx` (`booking_id`),
  KEY `service_id_booked_idx` (`service_id`),
  CONSTRAINT `booking_id_booked` FOREIGN KEY (`booking_id`) REFERENCES `user_bookings` (`booking_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `service_id_booked` FOREIGN KEY (`service_id`) REFERENCES `service_table` (`service_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `user_booked_services` VALUES (1111111111111159,1393,758,1,758,120,NULL,NULL);
