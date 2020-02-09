import requests, json, praw
from api_authentication import reddit_obj, get_aws_secret

# Create the Reddit object (read only) to use in API calls
cred = get_aws_secret("hpg-keys","us-west-2")["reddit"]
REDDIT = reddit_obj(
        client_id=cred['clientid'],
        client_secret=cred['clientsecret'],
        user=cred['user'])

def get_posts(subreddit_name, post_count):
    # retrieve post titles  from subreddits and return as a list to process.
    titles = [r.title for r in REDDIT.subreddit(subreddit_name).hot(limit=post_count)]
    return titles

def parse_title(title):
    """Try to parse a title for a song name and artist
       This is based off common naming convention used in subreddit... no ML yet :)
       Rules:::
           - any post starting with [FRESH] will follow with <ARTIST> - <SONG> ...
           - posts with <NAME> - <WORDS> is almost always a song
           - any titles with `ft.` will have a feature, meaning a song"""
    # Rule One: look for a dash within post title or if it is a discussion post
    dash_loc = title.find('-')
    if dash_loc == -1 or title[:12].lower() == '[discussion]':
        return None
    else:
        pass
    # Look out for content after brackets
    if title[0] == "[":
        artist = title[(title.find(']')+2) : (dash_loc)]
        song = title[(dash_loc+1) :]
    # Look out for a regular song post
    else:
        artist = title[: dash_loc]
        song = title[dash_loc+1 :]

    # Now parse any crap off the end of a post
    info_loc = title.rfind('(')
    # has -1 index if there is none. If it comes after dash, it is info.
    song = song if info_loc < dash_loc else title[(dash_loc+1) : (info_loc)]
    # trim more crap off if in brackets
    song = song if song.find('[') == -1 else song[: song.find('[')-1]
    
    # handle features on a track.
    artist = artist if "ft." not in artist else artist[: artist.find('ft.')]
    
    # return dictionary of song posts
    song_post = {"artist":artist, "track": song}
    print(f"\nSong post we found so far:\n\t{song_post}")
    return song_post

