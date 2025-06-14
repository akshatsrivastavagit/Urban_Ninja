
CREATE TABLE IF NOT EXISTS  `reviews` (
  `ReviewID` int(11) NOT NULL AUTO_INCREMENT,
  `rating` int(11) DEFAULT NULL,
  `reviewText` varchar(1200) DEFAULT NULL,
  `reviewDate` timestamp NULL DEFAULT current_timestamp(),
  `booking_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`ReviewID`),
  KEY `fk_bk_id_idx` (`booking_id`),
  CONSTRAINT `fk_bk_id` FOREIGN KEY (`booking_id`) REFERENCES `user_bookings` (`booking_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reviews_chk_1` CHECK (`rating` >= 1 and `rating` <= 5)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `reviews` VALUES (30,4,'ver good service provided','2024-06-23 16:48:19',1111111111111146),(31,NULL,NULL,'2024-06-23 17:23:07',1111111111111147),(32,4,'acaw','2024-06-23 21:00:21',1111111111111148),(33,NULL,NULL,'2024-06-23 21:04:13',1111111111111149),(34,NULL,NULL,'2024-06-23 21:29:33',1111111111111150),(35,NULL,NULL,'2024-06-23 21:50:47',1111111111111151),(36,NULL,NULL,'2024-06-23 21:57:26',1111111111111152),(37,NULL,NULL,'2024-06-23 21:58:11',1111111111111153),(38,NULL,NULL,'2024-06-24 02:00:56',1111111111111154),(39,NULL,NULL,'2024-06-24 02:12:27',1111111111111155),(40,NULL,NULL,'2024-06-24 02:30:33',1111111111111156),(41,NULL,NULL,'2024-06-24 04:17:51',1111111111111157),(42,NULL,NULL,'2024-06-24 04:47:56',1111111111111158);
