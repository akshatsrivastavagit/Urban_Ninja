
CREATE TABLE IF NOT EXISTS `offers_table` (
  `offer_id` int(11) NOT NULL,
  `offer_name` text DEFAULT NULL,
  `min_amt` int(11) DEFAULT NULL,
  `no_of_services` int(11) DEFAULT NULL,
  `offer_condition` bigint(20) DEFAULT NULL,
  `offer_discount` int(11) DEFAULT NULL,
  `offer_description_terms` text DEFAULT NULL,
  PRIMARY KEY (`offer_id`),
  UNIQUE KEY `offer_id_UNIQUE` (`offer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `offers_table` VALUES (111111,'Welcome Offer',0,0,0,20,'This offer is applicable only for new users for first booking'),(111112,'Refer & Earn',0,1,0,10,'Both referrer and referee will get the discount'),(111113,'Summer Special',500,2,0,20,'Valid from June 1 to June 30. New customers only'),(111114,'Winter Special',500,2,0,20,'Valid from 1 December to 30 December. New customers only'),(111115,'Festive Season',800,5,0,25,'This offer is valid only on Diwali week'),(111116,'Weekend Special',700,5,0,15,'Valid on services based on Saturday and Sunday'),(111117,'Loyalty Award',2000,8,0,20,'Valid from 6th booking onwards. Minimum 5 bookings should be there'),(111118,'Early Benefit',1000,5,0,10,'Valid on advance bookings made 7 days prior'),(111119,'Flash Sale',1500,7,0,25,'Valid for 24 hours only on certain days'),(111120,'Anniversary Special',500,9,0,25,'Valid on UrbanClap\'s anniversary date');
