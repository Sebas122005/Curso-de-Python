create user if not exists 'admin'@'localhost' identified by 'admin';
grant all privileges on *.* to 'admin'@'localhost' with grant option;


create database if not exists crud_poo;
use crud_poo;

create table if not exists clientes (
    codigo int(10) primary key,
    nombre varchar(100) not null,
    ape_paterno varchar(100) not null,
    ape_materno varchar(100) not null,
    credito int(10) not null
);

insert into clientes (codigo, nombre, ape_paterno, ape_materno, credito) values
(1, 'Juan', 'Perez', 'Lopez', 5000),
(2, 'Maria', 'Gomez', 'Martinez', 7000),
(3, 'Carlos', 'Sanchez', 'Rodriguez', 6000);

select * from clientes;
