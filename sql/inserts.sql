insert into person values ('jg', MD5('some'), 'jake', 'goldstein');
insert into person values ('jdubs', MD5('super'), 'jeff', 'wagner');
insert into person values ('sg', MD5('secret'), 'sam', 'grover');
insert into person values ('rc', MD5('password'), 'raizy', 'cohen');

insert into movie (title, release_yr) values ('Purple Rain', 1984);
insert into movie (title, release_yr) values ('The Dark Knight', 2008);
insert into movie (title, release_yr) values ('The Lord of the Rings: The Return of the King', 2003);

insert into song (title, artist) values ("Sgt. Pepper's Lonely Hearts Club Band", 'The Beatles');
insert into song (title, artist) values ("With a Little Help from My Friends",  'The Beatles');
insert into song (title, artist) values ("Let's Go Crazy", 'Prince');
insert into song (title, artist) values ("Purple Rain", 'Prince');
insert into song (title, artist) values ("Why So Serious", 'Hans Zimmer');
insert into song (title, artist) values ("I'm Not A Hero", 'Hans Zimmer');
insert into song (title, artist) values ("A Storm Is Coming", 'Hans Zimmer');
insert into song (title, artist) values ("Hope And Memory", 'Howard Shore');
insert into song (title, artist) values ("Twilight And Shadow", 'Howard Shore');
insert into song (title, artist) values ("Shelob's Lair", 'Howard Shore');

insert into song_in_movie (movieID, title) values (1, "Let's Go Crazy");
insert into song_in_movie (movieID, title) values (1, "Purple Rain");
insert into song_in_movie (movieID, title) values (2, "Why So Serious");
insert into song_in_movie (movieID, title) values (2, "I'm Not A Hero");
insert into song_in_movie (movieID, title) values (2, "A Storm Is Coming");
insert into song_in_movie (movieID, title) values (3, "Hope And Memory");
insert into song_in_movie (movieID, title) values (3, "Twilight And Shadow");
insert into song_in_movie (movieID, title) values (3, "Shelob's Lair");


