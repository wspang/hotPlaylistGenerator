import requests, spotipy
from api_authentication import spotify_auth, get_aws_secret

# set global authentication for spotify API
# credentials are stored in AWS Secret Manager.
cred = get_aws_secret("hpg-keys","us-west-2")["spotify"]
token=spotify_auth(
        client_id=cred['clientid'],
        client_secret=cred['clientsecret'],
        user=cred['user'])
AUTH={'Authorization': f'Bearer {token}'}

# spotify APIs wrapped into functions

def get_track_uri(artist, track):
    # given an artist and song title, return the top track uri
    kw = f"track:{track}%20artist:{artist}"
    url = f"https://api.spotify.com/v1/search?q={kw}&type=track&limit=1"
    r = requests.get(url=url, headers=AUTH)
    
    # parse for track uri
    try:
        uri = r.json()['tracks']['items'][0]['uri']
        return uri
    except Exception:
        print(f"Could not find a match for {artist} - {track}")
        return None

def replace_tracks(playlist, tracks):
    # given a list of track uris, replace playlist with all those tracks
    url = f"https://api.spotify.com/v1/playlists/{playlist}/tracks"
    requests.put(url=url, headers=AUTH, json={"uris": tracks})
    return

