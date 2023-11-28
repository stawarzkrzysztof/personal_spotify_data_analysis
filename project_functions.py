import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy_credentials import client_id, client_secret, redirect_uri

#  scrap data from docs
def get_features_description(url: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #  really simple and probably useless scraping by html tags of the api website 
    feature_names = [ft.text 
                    for ft in soup.find_all('span',
                                            {'data-encore-id': "type", 
                                            "class":"Type__TypeElement-sc-goli3j-0 cfrXIO"})][4:]

    #  float type are called 'number' for some reason, I remaped it anyway
    feature_types = [ft.text 
                    if ft.text != "number" else "float"
                    for ft in soup.find_all('span', 
                                            {'data-encore-id': "type", 
                                            "class":"Type__TypeElement-sc-goli3j-0 bTCbvk"})][2:]

    feature_descs = [ft.text 
                    for ft in soup.find_all('p',
                                            {'data-encore-id': "type", 
                                            "class":"Type__TypeElement-sc-goli3j-0 bYQtYg"})][3:]

    feature_ranges = [ft.text 
                    for ft in soup.find_all('span', 
                                            {'data-encore-id': "type", 
                                            "class":"Type__TypeElement-sc-goli3j-0 etChWo"})][1:]
    feature_additional_infos = []
    examples_done = []
    for i, fr in enumerate(feature_ranges):
        if fr in examples_done: continue
        elif fr.split(":")[0] == "Range":
            feature_additional_infos.append((fr, feature_ranges[i+1]))
            examples_done.append(feature_ranges[i+1])
        else: feature_additional_infos.append(fr)
            
    #  here the final dict is created
    features_dict = {
        feature_name: {
            "type": feature_type,
            "description": feature_desc,
            "extra_info" : feature_additional_info
        }
        for feature_name, feature_type, feature_desc, feature_additional_info in \
            zip(feature_names, feature_types, feature_descs, feature_additional_infos)
    }
    
    return features_dict


#  show favourite artists and tracks this year
def show_spotify_wrapped(kind: str, top_limit=5, ):
    
    term_mapper = {
        "short_term": "4 weeks",
        "medium_term": "6 months",
        "long_term": "lifetime"
    }
    
    SPOTIPY_CLIENT_ID = client_id
    SPOTIPY_CLIENT_SECRET = client_secret
    SPOTIPY_REDIRECT_URI = redirect_uri
    scope = 'user-top-read user-library-read'
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))
    
    fig = plt.figure(figsize=(20, 10))
    subfigs = fig.subfigures(nrows=3, ncols=1)

    for row, (subfig, term) in enumerate(zip(subfigs, term_mapper.keys())):
        subfig.suptitle(f"My TOP{top_limit} {kind.title()} - {term_mapper[term]}", 
                        weight="bold", 
                        fontsize=15, 
                        y=.95)
        
        top_items = sp.current_user_top_artists(limit=top_limit, time_range=term) if kind.lower()=="artists" else sp.current_user_top_tracks(limit=top_limit, time_range=term)
        
        axs = subfig.subplots(nrows=1, ncols=top_limit)
        for i, (ax, item) in enumerate(zip(axs, top_items["items"])):
            
            if kind.lower()=="artists": item_image_url = item["images"][0]["url"]
            else:
                #  getting trak artists list and printing only 2, '...' if needed
                track_artists = [item["artists"][j]["name"] for j in range(len(item["artists"]))]
                track_artists2show = ', '.join(track_artists) \
                if len(track_artists) <= 2 else ', '.join(track_artists[:2])+"..."
                
                item_image_url = item["album"]["images"][0]["url"]

            with urllib.request.urlopen(item_image_url) as url:
                image_data = mpimg.imread(url, format='jpg')
                
            ax.grid(visible=False)
            ax.imshow(image_data)
            ax.set_xlabel(f"{i+1}. {item['name']}") if kind.lower()=="artists" else ax.set_xlabel(f"{i+1}. {track_artists2show} - {item['name']}", fontsize=11)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.tick_params(left=False, bottom=False)