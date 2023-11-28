import pandas as pd
import warnings
from tqdm import tqdm

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy_credentials import client_id, client_secret, redirect_uri

warnings.filterwarnings("ignore")

SPOTIPY_CLIENT_ID = client_id
SPOTIPY_CLIENT_SECRET = client_secret
SPOTIPY_REDIRECT_URI = redirect_uri

def get_playlist(type: str) -> pd.DataFrame:
    if type.lower() == "liked":  # liked songs
        scope = 'user-top-read user-library-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                                    scope=scope))
        #  obtaining audio features
        results = sp.current_user_saved_tracks()
        tracks = results['items']
        #  paginating through rest of the tracks since spotipy.current_user_saved_tracks()gives max 20.
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        tracks_ids = [item["track"]["id"] for item in tracks]  # getting tracks ids
        chunks = [tracks_ids[x:x+100] for x in range(0, len(tracks_ids), 100)]  # dividing in chunks of 100 ids 
        audio_features_in_chunks = [sp.audio_features(chunk) for chunk in chunks]  # getting features of chunks
        audio_features = [features for chunk_list in audio_features_in_chunks 
                          for features in chunk_list]  # merging features maps into one list
    else:  # top50
        scope = 'playlist-read-private playlist-read-collaborative'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                                    scope=scope))
        playlists = sp.category_playlists(category_id='toplists', country='PL', limit=50)
        top50_id = playlists["playlists"]["items"][0]["id"] if type.lower() == "poland" \
        else playlists["playlists"]["items"][1]["id"]
        results = sp.playlist_tracks(top50_id)
        tracks = results['items']
        tracks_id = [track_id["track"]["id"] for track_id in tracks]
        audio_features = sp.audio_features(tracks_id)  # extracting audio features
    
    #  creating datasets to save
    data = pd.DataFrame.from_records(audio_features)
    data["artists"] = pd.Series([', '.join([artists_info["name"]  # adding artists names to a dataframe
                                            for artists_info in item["track"]["artists"]]) 
                                        for item in tracks])
    data["track_name"]  = pd.Series([item["track"]["name"] for item in tracks])  # adding track names to a dataframe

    artists_ids = [item["track"]["artists"][0]["id"] for item in tracks]  # adding genres to a dataframe
    genres = []
    for art_id in tqdm(artists_ids, desc=f"Assigning genres to a songs - {type}..."):
        try:
            genres.append(sp.artist(art_id)["genres"][0])
        except IndexError:  # in case genres are not assigned
            genres.append(None)
    data["genre"] = pd.Series(genres)
    
    data = data.iloc[:, list(range(-3, data.shape[1]-3))]  # reordering columns so artist, track name and genre are first
    data.drop(["type", "id", "uri", "track_href", "analysis_url"], axis=1, inplace=True)  # dropping useless columns
    data.drop_duplicates(["artists", "track_name"], inplace=True)  # in case there are duplicated songs somewhere 
    return data

def main():
    liked_songs = get_playlist(type="liked")
    top50_poland = get_playlist(type="poland")
    top50_world = get_playlist(type="world")

    # change saving path for your usecase and machine
    save_path = "../personal_spotify_analysis/datasets/"
    liked_songs.to_csv(save_path+"liked_songs.csv", index=False)
    top50_poland.to_csv(save_path+"top50_poland.csv", index=False)
    top50_world.to_csv(save_path+"top50_world.csv", index=False)

    print(f"Datasets created at location: {save_path}")
    quit()

if __name__ == "__main__":
    main()