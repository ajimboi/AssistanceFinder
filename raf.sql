-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jul 25, 2023 at 12:25 PM
-- Server version: 8.0.31
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `raf`
--

-- --------------------------------------------------------

--
-- Table structure for table `approval`
--

CREATE TABLE `approval` (
  `request_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `approval`
--

INSERT INTO `approval` (`request_id`, `status`) VALUES
(24, 'accept'),
(26, 'accept');

-- --------------------------------------------------------

--
-- Table structure for table `performance_table`
--

CREATE TABLE `performance_table` (
  `months` date NOT NULL,
  `rating` int NOT NULL,
  `comment` text COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL,
  `project_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `performance_table`
--

INSERT INTO `performance_table` (`months`, `rating`, `comment`, `user_id`, `project_id`) VALUES
('2023-01-01', 1, 'He\'s bad', 1, 20),
('2023-02-01', 5, 'He\'s good!', 1, 20),
('2023-03-01', 4, 'He\'s good!', 1, 20),
('2023-04-01', 5, 'He\'s good!', 1, 20),
('2023-03-01', 3, 'He\'s ok', 1, 20);

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `request_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `request_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `requests`
--

INSERT INTO `requests` (`request_id`, `user_id`, `project_id`, `request_date`) VALUES
(24, 1, 20, '2023-07-06 16:20:25'),
(26, 1, 23, '2023-07-07 15:05:36');

-- --------------------------------------------------------

--
-- Table structure for table `save_project`
--

CREATE TABLE `save_project` (
  `project_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `title_grant` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `duration_grant` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `principal_researcher` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `monthly_allowance` decimal(10,2) DEFAULT NULL,
  `period_start` date DEFAULT NULL,
  `period_end` date DEFAULT NULL,
  `research_domain` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `save_project`
--

INSERT INTO `save_project` (`project_id`, `user_id`, `title_grant`, `duration_grant`, `total_amount`, `principal_researcher`, `monthly_allowance`, `period_start`, `period_end`, `research_domain`) VALUES
(20, 9, 'Red House', '1 Month', '123123.00', 'Akma', '123.00', '2023-07-06', '2023-07-28', 'Computer Science'),
(21, 9, 'Tchalla Ceremony', '24 Months', '21313.00', 'Akma', '123.00', '2023-07-20', '2023-09-25', 'Computer Science'),
(22, 9, 'Majlis LangMira', '24 Months', '123123.00', 'Akma', '12321.00', '2023-07-06', '2023-07-29', 'Computer Science'),
(23, 9, 'Water Quality Monitoring System', '12 Months', '500000.00', 'Akma', '1000.00', '2023-07-01', '2023-07-30', 'Computer Science');

-- --------------------------------------------------------

--
-- Table structure for table `skill_radar`
--

CREATE TABLE `skill_radar` (
  `communication1` int NOT NULL,
  `research_methodology1` int NOT NULL,
  `subject_matter1` int NOT NULL,
  `collaboration1` int NOT NULL,
  `time_management1` int NOT NULL,
  `user_id` int NOT NULL,
  `project_id` int DEFAULT NULL,
  `communication2` int NOT NULL,
  `communication3` int NOT NULL,
  `research_methodology2` int NOT NULL,
  `research_methodology3` int NOT NULL,
  `subject_matter2` int NOT NULL,
  `subject_matter3` int NOT NULL,
  `collaboration2` int NOT NULL,
  `collaboration3` int NOT NULL,
  `time_management2` int NOT NULL,
  `time_management3` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `skill_radar`
--

INSERT INTO `skill_radar` (`communication1`, `research_methodology1`, `subject_matter1`, `collaboration1`, `time_management1`, `user_id`, `project_id`, `communication2`, `communication3`, `research_methodology2`, `research_methodology3`, `subject_matter2`, `subject_matter3`, `collaboration2`, `collaboration3`, `time_management2`, `time_management3`) VALUES
(5, 3, 4, 5, 4, 1, 20, 4, 4, 4, 4, 5, 5, 5, 5, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `role` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL,
  `ic_number` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `gender` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `education_level` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `contact` varchar(255) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`name`, `password`, `email`, `role`, `user_id`, `ic_number`, `gender`, `education_level`, `address`, `contact`) VALUES
('Bon', '1231', 'aiman@yahoo.com', 'Research Assistant', 1, '010130030689', 'Male', 'Degree', 'Perlis', '01126554254'),
('Akma', '5671', 'akma@yahoo.com', 'Researcher', 9, '020230030689', 'Female', 'Reseacher', 'Kolej Gamma, UiTM Perak Tapah, Perak', '01136559803'),
('ayam', 'ayam', 'ayam@gmail.com', 'Research Assistant', 10, '32323123', 'male', 'Degree', 'dsadasdsa', '3232');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `approval`
--
ALTER TABLE `approval`
  ADD PRIMARY KEY (`request_id`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`request_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `project_id` (`project_id`);

--
-- Indexes for table `save_project`
--
ALTER TABLE `save_project`
  ADD PRIMARY KEY (`project_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `request_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `save_project`
--
ALTER TABLE `save_project`
  MODIFY `project_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `approval`
--
ALTER TABLE `approval`
  ADD CONSTRAINT `approval_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `requests` (`request_id`);

--
-- Constraints for table `requests`
--
ALTER TABLE `requests`
  ADD CONSTRAINT `requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `save_project`
--
ALTER TABLE `save_project`
  ADD CONSTRAINT `save_project_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
