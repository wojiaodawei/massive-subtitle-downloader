#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os

from pythonopensubtitles.opensubtitles import OpenSubtitles
from xmlrpc.client import ProtocolError

out_dir = "./subtitles/"

ost = OpenSubtitles()

# Login
token = ost.login('id', 'password')
print(token)

imdb_ids = list()
with open('movies_found.txt', 'r') as f:
    for line in f.readlines():
        identifiant, titre = line.strip().split('\t')
        imdb_ids.append((int(identifiant), titre))
            
sub_languages = {'fre': 'French', 'ger': 'German', 'spa': 'Spanish', 'ita': 'Italian', 'eng': 'English'}

already_requested = list()
with open("requests.txt", 'r') as f:
    for line in f.readlines():
        title, lang = line.strip().split('\t')
        already_requested.append((title, lang))
        
already_missed = list()
with open("missings.txt", 'r') as f:
    for line in f.readlines():
        title, lang = line.strip().split('\t')
        already_missed.append((title, lang))
        
# Create a function called "chunks" with two arguments, l and n:
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

"""
API RATE LIMIT of 40 requests per 10 second per IP Address
"""
nb_requests = 0
start = time.time()
start_ping = time.time()

def testLimit():
    global nb_requests, start, start_ping, ost
    # Every 15 minutes, you need to ping the server to show that you are alive
    ping_time = time.time() - start_ping
    if ping_time >= 840:
        pinging = False
        while not pinging:
            if ost.no_operation() == True:
                pinging = True
                start_ping = time.time()
    if nb_requests >= 40:
        process_time = time.time() - start
        wait_time = abs(10 - process_time) + 1
        time.sleep(wait_time)
        nb_requests = 0
        start = time.time()

def search_subtitles(sl_id, imdb_id):
    global nb_requests, ost, start_ping
    requesting = False
    while not requesting:
        try:
            testLimit()
            data = ost.search_subtitles([{'sublanguageid': sl_id, 'imdbid': imdb_id, 'extensions': 'srt'}])
            nb_requests += 1
            requesting = True
        except ProtocolError as e:
            print(e)
        except:
            print("ResponseNotReady: Request-sent")
            time.sleep(5)             
    return data

def add_request(sl_id, imdb_id):
    global nb_requests, ost, start_ping
    requesting = False
    while not requesting:
        try:
            testLimit()
            print("Request subtitle", ost.add_request({'sublanguageid': sl_id, 'idmovieimdb': imdb_id}))
            nb_requests += 1
            requesting = True
        except ProtocolError as e:
            print(e)
        except:
            print("ResponseNotReady: Request-sent")
            time.sleep(5)

def download_subtitles(list_id_subtitles, filenames, outpath):
    global nb_requests, ost, start_ping
    requesting = False
    while not requesting:
        try:
            testLimit()
            print("Download subtitles", ost.download_subtitles(list_id_subtitles, override_filenames=filenames, output_directory=outpath, extension='srt'))
            nb_requests += 1
            requesting = True
        except ProtocolError as e:
            print(e)
        except:
            print("ResponseNotReady: Request-sent")
            time.sleep(5)
    
requests = open("requests.txt", 'a')
missings = open("missings.txt", 'a')

# Search for subtitles
for sl_id in sub_languages.keys():
    print("~~~~~~~~~~~~~~ ", sub_languages.get(sl_id), " ~~~~~~~~~~~~~~")
    id_subtitles = list()
    filenames = dict()
    outpath = out_dir+sl_id+'/'
    dirs = os.listdir(outpath)
    for imdb_id, title in imdb_ids:
        print(title)
        if (title, sl_id) in already_requested or (title, sl_id) in already_missed:
            print("*********  already requested  *********")
        else:
            filename = title + '.srt'
            if filename not in dirs:
                data = search_subtitles(sl_id, imdb_id)
                if len(data) > 0:
                    print("*********  download in progress  *********")
                    #id_subtitle = data[0].get('IDSubtitle')
                    id_subtitle_file = data[0].get('IDSubtitleFile')
                    id_subtitles.append(id_subtitle_file)
                    filenames[id_subtitle_file] = filename
                else:
                    print('---------  is missing in', sl_id, 'version  ---------')
                    missings.write(title + '\t' + sl_id + '\n')
            else:
                print("*********  already downloaded  *********")
    # Download of subtitles
    # Create a list that from the results of the function chunks:
    for list_id_subtitles in list(chunks(id_subtitles, 20)):
        download_subtitles(list_id_subtitles, filenames, outpath)

requests.close()
missings.close()

# Remove your session token
ost.logout()
