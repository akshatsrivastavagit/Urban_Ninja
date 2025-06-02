
CREATE TABLE  IF NOT EXISTS  `warranty_table` (
  `warranty_id` int(11) NOT NULL AUTO_INCREMENT,
  `warranty_name` varchar(100) NOT NULL,
  `warranty_duration` int(11) NOT NULL,
  `warranty_description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`warranty_id`),
  UNIQUE KEY `warranty_id_UNIQUE` (`warranty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11111117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `warranty_table` VALUES (11111111,'Basic Warranty',30,'Covers basic repairs and maintenance for 30 days on electrical appliances.'),(11111112,'Standard Warranty',45,'Includes extended supoort and parts replacement for 45 days.'),(11111113,'Premium Warranty',60,'Provides comprehensive coverage for 60 days.'),(11111114,'Gold Warranty',90,'Includes priority services and free check-ups(in case of problem) for 90 days.'),(11111115,'Platinum Warranty',120,'Includes free replacement of major parts for 120 days.'),(11111116,'Diamond Warranty',180,'Includes free repairs and replacement of major parts for 180 days.');
