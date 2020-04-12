create schema  if not exists `login-app`;

create table if not exists `login-app`.`acces-log`
(
    id         int auto_increment
        primary key,
    user       varchar(10)                        not null,
    password   varchar(10)                        not null,
    acces_time datetime default CURRENT_TIMESTAMP not null,
    state      varchar(10)                        not null
);

create table if not exists `login-app`.usuarios
(
    id       int auto_increment
        primary key,
    username varchar(20) not null,
    password varchar(10) not null
);