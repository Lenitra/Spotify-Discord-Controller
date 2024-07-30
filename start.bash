#!/bin/bash

# Ecrit le fichier temporaire vide `access_token.txt`
: > acces_token.txt

# Exécute le premier script Python dans un nouveau terminal
gnome-terminal -- python3 webServer.py

# Exécute le deuxième script Python dans un autre nouveau terminal
gnome-terminal -- python3 BotDiscord.py

