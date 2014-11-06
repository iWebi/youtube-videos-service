from apiclient.discovery import build
from cache import Cache
import isodate
from easydict import EasyDict as edict
# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your
# project.
from util import flatten_list, load_file

DEVELOPER_KEY = "AIzaSyByR-19brS7IWGmskOHhXiaCpSUxWfQOeU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VIDEOS_CACHE = Cache()
FOUR_HOURS_IN_SECONDS = 4 * 60 * 60
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


class Video(dict):
    """
    Hold the necessary properties of the video returned in Http response to client. All unused properties are dropped-off
    before sending to UI
    """

    def __init__(self, id=None, publishedAt=None, thumbnail=None, title=None, duration=None):
        self['id'] = id
        self['thumbnail'] = thumbnail
        self['title'] = title
        self['duration'] = duration
        self['publishedAt'] = publishedAt


# strip off unused properties of the video entry in youtube api response. Check the same response returned by
# youtube in sample_response.json
# Also handles any filter requirements
def process_video_records(channel_videos):
    items = channel_videos.get("items", [])
    # video_durations = get_video_durations(items)
    processed_videos = []
    for item in items:
        # duration = video_durations[item['id']['videoId']]
        duration = 2500
        # consider videos longer than 40min
        if duration > 2400:
            processed_videos.append(
                Video(id=item.id.videoId,
                      thumbnail=item.snippet.thumbnails.default.url,
                      title=item.snippet.title,
                      duration=duration,
                      publishedAt=item.snippet.publishedAt
                )
            )
    return processed_videos


def _search_videos(channel_id, max_results):
    return youtube.search().list(
        part="snippet",
        order="date",
        # 2 months old videos
        # publishedAfter=(datetime.date.today() - datetime.timedelta(2*365/12)).isoformat()+'T00:00:00Z',
        type="video",
        videoDuration="long",
        channelId=channel_id,
        maxResults=max_results).execute()


def get_latest_videos_from_channel_ids(search_options):
    channel_ids = search_options['channelIds']
    max_results = search_options.get('maxResults', 50)
    videos = []
    for channel_id in channel_ids:
        channel_videos = VIDEOS_CACHE.get_from_cache(channel_id)
        if channel_videos is None:
            # channel_videos = _search_videos(channel_id=channel_id, max_results=max_results)
            channel_videos = edict(load_file('sample_response.json'))
            channel_videos = VIDEOS_CACHE.add_to_cache(key=channel_id, data=process_video_records(channel_videos),
                                                       duration=FOUR_HOURS_IN_SECONDS)
        videos.append(channel_videos)

    return flatten_list(videos)


def get_video_durations(channel_video_items):
    video_ids = []
    for item in channel_video_items:
        video_ids.append(item['id']['videoId'])
    id_param = ','.join(video_ids)
    content_details = youtube.videos().list(part="contentDetails", id=id_param).execute().get("items", [])
    duration_response_data = {}
    for content in content_details:
        duration_response_data[content['id']] = isodate.parse_duration(
            content['contentDetails']['duration']).total_seconds()
    return duration_response_data