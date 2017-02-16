create table user(
	username varchar(10),
	password varchar(9) not null,
	PRIMARY KEY(username))
create table user_info(username varchar(10),sex char,email varchar(10),PRIMARY KEY(username));
