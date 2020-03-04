#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import http.client
from ast import literal_eval

imdb_ids = list()  
with open('imdb_ids.txt', 'r') as f:
    for line in f.readlines():
        l = line.strip()
        if l != '':
            imdb_ids.append(int(l))
print("Nb de films trouvés (TMDb) : ", len(imdb_ids))

from imdb import IMDb, IMDbError

try:
    # create and instance of the IMDb class
    ia = IMDb(accessSystem='http', adultSearch=False)

    cleaned_imdb_ids = list()

    disney_companies = ia.search_company('Disney')
    #disney_movies = ia.get_keyword('disney')
    #print("Nb de films trouvés : ", len(disney_movies))
    #for i, movie in enumerate(disney_movies):
    for i, movie_id in enumerate(imdb_ids):
        print(i+1)
        #movie = ia.get_movie(movie.movieID)
        movie = ia.get_movie(movie_id)
        if 'title' in movie:
            print(movie['title'])
            if 'genres' in movie and 'kind' in movie:
                if 'Animation' in movie['genres'] and movie['kind'] == 'movie':
                    is_truly_disney = False
                    for company in disney_companies:
                        if 'production companies' in movie:
                            if company in movie['production companies'] or company in movie['distributors']:
                                is_truly_disney = True
                                break
                    if is_truly_disney:
                        print("VRAI")
                        cleaned_imdb_ids.append((int(movie.movieID), movie['title'] + " (" + str(movie["year"]) + ")"))
    print("Nb de films trouvés (IMDb) : ", len(cleaned_imdb_ids))
    with open('movies_found.txt', 'w') as f:
        f.write('\n'.join([str(identifiant) + '\t' + titre for (identifiant, titre) in cleaned_imdb_ids]))
except IMDbError as e:
    print(e)
