/*
SQLyog Community v12.4.0 (64 bit)
MySQL - 10.4.32-MariaDB : Database - prediccionesdb1
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`prediccionesdb1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `prediccionesdb1`;

/*Table structure for table `predicciones` */

DROP TABLE IF EXISTS `predicciones`;

CREATE TABLE `predicciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Imagen` varchar(255) DEFAULT NULL,
  `Edad_rango` varchar(30) DEFAULT NULL,
  `Genero` varchar(50) DEFAULT NULL,
  `Emocion` varchar(50) DEFAULT NULL,
  `Precision_Edad` varchar(255) DEFAULT NULL,
  `Precision_Genero` varchar(255) DEFAULT NULL,
  `Precision_Emocion` varchar(255) DEFAULT NULL,
  `fecha_Hora` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `predicciones` */

insert  into `predicciones`(`id`,`Imagen`,`Edad_rango`,`Genero`,`Emocion`,`Precision_Edad`,`Precision_Genero`,`Precision_Emocion`,`fecha_Hora`) values 
(1,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\6e336b92-ca36-40b9-aca5-aa06e83eff94.jpg','29','Man','sad','1.0','0.953096330165863','0.4110424220561981','2025-02-14 08:29:32'),
(2,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\06c9d1ff-a09e-4c9e-ad96-cf3ba29481c3.jpg','27','Man','sad','1.0','0.9823079109191895','0.711014449596405','2025-02-14 08:32:49'),
(3,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\898843b9-2d39-4a4a-8be3-b8dcdcd8adc6.jpg','27','Man','neutral','1.0','0.9997982382774353','0.9741238355636597','2025-02-14 09:37:08'),
(4,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\fb11a8c9-ae38-4e14-b1e7-5bea84991795.jpg','27','Man','neutral','1.0','0.9771705865859985','0.4862271845340729','2025-02-14 10:20:51'),
(5,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\e9117689-1e6a-4224-9dd5-e53f105fcd21.jpg','27','Man','sad','1.0','0.9536347389221191','0.5226823091506958','2025-02-14 10:22:34'),
(6,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\a8c4194b-7401-481f-89c7-5bc66d8d53f5.jpg','26','Man','sad','1.0','0.9716382622718811','0.5024617910385132','2025-02-14 10:24:15'),
(7,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\c2e97703-2039-4bff-b81c-052d6fc708ec.jpg','26','Man','neutral','1.0','0.9834385514259338','0.5494621396064758','2025-02-14 10:26:03'),
(8,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\164acaba-7859-4e9e-a6b9-1641e6cc8759.jpg','25','Man','neutral','1.0','0.9754676222801208','0.5911598096895445','2025-02-14 10:34:12'),
(9,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\d9ff725e-127c-44ac-8109-71c66ea81588.jpg','25','Man','sad','1.0','0.9895439147949219','0.4502201974391937','2025-02-14 10:35:55'),
(10,'C:\\Users\\lenin\\Desktop\\Proyecto final\\Modelos\\FINAL\\DATAC12\\d734c80d-50dd-4135-a593-657c0e4975da.jpg','25','Man','sad','1.0','0.9654656052589417','0.9895187610100962','2025-02-14 11:34:19');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
