insert into person values ('jg', MD5('some'), 'jake', 'goldstein');
insert into person values ('jdubs', MD5('super'), 'jeff', 'wagner');
insert into person values ('sg', MD5('secret'), 'sam', 'grover');
insert into person values ('rc', MD5('password'), 'raizy', 'cohen');

insert into movie (title, release_year, rating) values ('Purple Rain', 1984, 'R');
insert into movie (title, release_year, rating) values ('The Dark Knight', 2008, 'PG-13');
insert into movie (title, release_year, rating) values ('The Lord of the Rings: The Return of the King', 2003, 'PG-13');

insert into band (title) values ('The Beatles');
insert into band (title) values ('Prince');
insert into band (title) values ('Hans Zimmer');
insert into band (title) values ('Howard Shore');

insert into album (title, movieID) values ('Purple Rain', 1);
insert into album (title, movieID) values ('The Dark Knight', 2);
insert into album (title, movieID) values ('Lord Of The Rings 3 Soundtrack', 3);
insert into album (title, movieID) values ('Sgt Peppers Lonely Hearts Club Band', NULL);

insert into song (title, albumID, duration) values ("Sgt. Pepper's Lonely Hearts Club Band", 4, '2:02');
insert into song (title, albumID, duration) values ("With a Little Help from My Friends", 4, '2:44');
insert into song (title, albumID, duration) values ("Let's Go Crazy", 1, '4:40');
insert into song (title, albumID, duration) values ("Purple Rain", 1, '8:41');
insert into song (title, albumID, duration) values ("Why So Serious", 2, '9:14');
insert into song (title, albumID, duration) values ("I'm Not A Hero", 2, '6:34');
insert into song (title, albumID, duration) values ("A Storm Is Coming", 3, '2:52');
insert into song (title, albumID, duration) values ("Hope And Memory", 3, '1:45');
insert into song (title, albumID, duration) values ("Twilight And Shadow", 3, '3:30');
insert into song (title, albumID, duration) values ("Shelob's Lair", 3, '4:07');

insert into workedOn (albumID, bandID) values (1, 2);
insert into workedOn (albumID, bandID) values (4, 1);
insert into workedOn (albumID, bandID) values (2, 3);
insert into workedOn (albumID, bandID) values (3, 4);
