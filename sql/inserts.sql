insert into user values ('jake', MD5('some'));
insert into user values ('jeff', MD5('super'));
insert into user values ('sam', MD5('secret'));
insert into user values ('raizy', MD5('password'));

insert into movie (title, release_year, rating) values ('Purple Rain', 1984, 'R');
insert into movie (title, release_year, rating) values ('The Dark Knight', 2008, 'PG-13');
insert into movie (title, release_year, rating) values ('The Lord of the Rings: The Return of the King ', 2003, 'PG-13');

insert into band (title) values ('The Beatles');
insert into band (title) values ('Prince');
insert into band (title) values ('Hans Zimmer');
insert into band (title) values ('Lord Of The Rings 3 Soundtrack');
insert into band (title) values ('Howard Shore');

insert into album (title, bandID, movieID) values ('Purple Rain', 2, 1);
insert into album (title, bandID, movieID) values ('The Dark Knight', 3, 3);
insert into album (title, bandID, movieID) values ('Lord Of The Rings 3 Soundtrack', 16, 5);
insert into album (title, bandID, movieID) values ('Lord Of The Rings 3 Soundtrack', 17, 5);
insert into album (title, bandID, movieID) values ('Sgt Peppers Lonely Hearts Club Band', 1, NULL);

insert into song (title, albumID, duration) values ("Sgt. Pepper's Lonely Hearts Club Band", 5, '2:02');
insert into song (title, albumID, duration) values ("With a Little Help from My Friends", 5, '2:44');
insert into song (title, albumID, duration) values ("Let's Go Crazy", 1, '4:40');
insert into song (title, albumID, duration) values ("Purple Rain", 1, '8:41');
insert into song (title, albumID, duration) values ("Why So Serious", 2, '9:14');
insert into song (title, albumID, duration) values ("I'm Not A Hero", 2, '6:34');
insert into song (title, albumID, duration) values ("A Storm Is Coming", 3, '2:52');
insert into song (title, albumID, duration) values ("Hope And Memory", 3, '1:45');
insert into song (title, albumID, duration) values ("Twilight And Shadow", 4, '3:30');
insert into song (title, albumID, duration) values ("Shelob's Lair", 4, '4:07');
