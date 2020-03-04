# Massive subtitle downloader using IMDb and OpenSubtitles

~~ *This project was implemented in November 2018* ~~

2 scripts :

- un listMovies.py  pour chercher via une API les identifiants des films que l'on veut sur IMDb, an online database of information related to films
idmovieimdb
from imdb import IMDb
l'exemple présent dans le script est la recherche de films d'animation Disney


- un downloadSubtitles.py pour chercher via une API qui requiert la création d'un compte OpenSubtitles, tous les sous-titres des films dont les identifiants ont été extraits sur IMDb, puis les télécharger
pythonopensubtitles.opensubtitles import OpenSubtitles
to log in: token = ost.login('id', 'password')
sub_languages = {'fre': 'French', 'ger': 'German', 'spa': 'Spanish', 'ita': 'Italian', 'eng': 'English'}

dossier subtitles/
