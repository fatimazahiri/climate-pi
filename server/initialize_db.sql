-- Copyright (C) 2020  Connor Czarnuch

-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.

-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.

-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.

create database climatedb;

use climatedb;

create table device
(
    device_id char(5) not null,
    passkey_hash char(16) not null,
    latitude varchar(12) not null,
    longitude varchar(12) not null,
    primary key (device_id)
);

create table data
(
    device_id char(5) not null,
    passkey_hash char(16) not null,
    time int not null,
    temperature float,
    humidity float,
    pressure float,
    gas float,
    uv_index float,
    pm_25 float,
    pm_10 float,
    primary key (device_id, time),
    foreign key (device_id) references device(device_id) on delete cascade,
    foreign key (passkey_hash) references device(passkey_hash) on delete cascade
);

-- Can change password
create user 'raspberrypi'@'localhost' identified by 'raspberry';
grant all privileges on climatedb.* to 'raspberrypi'@'localhost' identified by 'raspberry';
flush privileges;
