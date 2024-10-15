from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Hardcoded song dictionary
songs = {
    "Song 1": {"artist": "Artist A", "album": "Album X", "genre": "Pop"},
    "Song 2": {"artist": "Artist B", "album": "Album Y", "genre": "Rock"},
    "Song 3": {"artist": "Artist C", "album": "Album Z", "genre": "Pop"},
    "Song 4": {"artist": "Artist D", "album": "Album W", "genre": "Jazz"},
    "Song 5": {"artist": "Artist E", "album": "Album V", "genre": "Rock"},
    "Song 6": {"artist": "Artist F", "album": "Album U", "genre": "Hip-Hop"},
    "Song 7": {"artist": "Artist G", "album": "Album T", "genre": "Classical"},
    "Song 8": {"artist": "Artist H", "album": "Album S", "genre": "Pop"},
    "Song 9": {"artist": "Artist I", "album": "Album R", "genre": "Jazz"},
    "Song 10": {"artist": "Artist J", "album": "Album Q", "genre": "Electronic"},
    "Song 11": {"artist": "Artist K", "album": "Album P", "genre": "Rock"},
    "Song 12": {"artist": "Artist L", "album": "Album O", "genre": "Pop"},
    "Song 13": {"artist": "Artist M", "album": "Album N", "genre": "Hip-Hop"},
    "Song 14": {"artist": "Artist N", "album": "Album M", "genre": "Jazz"},
    "Song 15": {"artist": "Artist O", "album": "Album L", "genre": "Classical"},
    "Song 16": {"artist": "Artist P", "album": "Album K", "genre": "Pop"},
    "Song 17": {"artist": "Artist Q", "album": "Album J", "genre": "Rock"},
    "Song 18": {"artist": "Artist R", "album": "Album I", "genre": "Electronic"},
    "Song 19": {"artist": "Artist S", "album": "Album H", "genre": "Hip-Hop"},
    "Song 20": {"artist": "Artist T", "album": "Album G", "genre": "Pop"},
}

# Route to render the main page
@app.route('/')
def index():
    genre_counts = {}
    for song in songs.values():
        genre = song['genre']
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1
    return render_template('index.html', genre_counts=genre_counts)

# Route to get songs by genre
@app.route('/songs/<genre>')
def get_songs_by_genre(genre):
    genre_songs = {name: details for name, details in songs.items() if details['genre'].lower() == genre.lower()}
    return jsonify(genre_songs)

if __name__ == '__main__':
    app.run(debug=True)