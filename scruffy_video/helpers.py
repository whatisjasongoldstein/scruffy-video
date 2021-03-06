import requests

try:
    import json
except ImportError:
    import simplejson as json

def get_video_type(link):
    """ Takes a url and decides if it's Vimeo or YouTube.
    Returns None for unkown types. """
    if 'vimeo.com/' in link:
        return 'vimeo'
    elif 'youtube.com/' in link or 'youtu.be' in link:
        return 'youtube'
    return None


def get_video_type_and_id(link):
    """ Returns the type and id as a tuple."""
    kind = get_video_type(link)
    if kind == 'vimeo':
        return (kind, vimeo_id(link))
    if kind == 'youtube':
        return (kind, youtube_id(link))
    return None


def youtube_id(link):
    """ Get the YouTube ID, regardless of format. """
    start_flags = ['youtu.be/', "?v=", "/v/"]
    start_id = None
    for flag in start_flags:
        if flag in link:
            start_id = link.find(flag) + len(flag)
            break
    if not start_id: # If it's not a valid URL
        return False
    the_id = link[start_id:start_id+11]
    return the_id


def vimeo_id(link):
    if "vimeo.com/" in link:
        return link[link.find("vimeo.com/")+10:]
    return False


def get_embed_src(link):
    """ Gets the source for an iframe to embed. """
    origin = get_video_type(link)
    if origin == 'vimeo':
        return "https://player.vimeo.com/video/%s" % vimeo_id(link)
    elif origin == 'youtube':
        return "//www.youtube.com/embed/%s" % youtube_id(link)
    else:
        return False


def call_api(link, keys=None):
    """ Get the API contents back. """
    keys = keys or {}

    API_FORMATS = {
        'vimeo': "http://vimeo.com/api/v2/video/{id}.json",
        'youtube': "https://www.googleapis.com/youtube/v3/videos?id={id}&key={key}&part=snippet,contentDetails,statistics,status"
    }
    kind, the_id = get_video_type_and_id(link)

    if kind in ["youtube",] and not keys.get(kind, False):
        raise Exception("An API key is required for {}".format(kind))

    if not kind or not the_id:
        return False
    api_link = API_FORMATS[kind].format(id=the_id, key=keys.get(kind, None))
    resp = requests.get(api_link, timeout=5)
    resp.raise_for_status()
    return json.loads(resp.content)


def get_image_url(link):
    """ Returns a url for the video's cover image. """
    video_type = get_video_type(link)
    if video_type == 'vimeo':
        data = call_api(link)
        image_link = data[0]['thumbnail_large']
    elif video_type == 'youtube':
        # YouTube sucks, and the max version isn't always available
        image_link = "http://img.youtube.com/vi/{}/maxdefault.jpg".format(youtube_id(link))
        if requests.get(image_link).status_code != 200:
            image_link = "http://img.youtube.com/vi/{}/hqdefault.jpg".format(youtube_id(link))
    else:
        raise ValueError('{} is not supported.'.format(video_type))
    return image_link

