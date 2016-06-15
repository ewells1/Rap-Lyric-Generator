import urllib
import json
import secrets

# Uses Musixmatch API to get lyrics for a particular artist
class LyricFetcher:

    def getLyrics(self, artistname):
        # URL pieces
        root = "http://api.musixmatch.com/ws/1.1/"
        suffix = "&format=json&apikey=" + secrets.apikey

        # Find artist and get id
        artistname = artistname.replace(' ', '-')
        url = root + "artist.search?q_artist=" + artistname + suffix
        # print(url)  # debug
        jsonobj = urllib.request.urlopen(url)
        jsonobj = jsonobj.readall().decode('utf-8')
        # print(jsonobj)  # debug
        artists = json.loads(jsonobj)
        artistid = artists["message"]["body"]["artist_list"][0]["artist"]["artist_id"]
        # print(artistid)  # debug

        # Get artist's albums
        url = root + "artist.albums.get?artist_id=" + str(artistid) + suffix
        # print(url)  # debug
        jsonobj = urllib.request.urlopen(url)
        jsonobj = jsonobj.readall().decode('utf-8')
        # print(jsonobj)  # debug
        albums = json.loads(jsonobj)
        albumids = []
        for album in albums["message"]["body"]["album_list"]:
            albumids.append(album["album"]["album_id"])
        # print(albumids)  # debug

        # Get songs from each album
        trackids = []
        for album in albumids:
            url = root + "album.tracks.get?album_id=" + str(album) + suffix
            # print(url)  # debug
            jsonobj = urllib.request.urlopen(url)
            jsonobj = jsonobj.readall().decode('utf-8')
            # print(jsonobj)  # debug
            tracks = json.loads(jsonobj)
            for track in tracks["message"]["body"]["track_list"]:
                trackids.append(track["track"]["track_id"])
        # print(trackids)  # debug

        # Get lyrics for each song
        lyricsbytrack = []
        for track in trackids:
            url = root + "track.lyrics.get?track_id=" + str(track) + suffix
            # print(url)  # debug
            jsonobj = urllib.request.urlopen(url)
            jsonobj = jsonobj.readall().decode('utf-8')
            # print(jsonobj)  # debug
            lyric = json.loads(jsonobj)
            if lyric["message"]["header"]["status_code"] != 404:
                lyricsbytrack.append(lyric["message"]["body"]["lyrics"]["lyrics_body"])
        # print(lyricsbytrack)  # debug

        # Clean up lyrics and put them together
        lyrics = ""
        for track in lyricsbytrack:
            tracklyrics = track.splitlines()
            track = ". ".join(tracklyrics[:-1])  # remove disclaimer
            lyrics += ". " + track
        # print(lyrics)  # debug
        lyrics = lyrics.lower()

        return lyrics
