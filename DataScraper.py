import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build, json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_version = "v3"
api_service_name = "youtube"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)

credentials = flow.run_console()

youtube = build(api_service_name, api_version, credentials=credentials)

# The following lists will store any essential data
nextPageToken = None
vid_privacy = []
vid_thumbs = []
vid_details = []
vid_title = []

total_vids = 0
public_vids = 0
unspecified = 0

print('\nExample: PLLjmbh6XPGK4ISY747FUHXEl9lBxre4mM')
pID = input('Enter playlist ID string: ')

while True:
    request = youtube.playlistItems().list(
        part="contentDetails, snippet, status",
        maxResults=50,
        playlistId=pID,
        pageToken=nextPageToken
    )

    response = request.execute()

    for item in response['items']:
        total_vids+=1

        vid_details.append(item['contentDetails']['videoId'])
        vid_title.append(item['snippet']['title'])
        vid_thumbs.append(item['snippet']['thumbnails'])

        if item['status']['privacyStatus'] == 'public':
            vid_privacy.append(item['status']['privacyStatus'])
            public_vids+=1
        if item['status']['privacyStatus'] != 'public':
            vid_privacy.append(item['status']['privacyStatus'])
            unspecified+=1

    nextPageToken = response.get('nextPageToken')

    if not nextPageToken:
        break

print('\nTotal videos: {}\nTotal public videos: {}\nTotal Unavailable Videos: {}'.format(total_vids,
                                                                                         public_vids, unspecified))

listString = ""
vidFile = open("playlistDetails.txt", "w+", encoding="utf-8")

for x in range(total_vids):
    listString += vid_title[x] + "\n"
    listString += vid_details[x] + "\n"
    vidThumbs = json.dumps(vid_thumbs[x])
    listString += vidThumbs + "\n"

    vidFile.write(listString)
    listString = ""

vidFile.close()
