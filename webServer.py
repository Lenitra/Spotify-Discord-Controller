from flask import Flask, request, redirect, jsonify
import requests
import base64
import time
import webbrowser
import yaml

app = Flask(__name__)

with open("config.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    client_id = data["spotify_client_id"]
    client_secret = data["spotify_client_secret"]
    redirect_uri = 'http://localhost:8888/callback'





# Fonction pour obtenir le jeton d'accès en échange du code d'autorisation
def get_access_token(code):
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()}
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()
    return token_info.get('access_token')


# Route pour l'URL de redirection
@app.route('/callback')
def callback():
    code = request.args.get('code')
    print("Le code expirera dans : ", request.args.get('expires_in'), " secondes")
    access_token = get_access_token(code)
    # save the access_token in a file
    with open('access_token.txt', 'w') as f:
        f.write(access_token)
    if access_token:
        # Vous pouvez effectuer d'autres actions ici, comme enregistrer le jeton d'accès dans une base de données
        return "Jetons d'accès obtenu avec succès!<br>"+access_token+"<script>setTimeout(function(){window.close();}, 1);</script>"
    else:
        return "Impossible d'obtenir le jeton d'accès."



# route pour afficher les infos de l'utilisateur (permet de debugger)
@app.route('/me')
def me():
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    return jsonify(response.json())



# Route pour ajouter une musique à la file d'attente
@app.route('/addqueue', methods=['POST'])
def addqueue():
    # Récupérer le jeton d'accès
    with open('access_token.txt', 'r') as f:
        access_token = f.read()
    headers = {'Authorization': 'Bearer ' + access_token}
    uri = request.args.get('uri')
    response = requests.post(f'https://api.spotify.com/v1/me/player/queue?uri={uri}', headers=headers)
    if response.status_code != 204 and response.status_code != 200:
        webbrowser.open('http://127.0.0.1:8888/')
        time.sleep(5)
        requests.post(f'http://localhost:8888/addqueue?uri={uri}')
    return "OK", 200


# Route pour l'URL d'autorisation
@app.route('/', methods=['GET' , 'POST'])
def login():
    # Remplacez les scopes par ceux que vous souhaitez demander à l'utilisateur
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming '
    state = 'some_state_value'  # Vous pouvez générer un état aléatoire ici si nécessaire
    authorize_url = 'https://accounts.spotify.com/authorize?' + \
                    'response_type=code&client_id=' + client_id + \
                    '&scope=' + scope + \
                    '&redirect_uri=' + redirect_uri + \
                    '&state=' + state
    return redirect(authorize_url)

if __name__ == '__main__':
    app.run(debug=True, port=8888)
