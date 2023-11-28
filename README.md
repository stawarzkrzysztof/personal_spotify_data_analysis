# Personal _Spotify_ data analysis  
## Done __November 2023__  
This is my first big data analysis personal project. I tried coding it in such a way so anybody can download this repo and with some changes, hopefully run the notebook himself.
# __Files description:__  
- `spotipy_credentials.py`: here I was storing my keys and url obtained on [Spotify for Developers](https://developer.spotify.com) website. If you want to run this project, create Developer account on Spotify and paste your credentials there
- `create_datasets.py`: this script connects to your Spotify account using `spotipy` and scraps the data from __Liked Songs__, __TOP50 Poland__ and __TOP50 World__ playlist for later comparsion in the analysis notebook
- `datasets`: in this folder three `.csv` files will be created after `create_datasets.py` script runs successfully
- `project_functions.py`: durning analysis I wrote two big functions and decided to move them to their separate file so the acutal notebook wouldn't be too long to read through
  - one funcion uses `BeautifulSoup` framework to scrap data from website docs, where features generated with `spotipy` are described
  - other function connects to user's Spotify account and creates `matplotlib` plots with so-called "Spotify Wrapped"; it shows user's top 5 most played artists and tracks in three different time periods
- `spotify_analysis_project.ipynb`: actual notebook with the whole analysis and visualizations.

# __About__  
I want my prorfolio to be personal, so this time I decided on analyzing my own __Liked Songs__ Spotify playlist, since I tend to add there all the songs I acutally like.  
# __Goals__  
My goal was simply to explore my main playlist and get better understanding of my music taste in general.
# __Visuals__  
  
# __Conclusions__
