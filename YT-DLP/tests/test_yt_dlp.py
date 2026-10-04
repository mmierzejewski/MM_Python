import importlib.util
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / 'yt-dlp.py'
SPEC = importlib.util.spec_from_file_location('video_downloader', SCRIPT_PATH)
video_downloader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(video_downloader)


def test_get_audio_tracks_accepts_missing_format_note(monkeypatch):
    class FakeYoutubeDL:
        def __init__(self, options):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def extract_info(self, url, download=False):
            return {
                'formats': [{
                    'format_id': 'audio-pl',
                    'format_note': None,
                    'ext': 'm4a',
                    'acodec': 'mp4a.40.2',
                    'vcodec': 'none',
                    'abr': 128,
                    'language': 'pl',
                }]
            }

    monkeypatch.setattr(video_downloader, 'YoutubeDL', FakeYoutubeDL)

    tracks = video_downloader.get_audio_tracks('https://example.com/video')

    assert len(tracks) == 1
    assert tracks[0]['format_id'] == 'audio-pl'
    assert tracks[0]['language_name'] == 'Polish'


def test_download_uses_selected_audio_without_fallback(monkeypatch, tmp_path):
    captured_options = {}

    class FakeYoutubeDL:
        def __init__(self, options):
            captured_options.update(options)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def extract_info(self, url, download=False):
            return {'id': 'video'}

        def prepare_filename(self, info):
            return str(tmp_path / 'video.mp4')

    monkeypatch.setattr(video_downloader, 'YoutubeDL', FakeYoutubeDL)

    succeeded = video_downloader.download_video(
        'https://example.com/video',
        tmp_path,
        audio_format_id='audio-pl',
    )

    assert succeeded is True
    assert captured_options['format'] == 'bestvideo+audio-pl'


@pytest.mark.parametrize(
    'contents',
    [
        '# My notes\nnot\ta\tcookie\trow\n',
        '# Netscape HTTP Cookie File\nmalformed cookie row\n',
        'domain\tTRUE\t/path\tTRUE\tnot-an-expiry\tname\tvalue\n',
        'domain\tMAYBE\t/path\tTRUE\t123\tname\tvalue\n',
    ],
)
def test_validate_cookie_file_rejects_malformed_files(tmp_path, contents):
    cookie_file = tmp_path / 'cookies.txt'
    cookie_file.write_text(contents, encoding='utf-8')

    assert video_downloader.validate_cookie_file(cookie_file) is False


def test_validate_cookie_file_accepts_netscape_cookie_row(tmp_path):
    cookie_file = tmp_path / 'cookies.txt'
    cookie_file.write_text(
        '# Netscape HTTP Cookie File\n'
        '.example.com\tTRUE\t/\tTRUE\t1798761600\tsession\ttoken\n',
        encoding='utf-8',
    )

    assert video_downloader.validate_cookie_file(cookie_file) is True


def test_validate_cookie_file_accepts_httponly_cookie(tmp_path):
    cookie_file = tmp_path / 'cookies.txt'
    cookie_file.write_text(
        '# Netscape HTTP Cookie File\n'
        '#HttpOnly_.example.com\tTRUE\t/\tTRUE\t1798761600\tsession\ttoken\n',
        encoding='utf-8',
    )

    assert video_downloader.validate_cookie_file(cookie_file) is True