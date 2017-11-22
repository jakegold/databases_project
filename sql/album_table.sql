CREATE TABLE album(
	  albumID int NOT NULL auto_increment,
	  title varchar(50),
    bandID varchar(50),
	  PRIMARY KEY(albumID),
    FOREIGN KEY (bandID) references band(bandID)
		  on delete cascade
);
