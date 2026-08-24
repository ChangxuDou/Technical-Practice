-- String,Numeric,Date and Time,Blob,Spatial

-- String -- 

-- 1) Char(x) fixed-length,like abbreviation of states
-- 2) Varchar(x) variable length strings(65,535 charactors ~64KB),usernames,passwords,e-mails,addresses
-- Varchar(50)  for username and passwords
-- Varchar(255) for Addresses
-- Warning: no mathematical operation

-- 3)MEDIUMTEXT: 16MB (JSON,CSV)
-- 4)LONGTEXT:4GB(Textbook,years of log files)
-- 5)TINYTEXT: 255 bytes

-- 6)TEXT: 64KB
-- Tipps: like Varchar,for this range of charactors, it's better to use Varchar type, cuz it can be indexed

-- English letter ;1 byte
-- European:2 bytes
-- Chinese/Japanese:3 bytes
-- Tipps: if the type of a column is char of 10, MYSQL will reserve 30 bytes for the values in that column