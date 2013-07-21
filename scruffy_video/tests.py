import mock
import requests
import helpers
from .helpers import (get_video_type, get_video_type_and_id, 
    youtube_id, vimeo_id, get_embed_src, call_api, get_image_url)


TEST_VIMEO_URL = "https://vimeo.com/22733150"
TEST_YOUTUBE_URL_1 = "http://www.youtube.com/watch?v=SicQi0H925g"
TEST_YOUTUBE_URL_2 = "http://www.youtube.com/v/SicQi0H925g"
TEST_YOUTUBE_URL_3 = "http://www.youtu.be/SicQi0H925g"


def test_get_video_type():
    """ YouTube and Vimeo links should return their respective types. """
    for link in [TEST_YOUTUBE_URL_1, TEST_YOUTUBE_URL_2, TEST_YOUTUBE_URL_3]:
        assert get_video_type(link) == 'youtube'
    assert get_video_type(TEST_VIMEO_URL) == 'vimeo'
    assert get_video_type("http://foobar.com/whatever") == None


def test_get_video_type_and_id():
    assert get_video_type_and_id(TEST_VIMEO_URL) == ('vimeo', '22733150')


def test_youtube_id():
    """ Should return the video's ID regardless of the link's format. """
    for link in [TEST_YOUTUBE_URL_1, TEST_YOUTUBE_URL_2, TEST_YOUTUBE_URL_3]:
        assert youtube_id(link) == 'SicQi0H925g'


def test_vimeo_id():
    """ Should return the video's id """
    assert vimeo_id(TEST_VIMEO_URL) == '22733150'


def test_get_embed_src():
    """ Should return a url we can stick in an iframe src to create a player. """
    assert get_embed_src(TEST_VIMEO_URL) == "http://player.vimeo.com/video/22733150"
    assert get_embed_src(TEST_YOUTUBE_URL_1) == "http://www.youtube.com/embed/SicQi0H925g"


@mock.patch.object(requests, 'get')
def test_call_api(mock_get):
    """ Should call the right API and return parsed json. """
    resp = mock.MagicMock()
    resp.raise_for_status.return_value = None
    resp.content = u"""{"thats":"a wrap"}"""
    mock_get.return_value = resp
    content = call_api(TEST_VIMEO_URL)
    assert mock_get.call_args[0][0] == 'http://vimeo.com/api/v2/video/22733150.json'
    assert content == {'thats': 'a wrap'}


@mock.patch.object(helpers, 'call_api')
def test_get_image_url_for_vimeo(mock_api):
    """ Should return the url of the main thumbnail found in the api call. """
    mock_api.return_value = [{
        'thumbnail_large': 'http://b.vimeocdn.com/ts/147/229/147229620_640.jpg',
    }]

    url = get_image_url(TEST_VIMEO_URL)
    assert url == "http://b.vimeocdn.com/ts/147/229/147229620_640.jpg"


@mock.patch.object(helpers, 'call_api')
def test_get_image_url_for_youtube(mock_api):
    """ Should return the url of the main thumbnail found in the api call. """
    mock_api.return_value = {'encoding': 'UTF-8',
                             'entry': {
                               'media$group': {
                                   'media$thumbnail': [
                                        {'height': 360,
                                        'time': '00:02:28.500',
                                        'url': 'http://i1.ytimg.com/vi/SicQi0H925g/0.jpg',
                                        'width': 480},
                                       {'height': 90,
                                        'time': '00:01:14.250',
                                        'url': 'http://i1.ytimg.com/vi/SicQi0H925g/1.jpg',
                                        'width': 120}
                                    ],
                                },
                            },}

    url = get_image_url(TEST_YOUTUBE_URL_3)
    assert url == "http://i1.ytimg.com/vi/SicQi0H925g/0.jpg"

