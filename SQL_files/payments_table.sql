CREATE TABLE IF NOT EXISTS  `payments_table` (
  `UPI_Ref_No` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `consumed` int(11) NOT NULL,
  `user_email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`UPI_Ref_No`),
  UNIQUE KEY `UPI_Ref_No_UNIQUE` (`UPI_Ref_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `payments_table` VALUES (1,0,0,NULL),(2,296,1,NULL),(3,607,1,NULL),(4,280,1,NULL),(8,0,1,NULL),(9,8495,0,NULL),(10,2400,0,NULL),(11,607,1,NULL),(12,607,1,NULL),(13,607,1,NULL),(15,607,1,NULL),(296,9632,0,NULL),(1010,0,0,NULL),(1234,336,1,'akshatgreninja@gmail.com'),(1425,0,1,'akshatgreninja@gmail.com'),(1526,0,0,NULL),(2536,0,0,'akshatgreninja@gmail.com'),(5962,0,0,NULL),(7410,2400,0,NULL),(8495,0,1,NULL),(8596,0,1,NULL),(8960,7198,1,NULL),(9632,0,0,'akshatgreninja@gmail.com'),(123654,1524,1,NULL),(852369,2400,1,NULL);
