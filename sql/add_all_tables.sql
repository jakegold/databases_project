CREATE TABLE user(
	username varchar(50),
	password varchar(50),
	PRIMARY KEY(username)
);

CREATE TABLE movie(
	movieID int NOT NULL auto_increment,
	title varchar(50),
	release_year  int,
    rating varchar(5),
	PRIMARY KEY(movieID)
);

CREATE TABLE band(
	bandID int NOT NULL auto_increment,
	title varchar(50),
	PRIMARY KEY(bandID)
);

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

CREATE TABLE song(
	songID int NOT NULL auto_increment,
	title varchar(50),
    albumID int,
    duration int,
	PRIMARY KEY(songID),
    FOREIGN KEY (albumID) references album(albumID)
		on delete cascade
);
