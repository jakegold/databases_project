CREATE TABLE movie(
	title varchar(50),
	release_year  int,
    rating varchar(5),
	PRIMARY KEY(title, release_year)
);
