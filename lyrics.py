import configparser
import requests
from bs4 import BeautifulSoup

def getAccessToken():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Client_Access_Token']['token']

token = getAccessToken()

def searchMusicArtist(name):
    api_url = "https://api.genius.com/search?q={}".format(name)
    headers = {'authorization':token}
    r = requests.get(api_url, headers=headers)
    return r.json()

#searchMusicArtist("drake")

def getArtistID(name):
    r = searchMusicArtist(name)
    id = r['response']['hits'][0]['result']['primary_artist']['id']
    return id

#print(getArtistID('drake'))

def getTopTenSongs(name):
    id = getArtistID(name)
    #api_url = "https://api.genius.com/artists/{}/songs?sort=popularity&per_page=10".format(id)
    api_url = "https://api.genius.com/artists/{}/songs".format(id)
    headers = {
        'authorization':token
    }
    params={
        'sort':'popularity',
        'per_page':10
    }
    r = requests.get(api_url, headers=headers, params=params)
    return r.json()

#print(getTopTenSongs('drake'))
def getSongURLs(name):
    topTenSongs = getTopTenSongs(name)
    songs = topTenSongs['response']['songs']
    song_urls = []
    for song in songs:
        song_urls.append(song['url'])
    return song_urls

def scrapeLyricText(name):
    links = getSongURLs(name)
    song_lyrics = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics_div =  soup.find(class_='lyrics')
        anchor_tags = lyrics_div.find_all('a')
        current_lyrics = []
        for anchor in anchor_tags:
            text = anchor.text
            if len(text) > 0 and text[0] != '[':
                current_lyrics.append(text)
        song_lyrics.append(current_lyrics)
    return song_lyrics

#print(scrapeLyricText('drake'))