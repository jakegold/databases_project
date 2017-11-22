CREATE TABLE song(
	songID int NOT NULL auto_increment,
	title varchar(50),
	albumID int,
	duration int,
	PRIMARY KEY(songID),
	FOREIGN KEY (albumID) references album(albumID)
		on delete cascade
);
