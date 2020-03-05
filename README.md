# Massive subtitle downloader using IMDb and OpenSubtitles

~~ *This project was implemented in November 2018* ~~

This project is composed of 2 big steps:
* research of movies on **IMDb**
* download of the subtitles of these movies on **OpenSubtitles**

## Research of movies on **IMDb**

*listMovies.py* is a Python script to search via an API for the *id_movie_imdb* IDs of the movies you want on [*IMDb*](https://www.imdb.com/), an online database of information related to movies.

*id_movie_imdb* is an unique ID given by IMDb to a movie.
It can be found in the URL. For example if you open IMDb for a movie, say "The Dark Knight Rises", the URL will be "https://www.imdb.com/title/tt1345836/". This last text "tt1345836" is the *id_movie_imdb* for this movie.

The API used is [**IMDbPY**](https://imdbpy.github.io/), a Python package useful to retrieve and manage the data of the IMDb movie database about movies, people, characters and companies.

The current example coded in the script is the search for Disney animation films.

## Download of the subtitles on **OpenSubtitles**

*downloadSubtitles.py* is a Python script to search on [OpenSubtitles](opensubtitles.org) via an API for all the subtitles of movies whose identifiers have been extracted from IMDb before, then download them.

The API used is *XMLRPC*, it requires the creation of an OpenSubtitles account.
Then to connect to the API in the python script you have to fill in your login credentials on the line:
```
token = ost.login('id', 'password')
```

Subtitles are downloaded in several languages: *French*, *German*, *Spanish*, *Italian* and *English*. You can manage (add/delete) the languages as you wish, directly in the code.

Once downloaded, subtitles are saved in the repository *subtitles/*.
