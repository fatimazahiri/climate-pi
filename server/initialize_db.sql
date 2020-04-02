create database climatedb;

use climatedb;

create table device(
    device_id varchar(5) not null,
    device_location varchar(24) not null,
    primary key (device_id)
);

create table data(
    device_id varchar(5) not null,
    time int not null,
    temperature float,
    humidity float,
    pressure float,
    uv_index float,
    primary key (device_id, time),
    foreign key (device_id) references device(device_id) on delete cascade
);

-- Can change password
create user 'raspberrypi'@'localhost' identified by 'raspberry';