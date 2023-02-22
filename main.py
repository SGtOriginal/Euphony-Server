"""
Euphony Server, for playing music from YouTube and other sources right from your browser.
Copyright (C) 2023  SGtOriginal
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
Contact SGtOriginal using the this email: sgtoriginal@gmail.com
"""

from flask import *
from threading import Thread
import requests
import time
import os
import sqlite3
import euphony

app = Flask('Euphony', static_folder='static')


@app.route("/")
def home():
  return render_template("home.html", search=url_for('search'))


@app.route("/test")
def home_test():
  return render_template("home_test.html")


@app.route("/search", methods=['GET', 'POST'])
def search():
  if request.method == 'GET':
    if request.args.get('name') != None:
      name = request.args.get('name')
      if "-" in name:
        name = " ".join(name.split("-"))
      info = euphony.ytsearch(name)
      table = []
      for i in range(0, len(info)):
        table.append(
          f"<tr>\n    <td>{info[i][0]}</td>\n    <td>{info[i][1]}</td>\n    <td><a href = '{url_for('play')}?id={info[i][0]}'>Click to listen</a></td>\n</tr>"
        )
      table = ''.join(table)
      return f"<table>\n    <tr>\n        <th>YTId</th>\n        <th>Title</th>\n        <th>Link</th>\n    </tr>\n    {table}\n</table>"
    else:
      return "<form action=\"search\" method=\"post\">\n    <label for=\"search\">Song Name</label>\n    <input type=\"text\" name=\"search\" value=\"\" required></br></br>\n    <button type=\"submit\">Search</button>\n</form>"
  elif request.method == 'POST':
    if request.form['search']:
      name = request.form['search']
    else:
      return redirect(url_for("search"))
    if "-" in name:
      name = " ".join(name.split("-"))
    return redirect(url_for("search", name=name))


@app.route("/play")
@app.route("/play/<string:audid>")
def play(audid=None):
  if request.args.get('id') != None:
    id = request.args.get('id')
    check1 = os.listdir(os.path.join(os.getcwd(), 'static', 'music'))
    if f"{id}.mp3" not in check1:
      conn = sqlite3.connect('euphonydb.db')
      cur = conn.cursor()
      cur.execute("SELECT * FROM musicdata WHERE id=?", (id, ))
      check2 = cur.fetchall()
      conn.close()
      if len(check2) != 0:
        euphony.getfromdb(id)
        return render_template("song.html", id=id)

      elif len(check2) == 0:
        euphony.download(id)
        euphony.uploadtodb(id)
        return render_template("song.html", id=id)

    elif f"{id}.mp3" in check1:
      conn = sqlite3.connect('euphonydb.db')
      cur = conn.cursor()
      cur.execute("SELECT * FROM musicdata WHERE id=?", (id, ))
      check2 = cur.fetchall()
      if len(check2) != 0:
        return render_template("song.html", id=id)

      elif len(check2) == 0:
        euphony.uploadtodb(id)
        return render_template("song.html", id=id)

  elif audid != None:
    check1 = os.listdir(os.path.join(os.getcwd(), 'static', 'music'))
    if f"{audid}.mp3" not in check1:
      conn = sqlite3.connect('euphonydb.db')
      cur = conn.cursor()
      cur.execute("SELECT * FROM musicdata WHERE id=?", (audid, ))
      check2 = cur.fetchall()
      conn.close()
      if len(check2) != 0:
        euphony.getfromdb(id)
        return send_file(f"static/music/{audid}.mp3", mimetype="audio/mp3")

      elif len(check2) == 0:
        euphony.download(audid)
        euphony.uploadtodb(audid)
        return send_file(f"static/music/{audid}.mp3", mimetype="audio/mp3")

    elif f"{audid}.mp3" in check1:
      conn = sqlite3.connect('euphonydb.db')
      cur = conn.cursor()
      cur.execute("SELECT * FROM musicdata WHERE id=?", (audid, ))
      check2 = cur.fetchall()
      if len(check2) != 0:
        return send_file(f"static/music/{audid}.mp3", mimetype="audio/mp3")

      elif len(check2) == 0:
        euphony.uploadtodb(id)
        return send_file(f"static/music/{audid}.mp3", mimetype="audio/mp3")

  else:
    return redirect(url_for("search"))


def run():
  app.run(host='0.0.0.0', port=8080)


def server():
  th = Thread(target=run)
  th.start()
  while True:
    requests.get("https://Euphony-Server.sgtoriginal.repl.co")
    time.sleep(30)


if os.path.exists("static"):
  os.chdir("static")
  if os.path.exists("music"):
    os.chdir(app.root_path)
    pass
  else:
    os.mkdir("music")
    os.chdir(app.root_path)
else:
  os.mkdir("static")
  os.chdir("static")
  os.mkdir("music")
  os.chdir(app.root_path)

conn = sqlite3.connect("euphonydb.db")
cur = conn.cursor()
cur.executescript("""
    CREATE TABLE IF NOT EXISTS "musicdata" (
        "id"	TEXT,
        "url"	TEXT,
        "yturl"	TEXT,
        "file"	BLOB
    )
    """)
conn.commit()

if os.name == 'nt':
  os.system('cls')
else:
  os.system("clear")
print("""
-----------------------------------------------------------------------------------
#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#
-----------------------------------------------------------------------------------
   ▄████████ ███    █▄     ▄███████▄    ▄█    █▄     ▄██████▄  ███▄▄▄▄   ▄██   ▄   
  ███    ███ ███    ███   ███    ███   ███    ███   ███    ███ ███▀▀▀██▄ ███   ██▄ 
  ███    █▀  ███    ███   ███    ███   ███    ███   ███    ███ ███   ███ ███▄▄▄███ 
 ▄███▄▄▄     ███    ███   ███    ███  ▄███▄▄▄▄███▄▄ ███    ███ ███   ███ ▀▀▀▀▀▀███ 
▀▀███▀▀▀     ███    ███ ▀█████████▀  ▀▀███▀▀▀▀███▀  ███    ███ ███   ███ ▄██   ███ 
  ███    █▄  ███    ███   ███          ███    ███   ███    ███ ███   ███ ███   ███ 
  ███    ███ ███    ███   ███          ███    ███   ███    ███ ███   ███ ███   ███ 
  ██████████ ████████▀   ▄████▀        ███    █▀     ▀██████▀   ▀█   █▀   ▀█████▀
-----------------------------------------------------------------------------------
X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X#X
-----------------------------------------------------------------------------------
""")

server()
