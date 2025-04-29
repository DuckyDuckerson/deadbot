import requests
import base64
from database.sql_bs.sqlfunctions import insert_artist_data as insert_artist_data
from database.sql_bs.sqlfunctions import insert_track_data as insert_track_data
import datetime


CLIENT_ID = 'db1e53dfbfdc4ebe83c39a8bc7ec1d81'
CLIENT_SECRET = '5b034ad872e548c0aa4f90d9fe0cc528'


def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    auth_data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, headers=auth_header, data=auth_data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        print("Error fetching access token")
        return None


def get_artist_data():
    access_token = get_access_token()
    artist_id = '2MC67O2xkG8buXrq1cRGCN'
    artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(artist_url, headers=headers)

    if response.status_code == 200:
        artist_data = response.json()
        name = artist_data['name']
        popularity = artist_data['popularity']
        followers = artist_data['followers']['total']
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        insert_artist_data(name, popularity, followers, timestamp)
    else:
        print("Error fetching artist data")


def get_top_tracks():
    access_token = get_access_token()
    artist_id = '2MC67O2xkG8buXrq1cRGCN'
    top_tracks_url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(top_tracks_url, headers=headers)

    if response.status_code == 200:
        top_tracks_data = response.json()
        for track in top_tracks_data['tracks']:
            track_name = track['name']
            track_popularity = track['popularity']
            track_id = track['id']
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


            insert_track_data(track_name, track_popularity, track_id, timestamp)
    else:
        print("Error fetching top tracks")
