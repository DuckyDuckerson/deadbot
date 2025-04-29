import sqlite3
import requests


def create_database():
    conn = sqlite3.connect('artist_data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS artists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    popularity INTEGER,
                    followers INTEGER,
                    timestamp TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS tracks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    popularity INTEGER,
                    artist_id TEXT,
                    timestamp TEXT)''')

    conn.commit()
    conn.close()


def insert_artist_data(name, popularity, followers, timestamp):
    conn = sqlite3.connect('artist_data.db')
    c = conn.cursor()

    c.execute('''INSERT INTO artists (name, popularity, followers, timestamp)
                 VALUES (?, ?, ?, ?)''', (name, popularity, followers, timestamp))

    conn.commit()
    conn.close()

def insert_track_data(name, popularity, artist_id, timestamp):
    conn = sqlite3.connect('artist_data.db')
    c = conn.cursor()

    c.execute('''INSERT INTO tracks (name, popularity, artist_id, timestamp)
                 VALUES (?, ?, ?, ?)''', (name, popularity, artist_id, timestamp))

    conn.commit()
    conn.close()


def get_current_timestamp():
    response = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC')
    current_time = response.json()['datetime']
    return current_time


def store_artist_data(artist_data):
    name = artist_data['name']
    popularity = artist_data['popularity']
    followers = artist_data['followers']['total']

    timestamp = get_current_timestamp()

    insert_artist_data(name, popularity, followers, timestamp)


def store_track_data(track_data, artist_id):
    name = track_data['name']
    popularity = track_data['popularity']

    timestamp = get_current_timestamp()

    insert_track_data(name, popularity, artist_id, timestamp)


def fetch_data():
    conn = sqlite3.connect('artist_data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM artists")

    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()
