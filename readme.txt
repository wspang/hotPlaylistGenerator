    __    __    ____      ______
   /  /__/  /  |    |    /_   _/
  /   __   /   | || |     /  / 
 /__/  /__/    |____|    /__/   PLAYLIST GENERATOR
 _________________________________________________
 *************************************************
 @Author: Will Spangler

___THE APPLICATION
get a daily ingest of whats `hot` from the community.
`Hot` music is ingested from Reddit music subreddit's
on their hot posts. Posts are filtered to identify
songs and artists. Using Spotify APIs, daily playlists 
are truncated per subreddit. Track URIs are found
via the search API.
Additionally, performance and track details will be
tracked in a SQL database. This will serve to:
  (1) track how well the app can identify tracks
  (2) track how often tracks are posted in hot section
  (3) cross check spotify popularity to what makes a
      a reddit track go hot
  (4) gather insights on other stuff...

___PURPOSE
Have a constant daily stream of music for what is hot
in the community. This is a community supported playlist,
Data will also be acquired throughout time to enhance
more features and insight to community taste.

___PROCESSES
-Application that pings music subreddits four times a day
to ingest post titles and upvotes/downvotes.

- Once a day a playlist is generated on Spotify (through
search APIs and playlist APIs) based on the ingest

- All metrics (4x daily) are loaded into a relational DB.
The relational DB will support metric insight and visuals.

___ARCHITECTURE AWS
Ingest: Lambda functions on CRON schedule. (free)
Backend: AWS RDS db.t2.micro DB (free 20GB)
Notifications: AWS SNS (1 mil free)
Credentials: AWS Secrets Manager ($.4/month)

