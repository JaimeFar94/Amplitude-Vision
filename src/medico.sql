-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-05-2024 a las 18:49:20
-- Versión del servidor: 10.4.25-MariaDB
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `medico`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `antecedentes`
--

CREATE TABLE `antecedentes` (
  `id` int(11) NOT NULL,
  `diabetes` varchar(20) DEFAULT NULL,
  `hipertension` varchar(20) DEFAULT NULL,
  `artritis` varchar(20) DEFAULT NULL,
  `alergia` varchar(20) DEFAULT NULL,
  `catarata` varchar(20) DEFAULT NULL,
  `glaucoma` varchar(20) DEFAULT NULL,
  `estrabismo` varchar(20) DEFAULT NULL,
  `queratocono` varchar(20) DEFAULT NULL,
  `otros` varchar(50) DEFAULT NULL,
  `diabetes_per` varchar(20) DEFAULT NULL,
  `hipertension_per` varchar(20) DEFAULT NULL,
  `Artritis_per` varchar(20) DEFAULT NULL,
  `Alergia_per` varchar(20) DEFAULT NULL,
  `ulcera_per` varchar(20) DEFAULT NULL,
  `cirugia_per` varchar(20) DEFAULT NULL,
  `lentes_contacto_per` varchar(20) DEFAULT NULL,
  `otros1` varchar(20) DEFAULT NULL,
  `descripcion` varchar(80) DEFAULT NULL,
  `paciente_documento` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `antecedentes`
--

INSERT INTO `antecedentes` (`id`, `diabetes`, `hipertension`, `artritis`, `alergia`, `catarata`, `glaucoma`, `estrabismo`, `queratocono`, `otros`, `diabetes_per`, `hipertension_per`, `Artritis_per`, `Alergia_per`, `ulcera_per`, `cirugia_per`, `lentes_contacto_per`, `otros1`, `descripcion`, `paciente_documento`) VALUES
(3, 'refiere', 'no_refiere', 'no_refiere', 'no_refiere', 'no_refiere', 'no_refiere', 'no_refiere', 'no_refiere', '      ', 'No Refiere', 'No Refiere', 'No Refiere', 'No Refiere', 'No Refiere', 'No Refiere', 'No Refiere', 'No Refiere', 'No Refiere', 1019103000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `delete`
--

CREATE TABLE `delete` (
  `id` int(11) NOT NULL,
  `eliminado` tinyint(1) DEFAULT NULL,
  `fecha_eliminacion` datetime DEFAULT NULL,
  `nombre_eliminado` varchar(100) DEFAULT NULL,
  `documento_eliminado` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventory`
--

CREATE TABLE `inventory` (
  `id` int(11) NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `sede` int(11) DEFAULT NULL,
  `montura` varchar(40) DEFAULT NULL,
  `cantidad_montura` int(11) DEFAULT NULL,
  `marca` varchar(40) DEFAULT NULL,
  `referencia` varchar(20) DEFAULT NULL,
  `color` varchar(20) DEFAULT NULL,
  `cordones` varchar(30) DEFAULT NULL,
  `cantidad_cordones` int(11) DEFAULT NULL,
  `estuches` varchar(30) DEFAULT NULL,
  `cantidad_estuches` int(11) DEFAULT NULL,
  `stopper` varchar(50) DEFAULT NULL,
  `cantidad_stopper` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `inventory`
--

INSERT INTO `inventory` (`id`, `fecha`, `sede`, `montura`, `cantidad_montura`, `marca`, `referencia`, `color`, `cordones`, `cantidad_cordones`, `estuches`, `cantidad_estuches`, `stopper`, `cantidad_stopper`) VALUES
(1, '2024-05-01 00:00:00', 0, 'fina', 15, 'Photon ', 'PHQ2737', 'rojo', '0', 0, 'SI', 1, 'N/A', 15),
(2, '2024-05-01 00:00:00', 0, 'fina', 15, 'Photon ', 'PHQ2737', 'rojo', '0', 0, 'SI', 1, 'N/A', 15),
(3, '0000-00-00 00:00:00', 0, '', 0, '', '', '', '', 0, '', 0, '', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mov_consulta`
--

CREATE TABLE `mov_consulta` (
  `id` int(11) NOT NULL,
  `mov_consulta` varchar(200) DEFAULT NULL,
  `ulti_consulta` varchar(100) DEFAULT NULL,
  `esfera` varchar(50) DEFAULT NULL,
  `cilindro` varchar(50) DEFAULT NULL,
  `eje` varchar(50) DEFAULT NULL,
  `dp` varchar(50) DEFAULT NULL,
  `vl20` varchar(50) DEFAULT NULL,
  `vp20` varchar(50) DEFAULT NULL,
  `add_0` varchar(50) DEFAULT NULL,
  `esfera_1` varchar(50) DEFAULT NULL,
  `cilindro_1` varchar(50) DEFAULT NULL,
  `eje_1` varchar(50) DEFAULT NULL,
  `dp_1` varchar(50) DEFAULT NULL,
  `vl20_1` varchar(50) DEFAULT NULL,
  `vp20_1` varchar(50) DEFAULT NULL,
  `add_1` varchar(50) DEFAULT NULL,
  `tipo_lente` varchar(50) DEFAULT NULL,
  `montura` varchar(50) DEFAULT NULL,
  `material` varchar(50) DEFAULT NULL,
  `filtro` varchar(50) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `observacion` varchar(100) DEFAULT NULL,
  `paciente_documento` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `mov_consulta`
--

INSERT INTO `mov_consulta` (`id`, `mov_consulta`, `ulti_consulta`, `esfera`, `cilindro`, `eje`, `dp`, `vl20`, `vp20`, `add_0`, `esfera_1`, `cilindro_1`, `eje_1`, `dp_1`, `vl20_1`, `vp20_1`, `add_1`, `tipo_lente`, `montura`, `material`, `filtro`, `color`, `observacion`, `paciente_documento`) VALUES
(3, 'Ojito maluco', '4/11/2023', 'Esfera', 'Cilindro', 'eje', 'dp', 'vl20', 'vp20', 'add', 'Esfera', 'Cilindro', 'eje', 'dp', 'vl20', 'vp20', 'add', 'bueno', 'fina', 'Material', 'transition', 'rojo', NULL, 1019103000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paciente`
--

CREATE TABLE `paciente` (
  `id` int(11) NOT NULL,
  `documento` int(11) NOT NULL,
  `tipo` varchar(10) DEFAULT NULL,
  `nombre_paciente` varchar(200) DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
  `genero` varchar(50) DEFAULT NULL,
  `correo_electronico` varchar(255) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `telefono` varchar(40) DEFAULT NULL,
  `eps` varchar(50) DEFAULT NULL,
  `cargo` varchar(100) DEFAULT NULL,
  `acompanante` varchar(100) DEFAULT NULL,
  `parentesco` varchar(60) DEFAULT NULL,
  `telefono_acompanante` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `paciente`
--

INSERT INTO `paciente` (`id`, `documento`, `tipo`, `nombre_paciente`, `edad`, `genero`, `correo_electronico`, `direccion`, `telefono`, `eps`, `cargo`, `acompanante`, `parentesco`, `telefono_acompanante`) VALUES
(3, 1019103000, 'cedula', 'Jaime Andres Farfan Rodriguez', 29, 'Masculino', 'farfanjaime05@gmail.com', 'cra 53b#135a12', '3204978115', 'salud total', 'Ingeniero de sistemas', 'Gloria Rodriguez', 'Madre', '3152805686');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibo`
--

CREATE TABLE `recibo` (
  `id` int(11) NOT NULL,
  `fecha_compra` datetime DEFAULT NULL,
  `numero_recibo` int(11) DEFAULT NULL,
  `documento` int(11) DEFAULT NULL,
  `nombre_paciente` varchar(200) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `telefono` int(11) DEFAULT NULL,
  `correo` varchar(200) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `cantidad_1` int(11) DEFAULT NULL,
  `cantidad_2` int(11) DEFAULT NULL,
  `cantidad_3` int(11) DEFAULT NULL,
  `cantidad_4` int(11) DEFAULT NULL,
  `cantidad_5` int(11) DEFAULT NULL,
  `cantidad_6` int(11) DEFAULT NULL,
  `cantidad_7` int(11) DEFAULT NULL,
  `detalle` varchar(200) DEFAULT NULL,
  `detalle_1` varchar(200) DEFAULT NULL,
  `detalle_2` varchar(200) DEFAULT NULL,
  `detalle_3` varchar(200) DEFAULT NULL,
  `detalle_4` varchar(200) DEFAULT NULL,
  `detalle_5` varchar(200) DEFAULT NULL,
  `detalle_6` varchar(200) DEFAULT NULL,
  `detalle_7` varchar(200) DEFAULT NULL,
  `valor_unitario` int(11) DEFAULT NULL,
  `valor_unitario_1` int(11) DEFAULT NULL,
  `valor_unitario_2` int(11) DEFAULT NULL,
  `valor_unitario_3` int(11) DEFAULT NULL,
  `valor_unitario_4` int(11) DEFAULT NULL,
  `valor_unitario_5` int(11) DEFAULT NULL,
  `valor_unitario_6` int(11) DEFAULT NULL,
  `valor_unitario_7` int(11) DEFAULT NULL,
  `valor_total` int(11) DEFAULT NULL,
  `valor_total_1` int(11) DEFAULT NULL,
  `valor_total_2` int(11) DEFAULT NULL,
  `valor_total_3` int(11) DEFAULT NULL,
  `valor_total_4` int(11) DEFAULT NULL,
  `valor_total_5` int(11) DEFAULT NULL,
  `valor_total_6` int(11) DEFAULT NULL,
  `valor_total_7` int(11) DEFAULT NULL,
  `total` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `recibo`
--

INSERT INTO `recibo` (`id`, `fecha_compra`, `numero_recibo`, `documento`, `nombre_paciente`, `direccion`, `telefono`, `correo`, `cantidad`, `cantidad_1`, `cantidad_2`, `cantidad_3`, `cantidad_4`, `cantidad_5`, `cantidad_6`, `cantidad_7`, `detalle`, `detalle_1`, `detalle_2`, `detalle_3`, `detalle_4`, `detalle_5`, `detalle_6`, `detalle_7`, `valor_unitario`, `valor_unitario_1`, `valor_unitario_2`, `valor_unitario_3`, `valor_unitario_4`, `valor_unitario_5`, `valor_unitario_6`, `valor_unitario_7`, `valor_total`, `valor_total_1`, `valor_total_2`, `valor_total_3`, `valor_total_4`, `valor_total_5`, `valor_total_6`, `valor_total_7`, `total`) VALUES
(1, '2024-05-01 00:00:00', 76, 1019103000, 'Jaime Farfan', 'cra53b#135a12', 2147483647, 'jaime.farfan@cun.edu.co', 1, 0, 0, 0, 0, 0, 0, 0, 'Gafas negras', '', '', '', '', '', '', '', 200000, 0, 0, 0, 0, 0, 0, 0, 200000, 0, 0, 0, 0, 0, 0, 0, 200000),
(2, '2024-05-01 00:00:00', 77, 1019103000, 'Jaime Farfan', 'cra53b#135a12', 2147483647, 'jaime.farfan@cun.edu.co', 1, 0, 0, 0, 0, 0, 0, 0, 'Gafas negras', '', '', '', '', '', '', '', 200000, 0, 0, 0, 0, 0, 0, 0, 200000, 0, 0, 0, 0, 0, 0, 0, 200000),
(3, '2024-05-01 00:00:00', 77, 1019103000, 'Jaime Farfan', 'cra53b#135a12', 2147483647, 'jaime.farfan@cun.edu.co', 1, 0, 0, 0, 0, 0, 0, 0, 'Gafas negras', '', '', '', '', '', '', '', 200000, 0, 0, 0, 0, 0, 0, 0, 200000, 0, 0, 0, 0, 0, 0, 0, 200000),
(4, '2024-05-02 00:00:00', 79, 1019103000, 'Jaime Farfan', 'cra53b#135a12', 2147483647, 'jaime.farfan@cun.edu.co', 1, 0, 0, 0, 0, 0, 0, 0, 'Gafas negras', '', '', '', '', '', '', '', 200000, 0, 0, 0, 0, 0, 0, 0, 200000, 0, 0, 0, 0, 0, 0, 0, 200000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `signup`
--

CREATE TABLE `signup` (
  `id` int(11) NOT NULL,
  `nombre` varchar(40) DEFAULT NULL,
  `correo` varchar(70) DEFAULT NULL,
  `usuario` varchar(40) DEFAULT NULL,
  `contrasena` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `signup`
--

INSERT INTO `signup` (`id`, `nombre`, `correo`, `usuario`, `contrasena`) VALUES
(17, 'Jaime Andres Farfan Rodriguez', 'jaime.farfan@cun.edu.co', 'j-farfan', 'e102618b546754fd25bfb221cbfea02d'),
(18, 'Sebastián Ocampo', 'ocampo_trivio@hotmail.com', 'SebasRider', 'd0d3d45cf35c395c0a09f44924f61804'),
(19, 'Jarlon', 'farfanjaime05@gmail.com', 'j@rlon', '4327da8c559489796e81a9fe84ac8099');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vista`
--

CREATE TABLE `vista` (
  `id` int(11) NOT NULL,
  `vision_lejana` varchar(40) DEFAULT NULL,
  `vision_proxima` varchar(40) DEFAULT NULL,
  `ducciones_od` varchar(40) DEFAULT NULL,
  `ducciones_oi` varchar(40) DEFAULT NULL,
  `ppc_od` varchar(40) DEFAULT NULL,
  `ppc_oi` varchar(40) DEFAULT NULL,
  `ojo_derecho` varchar(30) DEFAULT NULL,
  `ojo_izquierdo` varchar(30) DEFAULT NULL,
  `ojo_drc_querato` varchar(30) DEFAULT NULL,
  `ojo_izq_querato` varchar(30) DEFAULT NULL,
  `ojo_drc_refac` varchar(30) DEFAULT NULL,
  `ojo_izq_refac` varchar(30) DEFAULT NULL,
  `esfera_retino` varchar(30) DEFAULT NULL,
  `cilindro_retino` varchar(30) DEFAULT NULL,
  `eje_retino` varchar(30) DEFAULT NULL,
  `dp_retino` varchar(30) DEFAULT NULL,
  `vl20_retino` varchar(30) DEFAULT NULL,
  `vp20_retino` varchar(30) DEFAULT NULL,
  `add_retino` varchar(30) DEFAULT NULL,
  `esfera_retino_1` varchar(30) DEFAULT NULL,
  `cilindro_retino_1` varchar(30) DEFAULT NULL,
  `eje_retino_1` varchar(30) DEFAULT NULL,
  `dp_retino_1` varchar(30) DEFAULT NULL,
  `vl20_retino_1` varchar(30) DEFAULT NULL,
  `vp20_retino_1` varchar(30) DEFAULT NULL,
  `add_retino_1` varchar(30) DEFAULT NULL,
  `paciente_documento` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `vista`
--

INSERT INTO `vista` (`id`, `vision_lejana`, `vision_proxima`, `ducciones_od`, `ducciones_oi`, `ppc_od`, `ppc_oi`, `ojo_derecho`, `ojo_izquierdo`, `ojo_drc_querato`, `ojo_izq_querato`, `ojo_drc_refac`, `ojo_izq_refac`, `esfera_retino`, `cilindro_retino`, `eje_retino`, `dp_retino`, `vl20_retino`, `vp20_retino`, `add_retino`, `esfera_retino_1`, `cilindro_retino_1`, `eje_retino_1`, `dp_retino_1`, `vl20_retino_1`, `vp20_retino_1`, `add_retino_1`, `paciente_documento`) VALUES
(3, 'VISIÓN LEJANA', 'VISION PRÓXIMA', 'DUCCIONES OD', 'DUCCIONES OI', 'PPC OD', 'PPC OI', 'OJO DERECHO OFTALMOSCOPIA', 'OJO IZQUIERDO OFTALMOSCOPIA	', 'OJO DERECHO QUERATOMETRIA', 'OJO IZQUIERDO QUERATOMETRIA', 'OJO DERECHO REFACTROMETRIA', 'OJO IZQUIERDO REFACTROMETRIA', 'Esfera', 'Cilindro', 'eje', 'dp', 'vl20', 'vp20', 'add', 'Esfera', 'Cilindro', 'eje', 'dp', 'vl20', 'vp20', 'add', 1019103000);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `antecedentes`
--
ALTER TABLE `antecedentes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `paciente_documento` (`paciente_documento`);

--
-- Indices de la tabla `delete`
--
ALTER TABLE `delete`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `mov_consulta`
--
ALTER TABLE `mov_consulta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `paciente_documento` (`paciente_documento`);

--
-- Indices de la tabla `paciente`
--
ALTER TABLE `paciente`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `documento` (`documento`);

--
-- Indices de la tabla `recibo`
--
ALTER TABLE `recibo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `signup`
--
ALTER TABLE `signup`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- Indices de la tabla `vista`
--
ALTER TABLE `vista`
  ADD PRIMARY KEY (`id`),
  ADD KEY `paciente_documento` (`paciente_documento`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `antecedentes`
--
ALTER TABLE `antecedentes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `delete`
--
ALTER TABLE `delete`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `mov_consulta`
--
ALTER TABLE `mov_consulta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `paciente`
--
ALTER TABLE `paciente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `recibo`
--
ALTER TABLE `recibo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `signup`
--
ALTER TABLE `signup`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `vista`
--
ALTER TABLE `vista`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `antecedentes`
--
ALTER TABLE `antecedentes`
  ADD CONSTRAINT `antecedentes_ibfk_1` FOREIGN KEY (`paciente_documento`) REFERENCES `paciente` (`documento`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `mov_consulta`
--
ALTER TABLE `mov_consulta`
  ADD CONSTRAINT `mov_consulta_ibfk_1` FOREIGN KEY (`paciente_documento`) REFERENCES `paciente` (`documento`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `vista`
--
ALTER TABLE `vista`
  ADD CONSTRAINT `vista_ibfk_1` FOREIGN KEY (`paciente_documento`) REFERENCES `paciente` (`documento`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
