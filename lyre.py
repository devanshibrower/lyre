from flask import Flask, render_template, redirect, request, session, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv, find_dotenv
import os
import time
from collections import defaultdict

# Load environment variables from .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
print(f"Loading environment variables from: {dotenv_path}")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Spotify credentials
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
print(f"CLIENT_ID: {CLIENT_ID}, CLIENT_SECRET: {CLIENT_SECRET}, REDIRECT_URI: {REDIRECT_URI}")
print(f"Redirect URI: {os.getenv('SPOTIPY_REDIRECT_URI')}")

# Set up Spotipy authentication
sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="playlist-read-private"
)


@app.route('/')
def index():
    print("Accessing index route")
    if not session.get('token_info'):
        print("No token info, redirecting to login")
        return redirect('/login')
    print("Token info found, redirecting to playlists")
    return redirect('/playlists')

@app.route('/login')
def login():
    print("Accessing login route")
    auth_url = sp_oauth.get_authorize_url()
    print(f"Generated auth URL: {auth_url}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    print("Accessing callback route")
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    print("Token info saved to session, redirecting to playlists")
    return redirect('/playlists')

@app.route('/playlists')
def playlists():
    token_info = get_token()
    if not token_info:
        return redirect('/login')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_playlists()
    
    return render_template('playlists.html', playlists=results['items'])

@app.route('/get_playlist/<playlist_id>')
def get_playlist(playlist_id):
    token_info = get_token()
    if not token_info:
        return jsonify({'error': 'Not authenticated'}), 401
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Get playlist tracks
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Get more tracks if the playlist has more than 100 tracks
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    genre_counts = defaultdict(int)
    songs = []
    
    for item in tracks:
        track = item['track']
        if track is not None:
            # Get artist genres
            artist_id = track['artists'][0]['id']
            artist_info = sp.artist(artist_id)
            genres = artist_info['genres']
            
            # If no genres, use "Unknown"
            if not genres:
                genres = ['Unknown']
            
            # Increment genre counts
            for genre in genres:
                genre_counts[genre] += 1
            
            # Add song information
            songs.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'genre': genres[0]  # Using the first genre for simplicity
            })
    
    return jsonify({
        'genre_counts': dict(genre_counts),
        'songs': songs
    })

def calculate_genre_counts(songs):
    genre_counts = {}
    for song in songs.values():
        genre = song.get('genre', 'Unknown')
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1
    return genre_counts

def get_token():
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    
    return token_info

if __name__ == '__main__':
    app.run(debug=True, port=5001)
