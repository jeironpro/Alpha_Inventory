-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-12-2023 a las 06:23:45
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `alpha_inventory`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_articulos`
--

CREATE TABLE `alphainventory_articulos` (
  `id_articulo` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `talla` varchar(20) NOT NULL,
  `marca` varchar(20) NOT NULL,
  `referencia` varchar(80) NOT NULL,
  `ubicacion` varchar(20) NOT NULL,
  `costo` int(11) NOT NULL,
  `precio` int(11) NOT NULL,
  `itbis` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `unidadMedida` varchar(8) NOT NULL,
  `margenBeneficio` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_clientes`
--

CREATE TABLE `alphainventory_clientes` (
  `id_cliente` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `direccion` varchar(80) NOT NULL,
  `ciudad` varchar(20) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `cedula` varchar(11) NOT NULL,
  `correoElectronico` varchar(254) NOT NULL,
  `rnc` int(11) NOT NULL,
  `descuento` varchar(4) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_compras`
--

CREATE TABLE `alphainventory_compras` (
  `id_compra` int(11) NOT NULL,
  `horaCompra` time(6) NOT NULL,
  `fechaCompra` date NOT NULL,
  `encargadoCompra` varchar(50) NOT NULL,
  `suplidor` varchar(50) NOT NULL,
  `codigo` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `itbis` int(11) NOT NULL,
  `costo` int(11) NOT NULL,
  `totalCompra` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_encargadoscompras`
--

CREATE TABLE `alphainventory_encargadoscompras` (
  `id_encargadoCompra` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `encargadoCompra` varchar(50) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_encargadosventas`
--

CREATE TABLE `alphainventory_encargadosventas` (
  `id_encargadoVenta` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `encargadoVenta` varchar(50) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_marcas`
--

CREATE TABLE `alphainventory_marcas` (
  `id_marca` int(11) NOT NULL,
  `marca` varchar(50) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_registrousuario`
--

CREATE TABLE `alphainventory_registrousuario` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `apellido` varchar(40) NOT NULL,
  `nombreUsuario` varchar(20) NOT NULL,
  `direccion` varchar(80) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `correoElectronico` varchar(254) NOT NULL,
  `contrasena` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_suplidores`
--

CREATE TABLE `alphainventory_suplidores` (
  `id_suplidor` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `direccion` varchar(80) NOT NULL,
  `ciudad` varchar(20) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `limiteCredito` varchar(11) NOT NULL,
  `condiciones` varchar(50) NOT NULL,
  `rnc` int(11) NOT NULL,
  `descuento` varchar(4) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alphainventory_ventas`
--

CREATE TABLE `alphainventory_ventas` (
  `id_venta` int(11) NOT NULL,
  `horaVenta` time(6) NOT NULL,
  `fechaVenta` date NOT NULL,
  `encargadoVenta` varchar(50) NOT NULL,
  `cliente` varchar(50) NOT NULL,
  `codigo` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `itbis` int(11) NOT NULL,
  `precio` int(11) NOT NULL,
  `totalVenta` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add registro usuario', 1, 'add_registrousuario'),
(2, 'Can change registro usuario', 1, 'change_registrousuario'),
(3, 'Can delete registro usuario', 1, 'delete_registrousuario'),
(4, 'Can view registro usuario', 1, 'view_registrousuario'),
(5, 'Can add marcas', 2, 'add_marcas'),
(6, 'Can change marcas', 2, 'change_marcas'),
(7, 'Can delete marcas', 2, 'delete_marcas'),
(8, 'Can view marcas', 2, 'view_marcas'),
(9, 'Can add encargados ventas', 3, 'add_encargadosventas'),
(10, 'Can change encargados ventas', 3, 'change_encargadosventas'),
(11, 'Can delete encargados ventas', 3, 'delete_encargadosventas'),
(12, 'Can view encargados ventas', 3, 'view_encargadosventas'),
(13, 'Can add encargados compras', 4, 'add_encargadoscompras'),
(14, 'Can change encargados compras', 4, 'change_encargadoscompras'),
(15, 'Can delete encargados compras', 4, 'delete_encargadoscompras'),
(16, 'Can view encargados compras', 4, 'view_encargadoscompras'),
(17, 'Can add compras', 5, 'add_compras'),
(18, 'Can change compras', 5, 'change_compras'),
(19, 'Can delete compras', 5, 'delete_compras'),
(20, 'Can view compras', 5, 'view_compras'),
(21, 'Can add clientes', 6, 'add_clientes'),
(22, 'Can change clientes', 6, 'change_clientes'),
(23, 'Can delete clientes', 6, 'delete_clientes'),
(24, 'Can view clientes', 6, 'view_clientes'),
(25, 'Can add articulos', 7, 'add_articulos'),
(26, 'Can change articulos', 7, 'change_articulos'),
(27, 'Can delete articulos', 7, 'delete_articulos'),
(28, 'Can view articulos', 7, 'view_articulos'),
(29, 'Can add suplidores', 8, 'add_suplidores'),
(30, 'Can change suplidores', 8, 'change_suplidores'),
(31, 'Can delete suplidores', 8, 'delete_suplidores'),
(32, 'Can view suplidores', 8, 'view_suplidores'),
(33, 'Can add ventas', 9, 'add_ventas'),
(34, 'Can change ventas', 9, 'change_ventas'),
(35, 'Can delete ventas', 9, 'delete_ventas'),
(36, 'Can view ventas', 9, 'view_ventas'),
(37, 'Can add log entry', 10, 'add_logentry'),
(38, 'Can change log entry', 10, 'change_logentry'),
(39, 'Can delete log entry', 10, 'delete_logentry'),
(40, 'Can view log entry', 10, 'view_logentry'),
(41, 'Can add permission', 11, 'add_permission'),
(42, 'Can change permission', 11, 'change_permission'),
(43, 'Can delete permission', 11, 'delete_permission'),
(44, 'Can view permission', 11, 'view_permission'),
(45, 'Can add group', 12, 'add_group'),
(46, 'Can change group', 12, 'change_group'),
(47, 'Can delete group', 12, 'delete_group'),
(48, 'Can view group', 12, 'view_group'),
(49, 'Can add user', 13, 'add_user'),
(50, 'Can change user', 13, 'change_user'),
(51, 'Can delete user', 13, 'delete_user'),
(52, 'Can view user', 13, 'view_user'),
(53, 'Can add content type', 14, 'add_contenttype'),
(54, 'Can change content type', 14, 'change_contenttype'),
(55, 'Can delete content type', 14, 'delete_contenttype'),
(56, 'Can view content type', 14, 'view_contenttype'),
(57, 'Can add session', 15, 'add_session'),
(58, 'Can change session', 15, 'change_session'),
(59, 'Can delete session', 15, 'delete_session'),
(60, 'Can view session', 15, 'view_session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(10, 'admin', 'logentry'),
(7, 'AlphaInventory', 'articulos'),
(6, 'AlphaInventory', 'clientes'),
(5, 'AlphaInventory', 'compras'),
(4, 'AlphaInventory', 'encargadoscompras'),
(3, 'AlphaInventory', 'encargadosventas'),
(2, 'AlphaInventory', 'marcas'),
(1, 'AlphaInventory', 'registrousuario'),
(8, 'AlphaInventory', 'suplidores'),
(9, 'AlphaInventory', 'ventas'),
(12, 'auth', 'group'),
(11, 'auth', 'permission'),
(13, 'auth', 'user'),
(14, 'contenttypes', 'contenttype'),
(15, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'AlphaInventory', '0001_initial', '2023-12-30 05:22:23.124180'),
(2, 'contenttypes', '0001_initial', '2023-12-30 05:22:23.787940'),
(3, 'auth', '0001_initial', '2023-12-30 05:22:37.501225'),
(4, 'admin', '0001_initial', '2023-12-30 05:22:40.798024'),
(5, 'admin', '0002_logentry_remove_auto_add', '2023-12-30 05:22:40.915991'),
(6, 'admin', '0003_logentry_add_action_flag_choices', '2023-12-30 05:22:41.052620'),
(7, 'contenttypes', '0002_remove_content_type_name', '2023-12-30 05:22:42.539191'),
(8, 'auth', '0002_alter_permission_name_max_length', '2023-12-30 05:22:44.363227'),
(9, 'auth', '0003_alter_user_email_max_length', '2023-12-30 05:22:45.747239'),
(10, 'auth', '0004_alter_user_username_opts', '2023-12-30 05:22:45.808494'),
(11, 'auth', '0005_alter_user_last_login_null', '2023-12-30 05:22:46.665071'),
(12, 'auth', '0006_require_contenttypes_0002', '2023-12-30 05:22:46.711499'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2023-12-30 05:22:46.771604'),
(14, 'auth', '0008_alter_user_username_max_length', '2023-12-30 05:22:47.041858'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2023-12-30 05:22:47.182450'),
(16, 'auth', '0010_alter_group_name_max_length', '2023-12-30 05:22:48.227856'),
(17, 'auth', '0011_update_proxy_permissions', '2023-12-30 05:22:48.323837'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2023-12-30 05:22:48.491026'),
(19, 'sessions', '0001_initial', '2023-12-30 05:22:49.065575');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alphainventory_articulos`
--
ALTER TABLE `alphainventory_articulos`
  ADD PRIMARY KEY (`id_articulo`),
  ADD KEY `AlphaInventory_artic_usuario_id_9ea49fe0_fk_AlphaInve` (`usuario_id`);

--
-- Indices de la tabla `alphainventory_clientes`
--
ALTER TABLE `alphainventory_clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD KEY `AlphaInventory_clien_usuario_id_f23e3c0d_fk_AlphaInve` (`usuario_id`);

--
-- Indices de la tabla `alphainventory_compras`
--
ALTER TABLE `alphainventory_compras`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `AlphaInventory_compr_usuario_id_27f90d49_fk_AlphaInve` (`usuario_id`);

--
-- Indices de la tabla `alphainventory_encargadoscompras`
--
ALTER TABLE `alphainventory_encargadoscompras`
  ADD PRIMARY KEY (`id_encargadoCompra`),
  ADD KEY `AlphaInventory_encar_usuario_id_bacb336e_fk_AlphaInve` (`usuario_id`);

--
-- Indices de la tabla `alphainventory_encargadosventas`
--
ALTER TABLE `alphainventory_encargadosventas`
  ADD PRIMARY KEY (`id_encargadoVenta`),
  ADD KEY `AlphaInventory_encar_usuario_id_1db5376e_fk_AlphaInve` (`usuario_id`);

--
-- Indices de la tabla `alphainventory_marcas`
--
ALTER TABLE `alphainventory_marcas`
  ADD PRIMARY KEY (`id_marca`),
  ADD KEY `AlphaInventory_marca_usuario_id_14ab6924_fk_AlphaInve` (`usuario_id`);

--
-- Indices de la tabla `alphainventory_registrousuario`
--
ALTER TABLE `alphainventory_registrousuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `nombreUsuario` (`nombreUsuario`),
  ADD UNIQUE KEY `correoElectronico` (`correoElectronico`);

--
-- Indices de la tabla `alphainventory_suplidores`
--
ALTER TABLE `alphainventory_suplidores`
  ADD PRIMARY KEY (`id_suplidor`),
  ADD KEY `AlphaInventory_supli_usuario_id_f03aacd5_fk_AlphaInve` (`usuario_id`);

--
-- Indices de la tabla `alphainventory_ventas`
--
ALTER TABLE `alphainventory_ventas`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `AlphaInventory_venta_usuario_id_77f8e5e4_fk_AlphaInve` (`usuario_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alphainventory_articulos`
--
ALTER TABLE `alphainventory_articulos`
  MODIFY `id_articulo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alphainventory_clientes`
--
ALTER TABLE `alphainventory_clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alphainventory_compras`
--
ALTER TABLE `alphainventory_compras`
  MODIFY `id_compra` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alphainventory_encargadoscompras`
--
ALTER TABLE `alphainventory_encargadoscompras`
  MODIFY `id_encargadoCompra` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alphainventory_encargadosventas`
--
ALTER TABLE `alphainventory_encargadosventas`
  MODIFY `id_encargadoVenta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alphainventory_marcas`
--
ALTER TABLE `alphainventory_marcas`
  MODIFY `id_marca` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alphainventory_registrousuario`
--
ALTER TABLE `alphainventory_registrousuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alphainventory_suplidores`
--
ALTER TABLE `alphainventory_suplidores`
  MODIFY `id_suplidor` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `alphainventory_ventas`
--
ALTER TABLE `alphainventory_ventas`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alphainventory_articulos`
--
ALTER TABLE `alphainventory_articulos`
  ADD CONSTRAINT `AlphaInventory_artic_usuario_id_9ea49fe0_fk_AlphaInve` FOREIGN KEY (`usuario_id`) REFERENCES `alphainventory_registrousuario` (`id_usuario`);

--
-- Filtros para la tabla `alphainventory_clientes`
--
ALTER TABLE `alphainventory_clientes`
  ADD CONSTRAINT `AlphaInventory_clien_usuario_id_f23e3c0d_fk_AlphaInve` FOREIGN KEY (`usuario_id`) REFERENCES `alphainventory_registrousuario` (`id_usuario`);

--
-- Filtros para la tabla `alphainventory_compras`
--
ALTER TABLE `alphainventory_compras`
  ADD CONSTRAINT `AlphaInventory_compr_usuario_id_27f90d49_fk_AlphaInve` FOREIGN KEY (`usuario_id`) REFERENCES `alphainventory_registrousuario` (`id_usuario`);

--
-- Filtros para la tabla `alphainventory_encargadoscompras`
--
ALTER TABLE `alphainventory_encargadoscompras`
  ADD CONSTRAINT `AlphaInventory_encar_usuario_id_bacb336e_fk_AlphaInve` FOREIGN KEY (`usuario_id`) REFERENCES `alphainventory_registrousuario` (`id_usuario`);

--
-- Filtros para la tabla `alphainventory_encargadosventas`
--
ALTER TABLE `alphainventory_encargadosventas`
  ADD CONSTRAINT `AlphaInventory_encar_usuario_id_1db5376e_fk_AlphaInve` FOREIGN KEY (`usuario_id`) REFERENCES `alphainventory_registrousuario` (`id_usuario`);

--
-- Filtros para la tabla `alphainventory_marcas`
--
ALTER TABLE `alphainventory_marcas`
  ADD CONSTRAINT `AlphaInventory_marca_usuario_id_14ab6924_fk_AlphaInve` FOREIGN KEY (`usuario_id`) REFERENCES `alphainventory_registrousuario` (`id_usuario`);

--
-- Filtros para la tabla `alphainventory_suplidores`
--
ALTER TABLE `alphainventory_suplidores`
  ADD CONSTRAINT `AlphaInventory_supli_usuario_id_f03aacd5_fk_AlphaInve` FOREIGN KEY (`usuario_id`) REFERENCES `alphainventory_registrousuario` (`id_usuario`);

--
-- Filtros para la tabla `alphainventory_ventas`
--
ALTER TABLE `alphainventory_ventas`
  ADD CONSTRAINT `AlphaInventory_venta_usuario_id_77f8e5e4_fk_AlphaInve` FOREIGN KEY (`usuario_id`) REFERENCES `alphainventory_registrousuario` (`id_usuario`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
