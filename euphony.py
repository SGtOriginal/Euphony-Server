from youtube_search import YoutubeSearch
from pytube import YouTube
import time
import json
import os
import sqlite3

def download(id = None, name = None):
    if name != None:
        yturl = yturlget(name)
        ytid = ytidget(name)
        yt = YouTube(yturl)
        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download(output_path=f"{os.path.join(os.getcwd(), 'static', 'music')}")
        new_file = f'{ytid}.mp3'
        os.rename(f"{os.path.join(os.getcwd(), 'static', 'music', out_file)}", f"{os.path.join(os.getcwd(), 'static', 'music', new_file)}")
    elif id != None:
        yturl = yturlget(id)
        yt = YouTube(yturl)
        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download(output_path=f"{os.path.join(os.getcwd(), 'static', 'music')}")
        new_file = f'{id}.mp3'
        os.rename(f"{os.path.join(os.getcwd(), 'static', 'music', out_file)}", f"{os.path.join(os.getcwd(), 'static', 'music', new_file)}")

def yturlget(id = None, name = None):
    if name != None:
        yturl = f"https://www.youtube.com/watch?v={json.loads(YoutubeSearch(name, max_results=1).to_json())['videos'][0]['id']}"
        return yturl
    elif id != None:
        yturl = f"https://www.youtube.com/watch?v={id}"
        return yturl

def ctbd(filename):
    with open(filename, 'rb') as file:
        blobdata = file.read()
    return blobdata

def wtf(name, data):
    with open(f"{os.path.join(os.getcwd(), 'static', 'music', f'{name}.mp3')}", 'wb') as file:
        file.write(data)

def uploadtodb(id = None, name = None):
    if name != None:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        yturl = yturlget(name)
        ytid = ytidget(name)
        url = f"/play?id={ytid}"
        file = ctbd(f"{os.path.join(os.getcwd(), 'static', 'music', f'{ytid}.mp3')}")
        cur.execute("INSERT INTO musicdata (id, url, yturl, file) VALUES (?, ?, ?, ?)", (ytid, url, yturl, file,))
        conn.commit()
        conn.close()
    elif id != None:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        yturl = yturlget(id)
        url = f"/play?id={id}"
        file = ctbd(f"{os.path.join(os.getcwd(), 'static', 'music', f'{id}.mp3')}")
        cur.execute("INSERT INTO musicdata (id, url, yturl, file) VALUES (?, ?, ?, ?)", (id, url, yturl, file,))
        conn.commit()
        conn.close()

def getfromdb(id = None, name = None):
    if name != None:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        ytid = ytidget(name)
        cur.execute("SELECT * FROM musicdata WHERE id=?", (ytid,))
        stuff = cur.fetchall()
        for row in stuff:
            wtf(ytid, row[3])
        conn.close()
    elif id != None:
        conn = sqlite3.connect('euphonydb.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM musicdata WHERE id=?", (id,))
        stuff = cur.fetchall()
        for row in stuff:
            wtf(id, row[3])
        conn.close()

def ytidget(name, i = 1, j = 0):
    ytid = json.loads(YoutubeSearch(name, max_results=i).to_json())["videos"][j]["id"]
    return ytid

def ytsearch(name):
    all = json.loads(YoutubeSearch(name, max_results=25).to_json())["videos"]
    info = []
    for i in range(0, len(all)):
        info.append([all[i]["id"], all[i]["title"]])
    return info