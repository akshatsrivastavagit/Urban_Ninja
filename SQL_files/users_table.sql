
CREATE TABLE IF NOT EXISTS `users_table` (
  `user_name` varchar(100) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `credits` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_email`),
  UNIQUE KEY `user_email_UNIQUE` (`user_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `users_table` VALUES ('Akshat Srivastava','akshat201103@gmail.com',607),('Akshat` Srivastava','akshatcharig@gmail.com',0),('Akshat Srivastava','akshatgreninja@gmail.com',9986299),('Akshat Srivastava','akshatsrivastavagre@gmail.com',0),('Master','masteremail@gmail.com',0);