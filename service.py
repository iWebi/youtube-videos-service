from apiclient.discovery import build



# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your
# project.
DEVELOPER_KEY = "AIzaSyByR-19brS7IWGmskOHhXiaCpSUxWfQOeU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_latest_videos_from_channel(search_options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    max_results = search_options.get('maxResults', 2)
    search_response = youtube.search().list(
        part="snippet",
        order="date",
        type="video",
        videoDuration="long",
        channelId=search_options['channelId'],
        maxResults=max_results).execute()
    return search_response.get("items", [])


