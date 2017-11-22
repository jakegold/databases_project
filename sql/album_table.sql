CREATE TABLE album(
	albumID int NOT NULL auto_increment,
	title varchar(50),
	bandID int,
	movieID int,
	PRIMARY KEY(albumID),
	FOREIGN KEY (bandID) references band(bandID)
		on delete cascade,
	FOREIGN KEY (movieID) references movie(movieID)
		on delete set null
);
