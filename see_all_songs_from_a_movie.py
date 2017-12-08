"""
NOTE!!!!!
This file should be included in a larger file. I just put it here like this so I could find it quickly if I needed to.
Again, this file should not be part of the final product!!!
"""

# NEW FOR SEEING SONGS FROM MOVIES
@app.route('/movies/<movieID>')
def songs_from_movies(movieID):

        print 'we here???'

        cursor = conn.cursor();
        movie_query = 'SELECT title from movie where movieID = %s'
        cursor.execute(movie_query, (movieID))
        movie_title = cursor.fetchone()

        if not movie_title:
            error = 'This movie does not exist!'
            return render_template('movie_and_songs.html', title_error = error)

        movie_title = movie_title['title']
        song_query = 'SELECT title, artist from song where title in (SELECT title from song_in_movie where movieID = %s)'
        cursor.execute(song_query,(movieID))
        song_data = cursor.fetchall()
        cursor.close()
        error = None
        if song_data:
            return render_template('movie_and_songs.html', posts=song_data, movie=movie_title, error=error)
        else:
            error = 'This Movie does not play any songs in it'
            return render_template('movie_and_songs.html', posts=song_data, movie=movie_title, error=error)  
