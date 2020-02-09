import boto3, json, praw
from spotipy import util

def get_aws_secret(secret_name, region):
    # Retrieve the AWS secret from secret manager to use in below
    # authentication function
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region)    
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret_data = get_secret_value_response['SecretString']
    secret_data = json.loads(secret_data)
    return secret_data

def reddit_obj(client_id, client_secret, user):
    # Create a reddit object to make API calls with
    user_agent = f"script:hotPlaylistGenerator:v01.0 (by u/{user}"
    reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent)
    return reddit

def spotify_auth(client_id, client_secret, user):
    # spotify credential jazz for their API

    #parameters in request for access token
    redirect_uri = "https://localhost:8080"
    scope = "playlist-modify-public"
    
    # token generation 
    token = util.prompt_for_user_token(
            username=user, 
            scope=scope,
            client_id=client_id, 
            client_secret=client_secret, 
            redirect_uri=redirect_uri)
    
    return token

def sql_db():
    # connect to sql db
    return

