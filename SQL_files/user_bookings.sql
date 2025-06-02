

CREATE TABLE IF NOT EXISTS `user_bookings` (
  `booking_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_email` varchar(100) DEFAULT NULL,
  `booking_name` varchar(60) DEFAULT NULL,
  `booked_location` varchar(300) DEFAULT NULL,
  `phone_no` int(11) DEFAULT NULL,
  `booking_date_time` varchar(50) DEFAULT NULL,
  `booked_date` date DEFAULT NULL,
  `booked_time` time DEFAULT NULL,
  `UPI_Ref_No` int(11) DEFAULT NULL,
  `duration` varchar(50) DEFAULT NULL,
  `total_amount` int(11) DEFAULT NULL,
  `offer_id` int(11) DEFAULT NULL,
  `discounted_total` int(11) DEFAULT NULL,
  `credits_used` int(11) DEFAULT 0,
  `sc_id` int(11) DEFAULT NULL,
  `final_amount` int(11) DEFAULT NULL,
  `total_minutes` int(11) DEFAULT NULL,
  `offer_name` varchar(100) DEFAULT NULL,
  `tech_id` int(11) DEFAULT NULL,
  `booking_token` varchar(255) DEFAULT NULL,
  `token_used` tinyint(1) DEFAULT 0,
  `otp` int(11) DEFAULT NULL,
  `booking_status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`booking_id`),
  UNIQUE KEY `booking_id_UNIQUE` (`booking_id`),
  UNIQUE KEY `booking_token` (`booking_token`),
  KEY `user_email_userbooking_idx` (`user_email`),
  KEY `UPI_Ref_No_booking_idx` (`UPI_Ref_No`),
  KEY `sc_id_bookings_idx` (`sc_id`),
  KEY `offer_id_booking_idx` (`offer_id`),
  CONSTRAINT `UPI_Ref_No_booking` FOREIGN KEY (`UPI_Ref_No`) REFERENCES `payments_table` (`UPI_Ref_No`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `offer_id` FOREIGN KEY (`offer_id`) REFERENCES `offers_table` (`offer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sc_id_bookings` FOREIGN KEY (`sc_id`) REFERENCES `sub_category_table` (`sc_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_email_userbooking` FOREIGN KEY (`user_email`) REFERENCES `users_table` (`user_email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1111111111111160 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `user_bookings` VALUES (1111111111111121,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-22 20:53:56','2024-06-23','16:00:00',1425,'3',1357,111111,1086,1086,21,0,210,'Welcome Offer',1111376,NULL,0,NULL,NULL),(1111111111111122,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-22 20:54:55','2024-06-23','16:00:00',1425,'2',758,111111,607,607,21,0,120,'Welcome Offer',1111190,NULL,0,NULL,NULL),(1111111111111123,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-22 21:05:50','2024-06-24','09:00:00',1425,'2',758,111111,607,607,21,0,120,'Welcome Offer',1111190,NULL,0,NULL,NULL),(1111111111111136,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 03:50:51','2024-06-24','16:00:00',1234,'30',98,111111,79,79,21,0,30,'Welcome Offer',1111190,NULL,0,NULL,NULL),(1111111111111137,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 03:56:12','2024-06-24','16:30:00',1425,'1',448,111111,359,359,21,0,75,'Welcome Offer',1111190,NULL,0,NULL,NULL),(1111111111111138,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 04:01:55','2024-06-24','19:00:00',2536,'30',98,111111,79,79,21,0,30,'Welcome Offer',1111376,NULL,0,NULL,NULL),(1111111111111139,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 04:09:55','2024-06-25','09:00:00',1234,'6',2344,111111,1876,1876,21,0,385,'Welcome Offer',1111190,NULL,0,NULL,NULL),(1111111111111140,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 04:15:11','2024-06-25','09:00:00',1425,'3',1097,111111,878,878,21,0,180,'Welcome Offer',1111376,NULL,0,NULL,NULL),(1111111111111141,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 04:36:50','2024-06-25','12:00:00',1425,'6',2454,111111,1964,1964,21,0,390,'Welcome Offer',1111376,NULL,0,NULL,NULL),(1111111111111142,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 04:40:49','2024-06-25','15:30:00',1234,'3',1357,111111,1086,1086,21,0,210,'Welcome Offer',1111190,NULL,0,NULL,NULL),(1111111111111143,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 04:43:46','2024-06-25','18:30:00',2536,'2',807,111111,646,646,21,0,135,'Welcome Offer',1111376,NULL,0,NULL,NULL),(1111111111111144,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 04:48:45','2024-06-24','16:30:00',1425,'2',856,111111,685,685,21,0,150,'Welcome Offer',1111190,NULL,0,NULL,NULL),(1111111111111145,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 04:52:27','2024-06-28','12:30:00',1234,'6',3355,111111,2684,2348,21,336,400,'Welcome Offer',1111190,NULL,0,NULL,NULL),(1111111111111146,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 22:18:19','2024-06-24','09:00:00',8596,'2',758,111111,607,607,21,0,120,'Welcome Offer',1111190,NULL,0,239832,'Completed'),(1111111111111147,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-23 22:53:07','2024-06-24','09:00:00',8495,'6',5273,111111,4219,4219,21,0,360,'Welcome Offer',1111376,NULL,0,915489,'pending'),(1111111111111148,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 02:30:21','2024-06-25','09:00:00',852369,'2',2999,111111,2400,0,22,2400,120,'Welcome Offer',1111190,NULL,0,616986,'Completed'),(1111111111111149,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 02:34:13','2024-06-25','09:00:00',123654,'5',1904,111111,1524,0,21,1524,300,'Welcome Offer',1111376,NULL,0,144042,'Cancelled'),(1111111111111150,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 02:59:33','2024-06-25','11:00:00',2,'6',2274,111111,1820,1524,21,296,360,'Welcome Offer',1111190,NULL,0,853033,'pending'),(1111111111111151,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 03:20:47','2024-06-25','09:00:00',8960,'6 hours 0 minutes',8997,111111,7198,0,22,7198,360,'Welcome Offer',1111190,NULL,0,159607,'pending'),(1111111111111152,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 03:27:26','2024-06-25','09:00:00',3,'2 hours 0 minutes',758,111111,607,0,21,607,120,'Welcome Offer',1111376,NULL,0,152586,'pending'),(1111111111111153,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 03:28:11','2024-06-25','11:00:00',4,'1 hour 0 minutes',349,111111,280,0,21,280,60,'Welcome Offer',1111376,NULL,0,320971,'pending'),(1111111111111154,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 07:30:56','2024-06-25','09:00:00',8,'9 hours 40 minutes',11093,111111,8875,8875,22,0,580,'Welcome Offer',1111190,NULL,0,515750,'pending'),(1111111111111155,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 07:42:27','0000-00-00','00:00:00',11,'2 hours 0 minutes',758,111111,607,0,21,607,120,'Welcome Offer',1111376,NULL,0,152936,'Completed'),(1111111111111156,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 08:00:33','2024-06-25','09:00:00',12,'2 hours 0 minutes',758,111111,607,0,21,607,120,'Welcome Offer',1111376,NULL,0,450315,'Cancelled'),(1111111111111157,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 09:47:51','2024-06-25','11:00:00',13,'2 hours 0 minutes',758,111111,607,0,21,607,120,'Welcome Offer',1111376,NULL,0,143878,'Completed'),(1111111111111158,'akshat201103@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 10:17:56','2024-06-25','13:00:00',15,'2 hours 0 minutes',758,111111,607,0,21,607,120,'Welcome Offer',1111376,NULL,0,135654,'pending'),(1111111111111159,'akshatgreninja@gmail.com',NULL,'Jalna',2147483647,'2024-06-24 12:49:41','2024-06-25','09:00:00',16,'2 hours 0 minutes',758,111111,607,607,21,0,120,'Welcome Offer',1111190,NULL,0,914441,'pending');
