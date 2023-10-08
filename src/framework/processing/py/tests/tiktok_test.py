"""
- test file type error
- test data not found error
- grouping by hour
    - multiple columns


"""

import json
import zipfile
import io
import tempfile
from pathlib import Path
from dataclasses import dataclass
from inspect import cleandoc
import pandas as pd
from pandas.testing import assert_frame_equal
from port.api import commands
from port import script


complete_contents = {
    "Profile": {
            "Profile Information": {
                "ProfileMap": {"userName": "jane_doe", "likesReceived": "77"}
            }
        },
        "Direct Messages": {
            "Chat History": {
                "ChatHistory": {
                    "Chat History with john_doe:": [
                        {
                            "Date": "2023-01-08 17:38:59",
                            "From": "john_doe",
                            "Content": "https://www.tiktokv.com/share/video/7167866677751860486/",
                        },
                        {
                            "Date": "2023-01-08 17:38:59",
                            "From": "jane_doe",
                            "Content": "👍",
                        },
                        {
                            "Date": "2023-01-08 18:12:45",
                            "From": "john_doe",
                            "Content": "cool",
                        },
                        {
                            "Date": "2023-01-08 18:12:55",
                            "From": "john_doe",
                            "Content": "https://www.tiktokv.com/share/video/7175594838077787434/",
                        },
                    ]
                }
            }
        },
        "Activity": {
            "Follower List": {"FansList": [{"Date": "2023-01-14 18:01:16"}]},
            "Following List": {
                "Following": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                ]
            },
            "Like List": {
                "ItemFavoriteList": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                ]
            },
            "Video Browsing History": {
                "VideoList": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                    {"Date": "2023-01-14 18:03:16"},
                    {"Date": "2023-01-14 18:04:16"},
                ]
            },
        },
        "Video": {
            "Videos": {
                "VideoList": [
                    {
                        "Likes": "1",
                        
                        "Date": "2023-01-14 18:01:16"},
                    {
                        "Likes": "1",
                        
                        "Date": "2023-01-14 18:02:16"},
                    {
                        "Likes": "1",
                        
                        "Date": "2023-01-14 18:03:16"},
                ]
            }
        },
        "Comment": {
            "Comments": {
                "CommentList": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                    {"Date": "2023-01-14 18:03:16"},
                ]
            }
        },
}

def get_test_file(name):
    return str(Path(__file__).parent.joinpath(name))


def assert_frame_str_equal(df1, df2):
    assert cleandoc(df1) == str(df2)


@dataclass
class PayloadString:
    value: str
    __type__: str = "PayloadString"


def test_wrong_file_type_is_handled():
    generator = script.process("test-session")
    file_prompt = next(generator)
    assert isinstance(file_prompt, commands.CommandSystemDonate)
    assert {
        "__type__": "CommandSystemDonate",
        "json_string": '[{ "message": "user entered script" }]',
        "key": "test-session-tracking",
    } == file_prompt.toDict()
    n = next(generator)
    assert {
        "__type__": "CommandUIRender",
        "page": {
            "__type__": "PropsUIPageDonation",
            "body": {
                "__type__": "PropsUIPromptFileInput",
                "description": {
                    "translations": {
                        "en": "Please follow the "
                        "download "
                        "instructions and "
                        "choose the file "
                        "that you stored on "
                        "your device. Click "
                        "“Skip” at the right "
                        "bottom, if you do "
                        "not have a TikTok "
                        "file. ",
                        "nl": "Volg de download "
                        "instructies en kies "
                        "het bestand dat u "
                        "opgeslagen heeft op "
                        "uw apparaat. Als u "
                        "geen TikTok bestand "
                        "heeft klik dan op "
                        "“Overslaan” rechts "
                        "onder.",
                    }
                },
                "extensions": "application/zip, text/plain",
            },
            "footer": {"__type__": "PropsUIFooter", "progressPercentage": 0},
            "header": {
                "__type__": "PropsUIHeader",
                "title": {"translations": {"en": "TikTok", "nl": "TikTok"}},
            },
            "platform": "TikTok",
        },
    } == n.toDict()

    payload = PayloadString(value=get_test_file("minimal.zip"))
    n = generator.send(payload)

    assert {
        "__type__": "CommandUIRender",
        "page": {
            "__type__": "PropsUIPageDonation",
            "body": {
                "__type__": "PropsUIPromptConfirm",
                "cancel": {"translations": {"en": "Continue", "nl": "Verder"}},
                "ok": {"translations": {"en": "Try again", "nl": "Probeer opnieuw"}},
                "text": {
                    "translations": {
            "en": "Unfortunately, we cannot process your data. Please make sure that you selected JSON as a file format when downloading your data from TikTok.",
            "nl": "Helaas kunnen we uw gegevens niet verwerken. Zorg ervoor dat u JSON heeft geselecteerd als bestandsformaat bij het downloaden van uw gegevens van TikTok.",
                    }
                },
            },
            "footer": {"__type__": "PropsUIFooter", "progressPercentage": 0},
            "header": {
                "__type__": "PropsUIHeader",
                "title": {"translations": {"en": "TikTok", "nl": "TikTok"}},
            },
            "platform": "TikTok",
        },
    } == n.toDict()


def test_summary_table():
    data = {
        "Profile": {
            "Profile Information": {
                "ProfileMap": {"username": "jane_doe", "likesReceived": "77"}
            }
        },
        "Direct Messages": {
            "Chat History": {
                "ChatHistory": {
                    "Chat History with john_doe:": [
                        {
                            "Date": "2023-01-08 17:38:59",
                            "From": "john_doe",
                            "Content": "https://www.tiktokv.com/share/video/7167866677751860486/",
                        },
                        {
                            "Date": "2023-01-08 17:38:59",
                            "From": "jane_doe",
                            "Content": "👍",
                        },
                        {
                            "Date": "2023-01-08 18:12:45",
                            "From": "john_doe",
                            "Content": "cool",
                        },
                        {
                            "Date": "2023-01-08 18:12:55",
                            "From": "john_doe",
                            "Content": "https://www.tiktokv.com/share/video/7175594838077787434/",
                        },
                    ]
                }
            }
        },
        "Activity": {
            "Follower List": {"FansList": [{"Date": "2023-01-14 18:01:16"}]},
            "Following List": {
                "Following": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                ]
            },
            "Like List": {
                "ItemFavoriteList": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                ]
            },
            "Video Browsing History": {
                "VideoList": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                    {"Date": "2023-01-14 18:03:16"},
                    {"Date": "2023-01-14 18:04:16"},
                ]
            },
        },
        "Video": {
            "Videos": {
                "VideoList": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                    {"Date": "2023-01-14 18:03:16"},
                ]
            }
        },
        "Comment": {
            "Comments": {
                "CommentList": [
                    {"Date": "2023-01-14 18:01:16"},
                    {"Date": "2023-01-14 18:02:16"},
                    {"Date": "2023-01-14 18:03:16"},
                ]
            }
        },
    }
    result = script.extract_summary_data(data)
    assert "tiktok_summary" == result.id
    assert "Summary information" == result.title.translations["en"]

    reference = """
             Description Number
    0          Followers      1
    1          Following      2
    2     Likes received     77
    3      Videos posted      3
    4        Likes given      2
    5    Comments posted      0
    6      Messages sent      0
    7  Messages received      4
    8     Videos watched      4
    """
    print(result.data_frame)
    assert_frame_str_equal(reference, result.data_frame)


def test_summary_table_with_minimal_data():
    data = {}
    reference = """
             Description  Number
    0          Followers       0
    1          Following       0
    2     Likes received       0
    3      Videos posted       0
    4        Likes given       0
    5    Comments posted       0
    6      Messages sent       0
    7  Messages received       0
    8     Videos watched       0
    """
    result = script.extract_summary_data(data)
    assert_frame_str_equal(reference, result.data_frame)


def test_video_posts_table():
    data = {
        "Video": {
            "Videos": {
                "VideoList": [
                    # Single video
                    {
                        "Date": "2022-12-29 12:11:00",
                        "Likes": "1",
                    },
                    # Videos in the same hour
                    {
                        "Date": "2022-12-29 13:11:00",
                        "Likes": "1",
                    },
                    {
                        "Date": "2022-12-29 13:52:00",
                        "Likes": "1",
                    },
                    # No likes
                    {
                        "Date": "2022-12-30 02:11:00",
                        "Likes": "1",
                    },
                ]
            }
        },
    }

    result = script.extract_video_posts(data)
    assert "tiktok_posts" == result.id
    assert "Video posts" == result.title.translations["en"]

    reference = """
             Date Timeslot  Videos  Likes received
    0  2022-12-29    12-13       1               1
    1  2022-12-29    13-14       2               2
    2  2022-12-30      2-3       1               1
    """
    assert_frame_str_equal(reference, result.data_frame)


def test_video_post_table_returns_none_without_posts():
    assert script.extract_video_posts({}) is None


def test_comments_and_likes_table():
    data = {
        "Comment": {
            "Comments": {
                "CommentsList": [
                    # One comment
                    {"Date": "2023-01-14 18:01:16"},
                    # Multiple comments
                    {"Date": "2023-01-15 19:12:16"},
                    {"Date": "2023-01-15 19:13:16"},
                    {"Date": "2023-01-15 19:14:16"},
                ]
            }
        },
        "Activity": {
            "Like List": {
                "ItemFavoriteList": [
                    {
                        "Date": "2023-01-14 02:11:01",
                    },
                    {
                        "Date": "2023-01-14 02:11:01",
                    },
                    {
                        "Date": "2023-01-14 07:45:01",
                    },
                    {
                        "Date": "2023-01-14 18:11:01",
                    },
                ]
            }
        },
    }
    result = script.extract_comments_and_likes(data)
    assert "tiktok_comments_and_likes" == result.id
    assert "Comments and likes" == result.title.translations["en"]

    reference = """
             Date Timeslot  Comment posts  Likes given
    0  2023-01-14      2-3              0            2
    1  2023-01-14      7-8              0            1
    2  2023-01-14    18-19              1            1
    3  2023-01-15    19-20              3            0
    """
    assert_frame_str_equal(reference, result.data_frame)


def test_comments_and_likes_table_returns_none_without_posts():
    assert script.extract_comments_and_likes({}) is None


def test_comment_activity_table():
    result = script.extract_comment_activity(tiktok_data)
    assert "tiktok_comment_activity" == result.id
    assert "Session information" == result.title.translations["en"]

    reference = pd.DataFrame.from_dict({})

    print(result.data_frame.to_dict())

    assert_frame_str_equal(reference, result.data_frame)


def test_comment_activity_table_returns_none_without_posts():
    assert script.extract_comment_activity({}) is None


def test_videos_liked_table():
    result = script.extract_videos_liked(tiktok_data)
    assert "tiktok_videos_liked" == result.id
    assert "Session information" == result.title.translations["en"]

    reference = pd.DataFrame.from_dict({})

    print(result.data_frame.to_dict())

    assert_frame_str_equal(reference, result.data_frame)


def test_videos_liked_table_returns_none_without_posts():
    assert script.extract_videos_liked({}) is None


def test_videos_viewed_table():
    data = {
        "Activity": {
            "Video Browsing History": {
                "VideoList": [
                    {"Date": "2022-11-29 04:44:00"},
                    {"Date": "2022-11-29 04:44:01"},
                    {"Date": "2022-11-29 05:14:01"},
                ]
            }
        }
    }
    result = script.extract_videos_viewed(data)
    assert "tiktok_videos_viewed" == result.id
    assert "Video views" == result.title.translations["en"]

    reference = """
             Date Timeslot  Videos
    0  2022-11-29      4-5       2
    1  2022-11-29      5-6       1
    """

    assert_frame_str_equal(reference, result.data_frame)


def test_videos_viewed_table_returns_none_without_posts():
    assert script.extract_videos_viewed({}) is None


def test_session_info_table():
    data = {
        "Video": {
            "Videos": {
                "VideoList": [
                    {"Date": "2023-01-01 10:11:12"},
                    {"Date": "2023-01-01 10:12:12"},
                ]
            }
        },
        "Activity": {
            "Video Browsing History": {"VideoList": [{"Date": "2023-01-01 10:13:12"}]}
        },
        "Comment": {"Comments": {"CommentsList": [{"Date": "2023-01-01 10:14:12"}]}},
    }

    result = script.extract_session_info(data)
    assert "tiktok_session_info" == result.id
    assert "Session information" == result.title.translations["en"]

    reference = """
                  Start  Duration (in minutes)
    0  2023-01-01 10:11                    3.0
    """
    assert_frame_str_equal(reference, result.data_frame)


def test_direct_messages_table():
    data = {
        "Profile": {"Profile Information": {"ProfileMap": {"userName": "jane_doe"}}},
        "Direct Messages": {
            "Chat History": {
                "ChatHistory": {
                    "Chat History with john_doe:": [
                        {
                            "Date": "2023-01-08 17:38:59",
                            "From": "john_doe",
                            "Content": "https://www.tiktokv.com/share/video/7167866677751860486/",
                        },
                        {
                            "Date": "2023-01-08 17:38:59",
                            "From": "jane_doe",
                            "Content": "👍",
                        },
                        {
                            "Date": "2023-01-08 18:12:45",
                            "From": "john_doe",
                            "Content": "cool",
                        },
                        {
                            "Date": "2023-01-08 18:12:55",
                            "From": "john_doe",
                            "Content": "https://www.tiktokv.com/share/video/7175594838077787434/",
                        },
                    ]
                }
            }
        },
    }
    result = script.extract_direct_messages(data)
    assert "tiktok_direct_messages" == result.id
    assert "Direct Message Activity" == result.title.translations["en"]

    reference = """
       Anonymous ID              Sent
    0             2  2023-01-08 17:38
    1             1  2023-01-08 17:38
    2             2  2023-01-08 18:12
    3             2  2023-01-08 18:12
    """
    print(result.data_frame)
    assert_frame_str_equal(reference, result.data_frame)


def test_comment_activity_table():
    data = {
        "Comment": {
            "Comments": {
                "CommentsList": [
                    {"Date": "2023-03-26 15:40:06", "Comment": "🥰🥰"},
                    {"Date": "2023-03-18 12:52:35", "Comment": "Like ut!"},
                    {"Date": "2023-03-11 15:06:35", "Comment": "Cute!"},
                    {"Date": "2023-03-11 15:05:52", "Comment": "Nice!"},
                    {"Date": "2023-03-03 14:22:03", "Comment": "😅😅"},
                ]
            }
        }
    }
    result = script.extract_comment_activity(data)
    assert "tiktok_comment_activity" == result.id
    assert "Comment Activity" == result.title.translations["en"]

    reference = """
              Posted on
    0  2023-03-26 15:40
    1  2023-03-18 12:52
    2  2023-03-11 15:06
    3  2023-03-11 15:05
    4  2023-03-03 14:22
    """
    assert_frame_str_equal(reference, result.data_frame)


def test_videos_liked_table():
    data = {
        "Activity": {
            "Favorite Videos": {
                "FavoriteVideoList": [
                    {
                        "Date": "2023-03-26 15:39:28",
                        "Link": "https://www.tiktokv.com/share/video/7199666315362061573/",
                    },
                    {
                        "Date": "2023-03-18 12:53:14",
                        "Link": "https://www.tiktokv.com/share/video/7209355519562140933/",
                    },
                    {
                        "Date": "2023-03-18 12:53:11",
                        "Link": "https://www.tiktokv.com/share/video/7209700824841489669/",
                    },
                    {
                        "Date": "2023-03-11 15:06:37",
                        "Link": "https://www.tiktokv.com/share/video/7191669641897463082/",
                    },
                ]
            }
        }
    }
    result = script.extract_videos_liked(data)
    assert "tiktok_videos_liked" == result.id
    assert "Videos liked" == result.title.translations["en"]

    reference = """
                  Liked                                               Link
    0  2023-03-26 15:39  https://www.tiktokv.com/share/video/7199666315...
    1  2023-03-18 12:53  https://www.tiktokv.com/share/video/7209355519...
    2  2023-03-18 12:53  https://www.tiktokv.com/share/video/7209700824...
    3  2023-03-11 15:06  https://www.tiktokv.com/share/video/7191669641...
    """
    print(result.data_frame)
    assert_frame_str_equal(reference, result.data_frame)


def test_timezone_to_uk():
    assert False


def test_get_json_data_from_zip_with_invalid_json():
    f = make_zip({"test.json": "testing"})
    assert [] == script.get_json_data_from_zip(f)


def test_get_json_data_from_zip_with_non_tiktok_json():
    f = make_zip({"test.json": "{}"})
    assert [] == script.get_json_data_from_zip(f)


def test_get_json_data_from_zip_with_valid_tiktok_json():
    tiktok_data = {
        "Profile": {"Profile Information": {"ProfileMap": {"userName": "test"}}}
    }
    f = make_zip({"test.json": json.dumps(tiktok_data)})
    assert [tiktok_data] == script.get_json_data_from_zip(f)


def test_extract_tiktok_data_works_with_zip_files():
    with tempfile.NamedTemporaryFile() as f:
        make_zip({"test.json": json.dumps(complete_contents)}, f)
        f.flush()
        result = script.extract_tiktok_data(f.name)
        assert len(result) > 1

def test_extract_tiktok_data_works_with_json_files():
    with tempfile.NamedTemporaryFile(mode="w+t") as f:
        json.dump(complete_contents, f)
        f.flush()
        result = script.extract_tiktok_data(f.name)
        assert len(result) > 1


def make_zip(contents, out=None):
    if out is None:
        out = io.BytesIO()
    z = zipfile.ZipFile(out, mode="w")
    for filename, data in contents.items():
        z.writestr(filename, data)
    z.close()
    out.seek(0)
    return out
