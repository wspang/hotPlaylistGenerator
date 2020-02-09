from reddit_ingest import get_posts, parse_title
from spotify_apis import get_track_uri, replace_tracks

# Main file for executing flow.

def handler(event, context):
    # Get incoming payload to run job
    payload = event['body']
    post_count = payload['post_count']

    # ingest titles from reddit, one sub at a time. Can parallelize later.
    # TODO: look into kicking off separate threads across functions to update metrics DB
    for i in payload['playlists']:

        # parse out dictionary
        sub, playlist_uri = i['sub'], i['uri']

        print(f"Ingesting {sub}")
        posts = get_posts(subreddit_name=sub, post_count=post_count)

        # parse titles and filter out nulls that did not qualify as tracks
        titles = list(filter(None, map(parse_title, posts)))
        print(f"Received {len(titles)} tracks for {sub}")
        # TODO: write out titles to int. storage

        # TODO: kick off spotify apis in separate lambda later on
        # search URIs of tracks 
        uris = [get_track_uri(artist=t['artist'], track=t['track']) for t in titles]
        uris = list(filter(None, uris))

        # Replace tracks in the playlist with the new list of track URIs
        replace_tracks(playlist=playlist_uri, tracks=uris)

# local running
if __name__=='__main__':
    payload = {
            "post_count": 50,
            "playlists": [
                {"sub":"HipHopHeads", "playlist": "hotHipHop", "uri":"5vrlPDIae4QQhdGHw7KFJc"},
                {"sub":"ListenToThis", "playlist": "hotCheckItOut", "uri":"2E6NKwGiLOkSaIocSff39Y"},
                {"sub":"Music", "playlist": "hotRandom", "uri":"7lRweQeV04LmHJggtLZr3n"},
                #{"sub":"Trap", "playlist": "", "uri":""},
                ]
             }
            
    event, context = {"body": payload}, None
    handler(event, context)

