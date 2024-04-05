create table usuario
(
    id_usuario SMALLINT UNSIGNED AUTO_INCREMENT,
    nombre CHAR(50) NOT NULL,
    apellido_1 CHAR(20) NOT NULL,
    apellido_2 CHAR(20),
    sexo ENUM('M','F','X') DEFAULT 'X',
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(12) NOT NULL,
    correo VARCHAR(255) NOT NULL,

    PRIMARY KEY (id_usuario)
)   AUTO_INCREMENT=1;





CREATE TABLE pago
(
    id_pago SMALLINT UNSIGNED AUTO_INCREMENT,
    id_usuario SMALLINT UNSIGNED NOT NULL,
    fecha_pago DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    metodo ENUM('Tarjeta','Efectivo') NOT NULL,
    cvc CHAR(3),
    expiracion CHAR(5),
    num_tarjeta CHAR(16),


    PRIMARY KEY (id_pago),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE ON UPDATE CASCADE
)   AUTO_INCREMENT=1;





CREATE TABLE departamento
(
    id_departamento SMALLINT UNSIGNED AUTO_INCREMENT, 
    precio DECIMAL(10,2) NOT NULL,
    direccion VARCHAR(255),
    info VARCHAR(255),

    PRIMARY KEY (id_departamento)
)   AUTO_INCREMENT=1;





CREATE TABLE reservacion
(
    id_reservacion SMALLINT UNSIGNED AUTO_INCREMENT,
    id_departamento SMALLINT UNSIGNED NOT NULL,
    id_usuario SMALLINT UNSIGNED NOT NULL,
    id_pago SMALLINT UNSIGNED NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,

    PRIMARY KEY (id_reservacion),
    FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_pago) REFERENCES pago(id_pago)
        ON DELETE CASCADE ON UPDATE CASCADE
)   AUTO_INCREMENT=1;






CREATE TABLE empleado
(
    id_sueldo SMALLINT UNSIGNED PRIMARY KEY,
    id_pago SMALLINT UNSIGNED,
    nombre VARCHAR(50) NOT NULL,
    apellido1 VARCHAR(15) NOT NULL,
    apellido2 VARCHAR(15),
    fecha_nacimiento DATE NOT NULL,
    sexo ENUM('M','F','X') DEFAULT 'X',
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE,
    estado BIT(1) NOT NULL,
    telefono CHAR(10) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    puesto VARCHAR(100) NOT NULL,
    sueldo DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_pago) REFERENCES pago(id_pago) ON DELETE CASCADE ON UPDATE CASCADE
);