-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Ott 04, 2026 alle 15:51
-- Versione del server: 10.4.32-MariaDB
-- Versione PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_parking`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `parking_spots`
--

CREATE TABLE `parking_spots` (
  `spot_id` varchar(10) NOT NULL,
  `status` enum('FREE','BUSY') DEFAULT 'FREE',
  `spot_type` enum('standard','disabled') DEFAULT 'standard',
  `last_update` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `parking_spots`
--

INSERT INTO `parking_spots` (`spot_id`, `status`, `spot_type`, `last_update`) VALUES
('A-101', 'BUSY', 'standard', '2026-10-04 13:49:03'),
('A-102', 'FREE', 'standard', '2026-10-04 13:49:03'),
('A-107', 'FREE', 'disabled', '2026-10-04 13:49:03'),
('B-116', 'FREE', 'disabled', '2026-10-04 13:49:03');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `parking_spots`
--
ALTER TABLE `parking_spots`
  ADD PRIMARY KEY (`spot_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
