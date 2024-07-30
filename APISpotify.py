import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yaml
import requests

# Récupération des clefs d'API dans les configs
with open("config.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    client_id = data["spotify_client_id"]
    client_secret = data["spotify_client_secret"]


# region Spotify API Credentials

# Permet de retourner l'URI de la première chanson trouvée
def recherche_chanson(nom_chanson):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Recherche de la chanson
    results = sp.search(q=nom_chanson, limit=1)

    # Récupération de l'URI de la première chanson trouvée
    if results["tracks"]["items"]:
        uri = results["tracks"]["items"][0]["uri"]
        return uri
    else:
        return None

# Retourne le nom de la chanson, l'artiste et l'URL de la chanson
def get_track_info(uri):
    # Authentification avec les clés d'API
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        # Obtenir les informations sur la piste à partir de son URI
        track_info = sp.track(uri)

        # Extraire le nom du titre et le premier artiste
        if track_info:
            track_name = track_info["name"]
            artist_name = track_info["artists"][0]["name"]
            url = track_info["external_urls"]["spotify"]
            return track_name, artist_name, url
        else:
            return None, None, None
    except spotipy.SpotifyException as e:
        print(f"Erreur : {e}")
        return None, None, None

# endregion

