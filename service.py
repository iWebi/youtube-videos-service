from apiclient.discovery import build
from cache import Cache

# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your
# project.
DEVELOPER_KEY = "AIzaSyByR-19brS7IWGmskOHhXiaCpSUxWfQOeU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VIDEOS_CACHE = Cache()
FOUR_HOURS_IN_SECONDS = 4 * 60 * 60

# Hold the necessary properties of the video returned in Http response to client. All unused properties are dropped-off
# before sending to UI
class Video(dict):
    def __init__(self, thumbnail=None, title=None):
        self[thumbnail] = thumbnail
        self[title] = title


# strip off unused properties of the video entry in youtube api response. Check the same response returned by
# youtube in sample_response.json
# Also handles any filter requirements
def process_video_record(channel_videos):
    items = channel_videos.get("items", [])
    processed_videos = []
    for item in items:
        processed_videos.append(Video(thumbnail=item.snippet.thumbnails.default, title=item.snippet.title))
    return processed_videos


def get_latest_videos_from_channel_ids(search_options):
    youtube = None
    channel_ids = search_options['channelIds']
    max_results = search_options.get('maxResults', 2)
    videos = []
    for channel_id in channel_ids:
        channel_videos = VIDEOS_CACHE.get_from_cache(channel_id)
        if channel_videos is None:
            if youtube is None:
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                                developerKey=DEVELOPER_KEY)
            channel_videos = youtube.search().list(
                part="snippet",
                order="date",
                type="video",
                videoDuration="long",
                channelId=channel_id,
                maxResults=max_results).execute()
        videos.append(VIDEOS_CACHE.add_to_cache(key=channel_id, data=process_video_record(channel_videos),
                                                duration=FOUR_HOURS_IN_SECONDS))
    return videos