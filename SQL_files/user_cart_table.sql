
CREATE TABLE IF NOT EXISTS `user_cart_table` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_email` varchar(100) NOT NULL,
  `service_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `sc_id` int(11) NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `user_email_idx` (`user_email`),
  KEY `service_id_idx` (`service_id`),
  KEY `sc_id_cart_idx` (`sc_id`),
  CONSTRAINT `fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service_table` (`service_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_email` FOREIGN KEY (`user_email`) REFERENCES `users_table` (`user_email`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `sc_id_cart` FOREIGN KEY (`sc_id`) REFERENCES `sub_category_table` (`sc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `user_cart_table` VALUES (19,'akshat201103@gmail.com',1547,1,25),(20,'akshat201103@gmail.com',1579,1,27),(22,'akshat201103@gmail.com',1280,1,16),(24,'akshat201103@gmail.com',1393,1,21),(25,'akshat201103@gmail.com',1548,1,25);
