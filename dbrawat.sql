-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 31 Bulan Mei 2018 pada 08.12
-- Versi server: 10.1.32-MariaDB
-- Versi PHP: 7.2.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbrawat`
--

DELIMITER $$
--
-- Prosedur
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_ambilPasienID` (IN `id` VARCHAR(20))  BEGIN
select * from pasien where kd_pasien = id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createAdmin` (IN `name` VARCHAR(50), IN `username` VARCHAR(12), IN `user_password` VARCHAR(255), IN `id` VARCHAR(6))  BEGIN
    if ( select exists (select * from admin where user_name = username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into admin
        (
            kd_petugas,
            nama_petugas,
            user_name,
            user_password
        )
        values
        (
            id,
            name,
            username,
            user_password
        );
     
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deletePasien` (IN `id` VARCHAR(20))  BEGIN
	delete from pasien where kd_pasien = id;
end$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_editPasien` (IN `nama` VARCHAR(100), IN `kode` VARCHAR(6), IN `jenis_kel` VARCHAR(10), IN `alamat1` VARCHAR(100), IN `umur1` VARCHAR(5), IN `user_data` VARCHAR(20))  BEGIN
	update pasien set nama_pasien=nama,jenis_kelamin=jenis_kel,alamat=alamat1,umur=umur1,admin=user_data where kd_pasien=kode;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getAllData` ()  BEGIN
	select * from pasien;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_tambahPasien` (IN `kode` VARCHAR(20), IN `nama` VARCHAR(100), IN `j_Kelamin` VARCHAR(20), IN `alamat` VARCHAR(100), IN `umur` VARCHAR(5), IN `user` VARCHAR(20))  BEGIN
    if ( select exists (select * from pasien where kd_pasien = kode) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into pasien
        (
            kd_pasien,
            nama_pasien,
            jenis_kelamin,
            alamat,
            umur,
            admin
        )
        values
        (
            kode,
            nama,
            j_kelamin,
            alamat,
            umur,
            user
        );		
     
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin` (IN `username` VARCHAR(20))  BEGIN
    select * from admin where user_name = username;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `kd_petugas` varchar(6) NOT NULL,
  `nama_petugas` varchar(50) DEFAULT NULL,
  `user_name` varchar(12) DEFAULT NULL,
  `user_password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`kd_petugas`, `nama_petugas`, `user_name`, `user_password`) VALUES
('30JGE1', 'aria@gmail.com', 'ariaelhamidy', 'pbkdf2:s'),
('5KBKZN', 'Langit', 'langit_7', 'langit07'),
('ADJKHL', 'Cahaya', 'cahaya_04', 'cahaya04'),
('CCOT91', 'Bintang', 'bintang_12', 'binbin12'),
('HZRXRP', 'gantangss', 'gan', 'pbkdf2:sha256:50000$Xd3v35Tk$d299cd06eb00b654796c916511f9bd4afad2ce04c51eb59901075ef229040c05'),
('LZDXBN', 'haha', 'haha', 'pbkdf2:sha256:50000$NOnDaaOn$629790bc2d5a5870070193e07c8e499f322fc2f6680cf9d2f18eb630eff359a7'),
('M549U6', 'Guntur', 'guntur_14', 'gunt1414'),
('Q24S0A', 'ganteng sekali', 'ganteng123', 'pbkdf2:s'),
('TESFIK', 'Bulan', 'bulan_15', 'bulann15'),
('TU1WSB', 'nuria elhamidy', 'nuria', 'pbkdf2:sha256:50000$DIWkJBtt$232e6429f7829d390f82587663681df1554346a5c85610965bebf9d563614b3d'),
('VICQP0', 'ganteng123', 'ganteng', 'pbkdf2:s');

-- --------------------------------------------------------

--
-- Struktur dari tabel `bayar`
--

CREATE TABLE `bayar` (
  `kd_bayar` varchar(12) NOT NULL,
  `kd_petugas` varchar(6) DEFAULT NULL,
  `kd_rawat_inap` varchar(6) DEFAULT NULL,
  `tgl_keluar` date DEFAULT NULL,
  `jml_hari` int(3) DEFAULT NULL,
  `biaya_rawat` varchar(25) DEFAULT NULL,
  `total_bayar` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `bayar`
--

INSERT INTO `bayar` (`kd_bayar`, `kd_petugas`, `kd_rawat_inap`, `tgl_keluar`, `jml_hari`, `biaya_rawat`, `total_bayar`) VALUES
('B-11-01-1', 'TESFIK', 'A-1101', '2018-03-26', 5, '1500000', '9125000'),
('B-11-01-2', 'CCOT91', 'A-1102', '2018-03-25', 2, '850000', '2700000'),
('B-11-01-3', 'M549U6', 'A-1103', '2018-04-06', 4, '500000', '3100000'),
('B-11-01-4', 'ADJKHL', 'A-1104', '2018-04-08', 3, '850000', '3300000');

-- --------------------------------------------------------

--
-- Struktur dari tabel `data_rawat_inap`
--

CREATE TABLE `data_rawat_inap` (
  `kd_rawat_inap` varchar(6) NOT NULL,
  `kd_pasien` varchar(6) DEFAULT NULL,
  `kd_kamar` varchar(6) DEFAULT NULL,
  `kd_dokter` varchar(10) DEFAULT NULL,
  `tgl_masuk` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `data_rawat_inap`
--

INSERT INTO `data_rawat_inap` (`kd_rawat_inap`, `kd_pasien`, `kd_kamar`, `kd_dokter`, `tgl_masuk`) VALUES
('A-1101', 'PP23VF', 'R001', 'F001', '2018-03-21'),
('A-1102', 'PP23GH', 'R002', 'F002', '2018-03-23'),
('A-1103', 'PP23BJ', 'R003', 'F003', '2018-04-02'),
('A-1104', 'PL25LE', 'R002', 'F004', '2018-04-05');

-- --------------------------------------------------------

--
-- Struktur dari tabel `dokter`
--

CREATE TABLE `dokter` (
  `kd_dokter` varchar(10) NOT NULL,
  `nama_dokter` varchar(50) DEFAULT NULL,
  `spesialis` varchar(30) DEFAULT NULL,
  `tarif` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `dokter`
--

INSERT INTO `dokter` (`kd_dokter`, `nama_dokter`, `spesialis`, `tarif`) VALUES
('F001', 'Abitama Satria', 'Jantung', '325000'),
('F002', 'Aria Samudera', 'Bedah', '500000'),
('F003', 'Dhea Fairuz', 'Kulit', '275000'),
('F004', 'Fitria Rizqa', 'Gigi', '250000'),
('F005', 'Hanif Arief', 'Jantung', '300000'),
('F006', 'Ismail Yusuf', 'Bedah', '350000'),
('F007', 'Muhammad Andri', 'Kulit', '265000'),
('F008', 'Prasastia Aryani ', 'Saraf', '225000'),
('F009', 'Syahifa Rahmita', 'Gigi', '270000');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pasien`
--

CREATE TABLE `pasien` (
  `kd_pasien` varchar(6) NOT NULL,
  `nama_pasien` varchar(40) DEFAULT NULL,
  `jenis_kelamin` varchar(10) DEFAULT NULL,
  `alamat` varchar(50) DEFAULT NULL,
  `umur` varchar(5) DEFAULT NULL,
  `pembuatan` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `admin` varchar(20) DEFAULT 'admin'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `pasien`
--

INSERT INTO `pasien` (`kd_pasien`, `nama_pasien`, `jenis_kelamin`, `alamat`, `umur`, `pembuatan`, `admin`) VALUES
('PL25LE', 'Lele', 'Laki-Laki', 'Tangerang', '25', '2018-05-30 17:38:47', 'admin'),
('PP22EQ', 'nurul', 'Perempuan', 'Bogor', '22', '2018-05-30 17:38:47', 'admin'),
('PP23BJ', 'Lulu', 'Perempuan', 'Bogor', '22', '2018-05-30 17:38:47', 'admin'),
('PP23GH', 'Lili', 'Perempuan', 'Depok', '23', '2018-05-30 17:38:47', 'admin'),
('PP23VF', 'Lala', 'Perempuan', 'Jakarta Timur', '23', '2018-05-30 17:38:47', 'admin');

-- --------------------------------------------------------

--
-- Struktur dari tabel `ruang_inap`
--

CREATE TABLE `ruang_inap` (
  `kd_kamar` varchar(6) NOT NULL,
  `nama_kamar` varchar(20) DEFAULT NULL,
  `kelas_kamar` int(2) DEFAULT NULL,
  `tarif` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `ruang_inap`
--

INSERT INTO `ruang_inap` (`kd_kamar`, `nama_kamar`, `kelas_kamar`, `tarif`) VALUES
('R001', 'Cemara', 1, '1500000'),
('R002', 'Bougenville', 2, '850000'),
('R003', 'Mawar', 3, '500000');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`kd_petugas`);

--
-- Indeks untuk tabel `bayar`
--
ALTER TABLE `bayar`
  ADD PRIMARY KEY (`kd_bayar`),
  ADD KEY `fk_petugas` (`kd_petugas`),
  ADD KEY `fk_rawat` (`kd_rawat_inap`);

--
-- Indeks untuk tabel `data_rawat_inap`
--
ALTER TABLE `data_rawat_inap`
  ADD PRIMARY KEY (`kd_rawat_inap`),
  ADD KEY `fk_pasien` (`kd_pasien`),
  ADD KEY `fk_kamar` (`kd_kamar`),
  ADD KEY `fk_dokter` (`kd_dokter`);

--
-- Indeks untuk tabel `dokter`
--
ALTER TABLE `dokter`
  ADD PRIMARY KEY (`kd_dokter`);

--
-- Indeks untuk tabel `pasien`
--
ALTER TABLE `pasien`
  ADD PRIMARY KEY (`kd_pasien`);

--
-- Indeks untuk tabel `ruang_inap`
--
ALTER TABLE `ruang_inap`
  ADD PRIMARY KEY (`kd_kamar`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `bayar`
--
ALTER TABLE `bayar`
  ADD CONSTRAINT `fk_petugas` FOREIGN KEY (`kd_petugas`) REFERENCES `admin` (`kd_petugas`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_rawat` FOREIGN KEY (`kd_rawat_inap`) REFERENCES `data_rawat_inap` (`kd_rawat_inap`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `data_rawat_inap`
--
ALTER TABLE `data_rawat_inap`
  ADD CONSTRAINT `fk_dokter` FOREIGN KEY (`kd_dokter`) REFERENCES `dokter` (`kd_dokter`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_kamar` FOREIGN KEY (`kd_kamar`) REFERENCES `ruang_inap` (`kd_kamar`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pasien` FOREIGN KEY (`kd_pasien`) REFERENCES `pasien` (`kd_pasien`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
