"""Get song titles and artists from Spotify playlist"""

import csv
import logging
import os
import re

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# load credentials from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
OUTPUT_DIR = "data"
OUTPUT_FILE_NAME = "track_info.csv"

# change for your target playlist
PLAYLIST_LINK = (
    "https://open.spotify.com/playlist/6jAarBZaMmBLnSIeltPzkz?si=d42be5c6ec194bb9"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)


def get_playlist_uri_from_link(playlist_link: str) -> str:
    """Get Spotify playlist URI from Spotify playlist link

    The URI is the bit after 'playlist' but before the '?'

    Example:
    get_playlist_uri_from_link(
        "https://open.spotify.com/playlist/6jAarBZaMmBLnSIeltPzkz?si=d42be5c6ec194bb9"
    )
    >>> "6jAarBZaMmBLnSIeltPzkz"

    """
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist_link):
        return match.groups()[0]
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")


if __name__ == "__main__":

    # authenticate
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )

    # create spotify session object
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    logger.info("Authenticated succesfully")

    # get uri from https link
    playlist_uri = get_playlist_uri_from_link(PLAYLIST_LINK)

    # get list of tracks in a given playlist (note: max playlist length 100)
    tracks = session.playlist_tracks(playlist_uri)["items"]

    # create csv file
    file_path = "/".join([OUTPUT_DIR, OUTPUT_FILE_NAME])
    with open(file_path, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["track", "artist"])

        # extract name and artist
        for track in tracks:
            name = track["track"]["name"]
            artists = ", ".join(
                [artist["name"] for artist in track["track"]["artists"]]
            )

            # write to csv
            writer.writerow([name, artists])

    logger.info("Extracted data saved in %s", file_path)
